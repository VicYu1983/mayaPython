# -*- coding: utf-8 -*-
import os,sys
import maya.cmds as cmds
import maya.mel as mel
import shutil

def Install(ToolRoot):
	usd = cmds.internalVar(usd=True)
	usrFold = usd[:-8]
	usrPlugFold = usrFold+"plugins/"
	usrScrptFold = usrFold+"scripts/"
	usrImgFold = usrFold+"prefs/icons/"

	g_ShelfTopLevel = mel.eval("$Temp = $gShelfTopLevel") # 取得maya global: gShelfTopLevel
	if cmds.tabLayout(g_ShelfTopLevel, q = True, ex = True):
		_tab = cmds.tabLayout(g_ShelfTopLevel,q=True,st=True)
		shelfButtons = cmds.shelfLayout(_tab , q=True, ca=True )
		
		if(shelfButtons):
			for btn in shelfButtons:
				if(cmds.control(btn,ex=True)):
					sfbtn = cmds.shelfButton(btn,q=True,annotation=True)
					if( sfbtn == "Open JFDestructionSkin" ):
						cmds.deleteUI(btn)
		JFAnmToolsPth = ToolRoot + '/JFDestructionSkin.mel'
		melCommand = 'source "' + JFAnmToolsPth + '";'
		cmds.shelfButton(parent = g_ShelfTopLevel + '|' + _tab ,
			image = 'pythonFamily.png',
			iol = 'JFDestructionSkin',
			label = 'JFDestructionSkin',
			sourceType = 'mel',
			annotation = 'Open JFDestructionSkin',
			command = melCommand
			)
	else:
		error('Must have active shelf to create shelf button')
