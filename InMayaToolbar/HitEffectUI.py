# -*- coding:utf-8 -*- 
from maya.api.OpenMaya import *
from maya.cmds import *
from PySide.QtGui import *
from vic.vicGui import BasicUI
from vic.vicTools import BasicObj
import sys

def doHitEffect( targetNode, hitPositionLocal, hitDirectionLocal, range, power ):
    targetVertexIter = targetNode.getVertexIter()
    while not targetVertexIter.isDone():
        hitPositionLocal = MPoint(hitPositionLocal)
        vertexPositionLocal = targetVertexIter.position()
        subVector = vertexPositionLocal - hitPositionLocal
        subVectorLength = subVector.length()
        if subVectorLength < range:
            factor = subVectorLength / range
            factor = 1 - ((2 * (pow(factor, 2))) - (pow(factor, 8)))
            targetVertexIter.setPosition(MPoint(hitDirectionLocal * factor * power + MVector(vertexPositionLocal)))
        targetVertexIter.next()
    targetVertexIter.updateSurface()

def doIt(targetName, hitFromName, hitTargetName, range, power):
    targetNode = BasicObj( targetName )
    hitFromNodes = [BasicObj( hitFromName )]
    hitTargetNodes = [BasicObj( hitTargetName )]
    
    hitFromLocal = [hitFrom.getPositionAsPoint() * targetNode.getMatrix().inverse() for hitFrom in hitFromNodes ]
    hitDirectLocal = [((hitTarget.getPositionAsPoint() * targetNode.getMatrix().inverse()) - hitFromLocal[i]).normalize() for i, hitTarget in enumerate(hitTargetNodes) ]
    
    for i, hitFrom in enumerate( hitFromLocal ):
        hitDirect = hitDirectLocal[i]
        hitPoint, hitRayParam, hitFace, hitTriangle, hitBary1, hitBary2 = targetNode.rayCast(hitFrom, hitDirect)
        if hitFace != -1:
            doHitEffect( targetNode, hitPoint, hitDirect, range, power )
           
class HitMeshEffectUI(BasicUI):
    
    def addOneRow(self, parentLayout, name, inputs, btns ):
        horiLayout = QHBoxLayout()
        parentLayout.addLayout( horiLayout )
        
        label = QLabel(name)
        label.setMinimumSize( 50, 0 )
        horiLayout.addWidget( label )
        
        input = QLineEdit()
        input.setMinimumSize( 130, 0 )
        horiLayout.addWidget( input )
        inputs.append( input )
        
        btn_pick = QPushButton('Pick')
        horiLayout.addWidget( btn_pick )
        btns.append( btn_pick )
        
    def addOneParam(self, parentLayout, name, max, min, value, params):
        horiLayout = QHBoxLayout()
        parentLayout.addLayout( horiLayout )
        
        label = QLabel(name)
        horiLayout.addWidget( label )
        
        slider_range = QDoubleSpinBox()
        slider_range.setMaximum( max )
        slider_range.setMinimum( min )
        slider_range.setValue(value)
        slider_range.setSingleStep(.1)
        horiLayout.addWidget( slider_range )
        
        params.append( slider_range )
    
    def _showWindow( self, uiName ):
        BasicUI._showWindow(self, uiName )
        
        btns = []
        inputs = []
        params = []
        
        mainLayout = QVBoxLayout(self.getMainWidget())
        
        selectGroup = QGroupBox('Selection')
        selectGroupLayout = QVBoxLayout()
        selectGroup.setLayout( selectGroupLayout )
        mainLayout.addWidget( selectGroup )
        
        self.addOneRow( selectGroupLayout, 'Target', inputs, btns )
        self.addOneRow( selectGroupLayout, 'Hit From', inputs, btns )
        self.addOneRow( selectGroupLayout, 'Hit Target', inputs, btns )
        
        def onBtnClick(id):
            sel = ls(sl=True)
            if len(sel) != 1:
                cmds.error( "you only can select only one object" )
            inputs[id].setText( sel[0] )
        
        for i, btn in enumerate( btns ):
            def closure( _i ):
                return lambda : onBtnClick(_i)
            btn.clicked.connect( closure(i) )
        
        paramsGroup = QGroupBox('Params')
        paramsGroupLayout = QVBoxLayout()
        paramsGroup.setLayout( paramsGroupLayout )
        mainLayout.addWidget( paramsGroup )
        
        self.addOneParam( paramsGroupLayout, 'Explode Range', sys.maxint, 0, 1, params )
        self.addOneParam( paramsGroupLayout, 'Explode Depth', sys.maxint, 0, 1, params )
        
        btn_doIt = QPushButton('Do It!')
        btn_doIt.clicked.connect( lambda : doIt( inputs[0].text(), inputs[1].text(), inputs[2].text(), params[0].value(), params[1].value() ))
        mainLayout.addWidget( btn_doIt )
    
HitMeshEffectUI('HitMeshEffectUI')
    
