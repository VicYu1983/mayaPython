import maya.cmds as cmds

cmds.parentConstraint(mo=False, weight=1)
target = cmds.ls(sl=1)[1].split('|').pop()
cmds.select( '%s_parentConstraint1' % target )
cmds.delete()