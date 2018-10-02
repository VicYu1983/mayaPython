# -*- coding: utf-8 -*-
from PySide.QtGui import *
import maya.OpenMayaUI as mui
import maya.api.OpenMaya as om
import shiboken

# 讀取外挂
def loadTransferVertexOrdersPlugin():
    plugInFile = 'EasingMoveVertex.py'
    maya.cmds.loadPlugin(plugInFile)    

# 監聽TransferVertexOrders.py的事件，更新進度條
def onTransferVertexOrdersUpdateMethod(percentage):
    if not bar.isVisible():
        bar.setVisible(True)
    barLabel.setText('Please Wait...')
    bar.setValue(int(percentage))
    
# 監聽TransferVertexOrders.py的事件，顯示完成   
def onTransferVertexOrdersDoneMethod(evt): 
    barLabel.setText('Done And Prepare For New One')  

# 取得maya本身的視窗
def getMayaWindow():
    pointer = mui.MQtUtil.mainWindow()
    return shiboken.wrapInstance( long( pointer ), QWidget )
    
windowName = 'EasingMoveVertex'
if cmds.window( windowName, exists=True):
    cmds.deleteUI( windowName, wnd=True )
    
loadTransferVertexOrdersPlugin()       
    
window = QMainWindow(getMayaWindow())
window.setObjectName( windowName )
window.setWindowTitle( windowName )
window.show()

mainWidget = QWidget()
window.setCentralWidget( mainWidget )

verticalLayout = QVBoxLayout(mainWidget)

groupBox = QGroupBox('EasingMoveVertex')
groupBoxLayout = QVBoxLayout()
groupBox.setLayout( groupBoxLayout )
verticalLayout.addWidget( groupBox )

def onBtnAddEffectClick():
    maya.cmds.EasingMoveVertex()
    
def onBtnClearEffectClick():
    if chk_alsoReset.isChecked():
        onBtnResetEffectClick()
    maya.cmds.EasingMoveVertexClear()       
    
def onBtnResetEffectClick():
    maya.cmds.EasingMoveVertexReset()      

btn_addEffect = QPushButton('Add Effect')
btn_addEffect.clicked.connect( onBtnAddEffectClick )
groupBoxLayout.addWidget( btn_addEffect )

btn_resetEffect = QPushButton('Reset Effect')
btn_resetEffect.clicked.connect( onBtnResetEffectClick )
groupBoxLayout.addWidget( btn_resetEffect )

horizontalLayout = QHBoxLayout()
groupBoxLayout.addLayout( horizontalLayout )

chk_alsoReset = QCheckBox('Also Reset')
horizontalLayout.addWidget( chk_alsoReset ) 

btn_clearEffect = QPushButton('Clear Effect')
btn_clearEffect.clicked.connect( onBtnClearEffectClick )
horizontalLayout.addWidget( btn_clearEffect )
