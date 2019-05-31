# -*- coding: utf-8 -*-
from vic.vicGui import BasicUI
from PySide.QtGui import *
import maya.OpenMayaUI as mui
import json


class BatchExportFBXUI( BasicUI ):
    def openPathDialog(self, do):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.DirectoryOnly)
        if dlg.exec_():
            do(dlg.selectedFiles()[0])
    def _showWindow( self, uiName ):
        BasicUI._showWindow( self, uiName )  
        
        def onBtnSetFromClick():
            self.openPathDialog(lambda path: lbl_setFrom.setText(path))
            
        def onBtnSetToClick():
            self.openPathDialog(lambda path: lbl_setTo.setText(path))
        
        verticalLayout = QVBoxLayout(self.getMainWidget())
        
        horiLayout = QHBoxLayout()
        verticalLayout.addLayout( horiLayout )
        btn_setFrom = QPushButton('From Path')
        btn_setFrom.setMinimumSize(80,0)        
        btn_setFrom.clicked.connect( onBtnSetFromClick )        
        horiLayout.addWidget( btn_setFrom )
        
        fromText = 'D:/Vic/Works/GJ/Maya' if self.isDebug() else 'From:'
        lbl_setFrom = QLabel(fromText )       
        lbl_setFrom.setMinimumSize(200,0)                
        horiLayout.addWidget( lbl_setFrom )
        
        horiLayout = QHBoxLayout()    
        verticalLayout.addLayout( horiLayout )           
        btn_setTo = QPushButton('To Path')
        btn_setTo.setMinimumSize(80,0)              
        btn_setTo.clicked.connect( onBtnSetToClick )        
        horiLayout.addWidget( btn_setTo )
        
        toText = 'D:/Vic/Works/GJ/FBX_maya' if self.isDebug() else 'To:'
        lbl_setTo = QLabel(toText)
        lbl_setTo.setMinimumSize(200,0)                        
        horiLayout.addWidget( lbl_setTo )        

        def onBtnExecuteClick():
            fromPath = lbl_setFrom.text()
            toPath = lbl_setTo.text()
            if fromPath != 'From:' and toPath != 'To:':
                print("start export!");
                cmds.BatchExportFBX(json.dumps([fromPath, toPath]))
                print("complete!");
            
        btn_execute = QPushButton('Execute!')
        btn_execute.clicked.connect( onBtnExecuteClick )
        verticalLayout.addWidget( btn_execute )
        
BatchExportFBXUI( 'BatchExportFBX', 'BatchExportFBX.py', True)


