from PySide.QtGui import *
import maya.OpenMayaUI as mui
import maya.api.OpenMaya as om
import shiboken
import re
import json

# 讀取外挂
def loadTransferVertexOrdersPlugin():
    plugInFile = 'TransferVertexOrders.py'
    maya.cmds.unloadPlugin(plugInFile)
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
    
def addOneRow( parentLayout, labelName, txt_pickNames, btn_adds, btn_subs, btn_clears ):
    horizontalLayout = QHBoxLayout()
    parentLayout.addLayout( horizontalLayout )
    
    label = QLabel( labelName )
    label.setMinimumSize( 40, 0 )
    horizontalLayout.addWidget( label )
    
    lineEdit = QLineEdit()
    lineEdit.setMinimumSize( 150, 0 )
    horizontalLayout.addWidget( lineEdit )
    
    btn_add = QPushButton('Add')
    horizontalLayout.addWidget( btn_add )  
    
    btn_sub = QPushButton('Sub')
    horizontalLayout.addWidget( btn_sub ) 
    
    btn_clear = QPushButton('Clear')
    horizontalLayout.addWidget( btn_clear ) 
    
    txt_pickNames.append( lineEdit ) 
    btn_adds.append( btn_add )
    btn_subs.append( btn_sub )
    btn_clears.append( btn_clear )
    
def addOneGroup(parentLayout, groupName, txt_pickNames, btn_adds, btn_subs, btn_clears):
    groupBox = QGroupBox(groupName)
    groupBoxLayout = QVBoxLayout()
    groupBox.setLayout( groupBoxLayout )
    parentLayout.addWidget( groupBox )
    
    addOneRow( groupBoxLayout, 'Face', txt_pickNames, btn_adds, btn_subs, btn_clears )
    addOneRow( groupBoxLayout, 'VertA', txt_pickNames, btn_adds, btn_subs, btn_clears )
    addOneRow( groupBoxLayout, 'VertB', txt_pickNames, btn_adds, btn_subs, btn_clears )  
    
# 把選取到的點或者面取出資料    
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
    # 從UI中取出參數
    passValue = []
    for i, ary in enumerate( inputValues ):
        passValue.append([])
        for elem in ary:
            info = filterInfoFromValue( elem )    
            if info is not None:
                passValue[i].append(int(info['id']))
                
    # 帶入要執行的物件名稱
    passValue.append( inputValues[0][0].split('.')[0] )   
    passValue.append( inputValues[3][0].split('.')[0] )
    
    # translate to json str
    passStr = json.dumps( passValue )
    
    # 呼叫外挂      
    maya.cmds.TransferVertexOrders(passStr) 
      
    bar.reset()    
    
windowName = 'TranferVertexOrders'
if cmds.window( windowName, exists=True):
    cmds.deleteUI( windowName, wnd=True )
    
loadTransferVertexOrdersPlugin()     

# 注冊事件，更新及完成事件
om.MUserEventMessage.addUserEventCallback('onTransferVertexOrdersUpdate', onTransferVertexOrdersUpdateMethod) 
om.MUserEventMessage.addUserEventCallback('onTransferVertexOrdersDone', onTransferVertexOrdersDoneMethod)      
    
window = QMainWindow(getMayaWindow())
window.setObjectName( windowName )
window.setWindowTitle( windowName )
window.show()

mainWidget = QWidget()
window.setCentralWidget( mainWidget )

verticalLayout = QVBoxLayout(mainWidget)

txt_pickNames = []
btn_adds = []
btn_subs = []
btn_clears = []
inputValues = [[], [], [], [], [], []]

addOneGroup( verticalLayout, 'From Mesh', txt_pickNames, btn_adds, btn_subs, btn_clears )
addOneGroup( verticalLayout, 'To Mesh', txt_pickNames, btn_adds, btn_subs, btn_clears )

# handle add buttons
def onBtnAddClick( index, target ):
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
            
    inputValues[index].append( selstr )  
    targetText.setText( str(inputValues[index]) )

for i, btn in enumerate( btn_adds ):
    def onClick(index, target):
        def insideClick():
            onBtnAddClick(index, target )
        return insideClick
    btn.clicked.connect( onClick(i, btn) )
    
# handle sub buttons    
def onBtnSubClick( index, target ):
    targetText = txt_pickNames[index]
    if len( inputValues[index] ) > 0:
        inputValues[index].pop()
    if len( inputValues[index] ) == 0:
        targetText.setText('')
    else:
        targetText.setText( str(inputValues[index]) )

for i, btn in enumerate( btn_subs ):
    def onClick(index, target):
        def insideClick():
            onBtnSubClick(index, target )
        return insideClick
    btn.clicked.connect( onClick(i, btn) ) 

# handle clear buttons
def onBtnClearClick( index, target ):
    targetText = txt_pickNames[index]
    while( len( inputValues[index] ) > 0 ):
        inputValues[index].pop()
    targetText.setText('') 

for i, btn in enumerate( btn_clears ):
    def onClick(index, target):
        def insideClick():
            onBtnClearClick(index, target )
        return insideClick
    btn.clicked.connect( onClick(i, btn) )        
    
# 執行按鈕   
btn_doIt = QPushButton('Do It!')
btn_doIt.clicked.connect( doIt )
verticalLayout.addWidget( btn_doIt )

# 讀取條，執行時才會出現
bar = QProgressBar()
bar.setVisible(False)
verticalLayout.addWidget(bar)  

# 狀態説明
barLabel = QLabel('Prepare For Work')
verticalLayout.addWidget(barLabel)  
        








