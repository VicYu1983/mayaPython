from vicGui import BasicPluginUI
from PySide.QtGui import *

class EasingMoveVertexPlugin( BasicPluginUI ):
    def _showWindow( self, pluginName):
        BasicPluginUI._showWindow( self, pluginName )
        
        verticalLayout = QVBoxLayout(self.getMainWidget())

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
        
EasingMoveVertexPlugin( 'EasingMoveVertex.py' )

