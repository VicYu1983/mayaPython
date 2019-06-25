# 流程：
# 一、選擇要導出的物件
# 二、freeze transform
# 三、點擊此按鈕
# 四、刪除歷史記錄

import maya.cmds as cmds
from vic.vicTools import BasicObj
from maya.api.OpenMaya import *

# 加入自動freeze后，undo就會變成很奇怪。所以freeze先用手動的方式實現
# cmds.FreezeTransformations()

target = cmds.ls(sl=True)
for name in target:    
    obj = BasicObj(name)
    bbox = obj.getBoundingBox()
    
    v1 = MVector(bbox.min)
    v2 = MVector(bbox.max)
    
    v_center = MVector((v1.x+v2.x)/2, (v1.y+v2.y)/2, v1.z)
    v_move = v_center - obj.getPosition()
    
    obj.setPosition( v_center )
    
    vertexIter = obj.getVertexIter()
    while not vertexIter.isDone():
        oldPos = vertexIter.position()
        vertexIter.setPosition( oldPos - v_move )
        vertexIter.next()
    
cmds.select(cl=1)
for name in target:
    cmds.select( name, add=1 )
cmds.move(0,0,0)    
cmds.ResetTransformations()

    
    

