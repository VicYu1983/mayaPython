from maya.cmds import *
from PySide.QtGui import *
from vic.vicTools import DataManager
from vic.vicTools import GameObj
from vic.vicGui import BasicUI
import random

class gameManager():
    def __init__(self, onDead):
        self.__pilePrefab = GameObj('TubePrefab')
        self.__player = GameObj('Player', False)
        self.__player.friction = 1
        self.__onDead = onDead
        pass
        
    def __createPiles(self):
        heights = [ random.random() * 6 - 3 for i in range(5) ]
        
        for i, h in enumerate( heights ):
            pile = self.__pilePrefab.clone()
            pile.setName( 'pile' )
            pile.velocity.x = -.2
            pile.friction = 1
            pile.setPosition( MVector( i * 7 + 2, heights[i], 0 ))
            self.__bottomPiles.append( pile )
            self.__allPiles.append( pile )        
            
        for i, h in enumerate( heights ):
            pile = self.__pilePrefab.clone()
            pile.setName( 'pile' )
            pile.velocity.x = -.2
            pile.friction = 1
            pile.setRotation( MEulerRotation( 0, 0, 3.14159 ))
            pile.setPosition( MVector( i * 7 + 2, heights[i] + 25, 0 ))
            self.__topPiles.append( pile )
            self.__allPiles.append( pile )      
        
    def start(self):
        self.__topPiles = []
        self.__bottomPiles = []
        self.__allPiles = []
        self.__createPiles()
        self.__player.setPosition( MVector( -7, 12, 0 ))
        self.__player.velocity.y = .3
        self.__time = 0
        select(clear=True)
        pass
        
    def jump( self ):
        self.__player.velocity.y += .5
        
    def dead( self ):
        if self.__onDead is not None:
            self.__onDead()
            
    def getTime(self):
        return self.__time
        
    def update(self):
        self.__time += 1
        
        self.__player.velocity.y -= .03
        self.__player.update()
        
        if self.__player.getPosition().y < 1.5:
            self.dead()
        elif self.__player.getPosition().y > 24:
            self.dead()
        
        for p in self.__allPiles:
            p.update()
            
        for i, bottomPile in enumerate( self.__bottomPiles ):
            topPile = self.__topPiles[i]
            if topPile.checkHit( self.__player ):
                self.dead()
            if bottomPile.checkHit( self.__player ):
                self.dead()
            if bottomPile.getPosition().x < -17.5:
                newHeight = random.random() * 6 - 3
                bottomPile.setPosition( MVector( 17.5, newHeight, 0 ))
                topPile.setPosition( MVector( 17.5, newHeight + 25, 0 ))
                
    
class AngryBirdUI(BasicUI):
    def _showWindow( self, uiName ):
        BasicUI._showWindow(self, uiName )
        
        self.game = None
        def onTimeUpdate(*args):
            if self.game is not None:
                self.game.update()
                lbl_msg.setText('Score:' + str(self.game.getTime()))
                
        def onDead():
            lbl_msg.setText('GameOver! Score:' + str(self.game.getTime()) + ' Please Try Again')
            gameEnd()
            
        def gameJump():
            if self.game is not None:
                self.game.jump()
            
        def gameStart():
            
            try:
                delete( 'pile*')
            except:
                pass
                
            self.game = gameManager(onDead)
            self.game.start()
            
            gameEnd()
            dataManager = DataManager.getInstance()
            dataManager.setData( 'timeChangeEventId', MDGMessage.addTimeChangeCallback(onTimeUpdate))
            
        def gameEnd():
            dataManager = DataManager.getInstance()
            if dataManager.hasData('timeChangeEventId' ):
                 MDGMessage.removeCallback( dataManager.getData('timeChangeEventId') )
                 dataManager.removeData('timeChangeEventId')
                 
        mainLayout = QVBoxLayout( self.getMainWidget() )
        
        gameLayout = QHBoxLayout()
        gameControllerBroup = QGroupBox('Controller')
        gameControllerLayout = QHBoxLayout()
        gameControllerBroup.setLayout( gameControllerLayout )
        
        mainLayout.addLayout( gameLayout )
        mainLayout.addWidget( gameControllerBroup )
        
        btn_start = QPushButton('Start')
        btn_start.clicked.connect( lambda : gameStart() )
        gameLayout.addWidget( btn_start )
        
        btn_end = QPushButton('End')
        btn_end.clicked.connect( lambda : gameEnd() )
        gameLayout.addWidget( btn_end )
        
        btn_jump = QPushButton('Jump')
        btn_jump.clicked.connect( lambda : gameJump() )
        gameControllerLayout.addWidget( btn_jump )
        
        lbl_msg = QLabel('Ready To Start')
        mainLayout.addWidget( lbl_msg )
        
AngryBirdUI('AngryBirdUI')


