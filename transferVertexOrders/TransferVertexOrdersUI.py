from PySide.QtGui import *
import maya.OpenMayaUI as mui
import shiboken
import re

def getMayaWindow():
    pointer = mui.MQtUtil.mainWindow()
    return shiboken.wrapInstance( long( pointer ), QWidget )
    
def addOneRow( parentLayout, labelName, txt_pickNames, btn_picks ):
    horizontalLayout = QHBoxLayout()
    parentLayout.addLayout( horizontalLayout )
    
    label = QLabel( labelName )
    label.setMinimumSize( 40, 0 )
    horizontalLayout.addWidget( label )
    lineEdit = QLineEdit()
    lineEdit.setMinimumSize( 150, 0 )

    horizontalLayout.addWidget( lineEdit )
    btn_choose = QPushButton('Pick')
    horizontalLayout.addWidget( btn_choose )  
    
    txt_pickNames.append( lineEdit ) 
    btn_picks.append( btn_choose )
    
def addOneGroup(parentLayout, groupName, txt_pickNames, btn_picks):
    groupBox = QGroupBox(groupName)
    groupBoxLayout = QVBoxLayout()
    groupBox.setLayout( groupBoxLayout )
    parentLayout.addWidget( groupBox )
    
    addOneRow( groupBoxLayout, 'Face', txt_pickNames, btn_picks )
    addOneRow( groupBoxLayout, 'VertA', txt_pickNames, btn_picks )
    addOneRow( groupBoxLayout, 'VertB', txt_pickNames, btn_picks )  
    
def filterInfoFromValue( str ):
    regex = r"([a-zA-z]*[\d]*)[.]([a-zA-Z]*)[[](\d*)[]]"
    matches = re.search(regex, str, re.MULTILINE)  
    
    matchValue = []
    if matches:
        for groupNum in range(0, len(matches.groups())):
            groupNum = groupNum + 1
            matchValue.append( matches.group(groupNum ) )
            
    if len( matchValue ) > 0:
        objName = matchValue[0]       
        isVertex = matchValue[1] == 'vtx'
        id = matchValue[2]
        return {'objName':objName, 'isVertex':isVertex, 'id':id}
    else:
        return None
    
def doIt():
    plugInFile = 'TransferVertexOrders.py'
    maya.cmds.unloadPlugin(plugInFile)
    maya.cmds.loadPlugin(plugInFile)
    
    passValue = []
    for txt in txt_pickNames:
        valueStr = txt.text();
        info = filterInfoFromValue( valueStr )    
        if info is not None:
            passValue.append(info['id'])
    if len( passValue ) < 6:
        cmds.error( "values is not enough!" )
        return
    passValue.append( txt_pickNames[0].text().split('.')[0] )   
    passValue.append( txt_pickNames[3].text().split('.')[0] )          
    maya.cmds.TransferVertexOrders(passValue)          

windowName = 'TranferVertexOrders'

if cmds.window( windowName, exists=True):
    cmds.deleteUI( windowName, wnd=True )
    
window = QMainWindow(getMayaWindow())
window.setObjectName( windowName )
window.setWindowTitle( windowName )
window.show()

mainWidget = QWidget()
window.setCentralWidget( mainWidget )

verticalLayout = QVBoxLayout(mainWidget)

txt_pickNames = []
btn_picks = []

addOneGroup( verticalLayout, 'From Mesh', txt_pickNames, btn_picks )
addOneGroup( verticalLayout, 'To Mesh', txt_pickNames, btn_picks )

def onBtnClick( index, target ):
    targetText = txt_pickNames[index]
    sel = cmds.ls(sl=True)
    if len( sel ) != 1:
        cmds.error( "you only can select only one vertex of face" )
    selstr = str(sel[0])
    info = filterInfoFromValue( selstr ) 
    if index == 0 or index == 3:
        if info['isVertex']:
            cmds.error( "you should select face, not vertex" ) 
    else:
        if not info['isVertex']:
            cmds.error( "you should select vertex, not face" ) 
    targetText.setText( selstr )

for i, btn in enumerate( btn_picks ):
    def onClick(index, target):
        def insideClick():
            onBtnClick(index, target )
        return insideClick
    btn.clicked.connect( onClick(i, btn) )

btn_doIt = QPushButton('Do It!')
btn_doIt.clicked.connect( doIt )
verticalLayout.addWidget( btn_doIt )






