# -*- coding: utf-8 -*-
from maya.api.OpenMaya import *
from PySide.QtGui import *
from vic.vicTools import DataManager
from vic.vicGui import BasicUI
import random

class MoveObj():
    def __init__(self, name):
        selection = MGlobal.getSelectionListByName( name )
        self.__node = selection.getDependNode(0)
        self.__transform = MFnTransform(selection.getDagPath(0).transform())    
        self.__bounding = MFnDagNode( selection.getDagPath(0) ).boundingBox.transformUsing( self.getMatrix().inverse() )
        self.velocity = MVector()
        
    def getPosition(self):
        return self.__transform.translation( MSpace.kTransform )
        
    def setPosition(self, pos):
        self.__transform.setTranslation( pos, MSpace.kTransform )
        
    def getBoundingBox(self):
        globalBoundingBox = MBoundingBox( self.__bounding )
        globalBoundingBox.transformUsing( self.getMatrix() )
        return globalBoundingBox
        
    def checkHit( self, bounding ):
        return self.getBoundingBox().intersects( bounding )
        
    def getMatrix( self ):
        return self.__transform.transformation().asMatrix()
        
    def update(self):
        position = self.getPosition()
        position += self.velocity
        self.velocity *= .9
        self.setPosition( position )
        
class GameManager():
    onHitCandy = 'onHitCandy'
    onDead = 'onDead'
    def __init__(self):
        self.player = MoveObj( "pCube1" )
        self.candys = [MoveObj( "pSphere1" )]
    def start(self):
        self.player.setPosition( MVector())
        self.dead = 0
        self.power = 0
        
        for candy in self.candys:
            candy.setPosition( MVector(random.random() * 16 - 8, 30, random.random() * 16 - 8 ))
            
    def update(self):
        def checkWall(mobj):
            mobjPos = mobj.getPosition()
            if mobjPos.x > 10:
                mobjPos.x = 10
                mobj.velocity.x *= -.4
                mobj.setPosition( mobjPos )
            elif mobjPos.x < -10:
                mobjPos.x = -10
                mobj.velocity.x *= -.4
                mobj.setPosition( mobjPos )
            if mobjPos.z > 10:
                mobjPos.z = 10
                mobj.velocity.z *= -.4
                mobj.setPosition( mobjPos )
            elif mobjPos.z < -10:
                mobjPos.z = -10
                mobj.velocity.z *= -.4
                mobj.setPosition( mobjPos )
                
        def checkHitPlayer(player, mobj):
            if player.checkHit( mobj.getBoundingBox() ):
                diff = mobj.getPosition() - player.getPosition()
                if mobj.velocity.y < 0:
                    mobj.velocity.y *= -2.5
                    mobj.velocity.x += diff.x * .5
                    mobj.velocity.z += diff.z * .5
                    self.power += 1
                    MUserEventMessage.postUserEvent(GameManager.onHitCandy) 
                
        def checkDead(mobj):
            return mobj.getPosition().y < -20
          
        self.player.update()    
        checkWall( self.player )
        
        for candy in self.candys:
            candy.velocity.y -= .1
            checkWall( candy )
            checkHitPlayer( self.player, candy )
            if checkDead( candy ):
                candy.velocity.y *= -5
                self.dead += 1
                MUserEventMessage.postUserEvent(GameManager.onDead) 
            candy.update()
        
game = None
def gameStart():
    global game
    game = GameManager()
    game.start()
    
    def onTimeUpdate(*args):
        game.update()
    
    gameEnd()
    
    if not MUserEventMessage.isUserEvent(GameManager.onHitCandy):
        MUserEventMessage.registerUserEvent(GameManager.onHitCandy)
        MUserEventMessage.registerUserEvent(GameManager.onDead)
        
    dataManager = DataManager.getInstance()
    dataManager.setData( 'timeChangeEventId', MDGMessage.addTimeChangeCallback(onTimeUpdate))
    
def gameEnd():
    
    if MUserEventMessage.isUserEvent(GameManager.onHitCandy):
        MUserEventMessage.deregisterUserEvent(GameManager.onHitCandy)
        MUserEventMessage.deregisterUserEvent(GameManager.onDead)
    
    dataManager = DataManager.getInstance()
    if dataManager.hasData('timeChangeEventId'):
        try:
            MDGMessage.removeCallback( dataManager.getData('timeChangeEventId') )
        except:
            pass
        dataManager.removeData( 'timeChangeEventId')
        
def moveUp(speed):
    if game is not None:
        game.player.velocity.z += -speed
        
def moveDown(speed):
    if game is not None:    
        game.player.velocity.z += speed             
        
def moveLeft(speed):
    if game is not None:
        game.player.velocity.x += -speed
        
def moveRight(speed):
    if game is not None:    
        game.player.velocity.x += speed        

class GameUI(BasicUI):
    def _showWindow( self, uiName):
        BasicUI._showWindow( self, uiName )
        
        vlayout = QVBoxLayout( self.getMainWidget() )
        
        grp_game = QGroupBox( 'Game' )
        grp_game_layout = QHBoxLayout()
        grp_game.setLayout( grp_game_layout )
        
        vlayout.addWidget( grp_game )
        
        grp_controller = QGroupBox('Controller')
        grp_controller_layout = QVBoxLayout()
        grp_controller.setLayout( grp_controller_layout )
        
        grp_controller_layout_layout1 = QHBoxLayout()
        grp_controller_layout_layout2 = QHBoxLayout()
        grp_controller_layout_layout3 = QHBoxLayout()
        grp_controller_layout.addLayout( grp_controller_layout_layout1 )
        grp_controller_layout.addLayout( grp_controller_layout_layout2 )
        grp_controller_layout.addLayout( grp_controller_layout_layout3 )
        
        vlayout.addWidget( grp_controller )
        
        btn_start = QPushButton('Start')
        btn_start.clicked.connect( lambda : gameStart() )
        grp_game_layout.addWidget( btn_start )
        
        btn_end = QPushButton('End')
        btn_end.clicked.connect( lambda : gameEnd() )
        grp_game_layout.addWidget( btn_end )
        
        btn_up = QPushButton('Up')
        btn_up.clicked.connect( lambda : moveUp( 1 ))
        grp_controller_layout_layout1.addWidget( btn_up )
        
        btn_left = QPushButton('<-')
        btn_left.clicked.connect( lambda : moveLeft( 1 ))
        grp_controller_layout_layout2.addWidget( btn_left )
        
        btn_right = QPushButton('->')
        btn_right.clicked.connect( lambda : moveRight( 1 ))
        grp_controller_layout_layout2.addWidget( btn_right )
        
        btn_down = QPushButton('Down')
        btn_down.clicked.connect( lambda : moveDown( 1 ))
        grp_controller_layout_layout3.addWidget( btn_down )
        
GameUI('Small Game')
    
    









