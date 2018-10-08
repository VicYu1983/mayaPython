from PySide.QtGui import *
import maya.cmds as cmds
import maya.OpenMayaUI as mui
import shiboken

class BasicUI():
    def __init__(self, uiName, pluginName = '', debug = False):
        if pluginName is not '':
            self.__loadPlugin( pluginName, debug )
        self._showWindow( uiName)
        
    def __loadPlugin( self, pluginName , debug = False ):
        if debug:
            cmds.unloadPlugin( pluginName )
        cmds.loadPlugin( pluginName )
        
    def __getMayaWindow(self):
        pointer = mui.MQtUtil.mainWindow()
        return shiboken.wrapInstance( long( pointer ), QWidget )
        
    def _showWindow( self, pluginName):
        if cmds.window( pluginName, exists=True):
            cmds.deleteUI( pluginName, wnd=True )
            
        self.__window = QMainWindow(self.__getMayaWindow())
        self.__window.setObjectName( pluginName )
        self.__window.setWindowTitle( pluginName )
        
        self.__mainWidget = QWidget()
        self.__window.setCentralWidget( self.__mainWidget )
        
        self.__window.show()
        
    def getMainWidget(self):
        return self.__mainWidget   
        

        