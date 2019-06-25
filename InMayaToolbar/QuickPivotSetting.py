import maya.cmds as cmds
from vic.vicTools import BasicObj
from maya.api.OpenMaya import *

target = cmds.ls(sl=True)
for name in target:
    
    obj = BasicObj(name)
    cmds.FreezeTransformations()
    
    # also can using: bbox = cmds.exactWorldBoundingBox( name )
    bbox = obj.getBoundingBox()
    
    v1 = MVector(bbox.min)
    v2 = MVector(bbox.max)
    
    # center 
    # v_center = (v1 + v2) / 2 - MVector(0,0,1)
    
    # center bottom
    v_center = MVector((v1.x+v2.x)/2, (v1.y+v2.y)/2, v1.z)
    v_move = v_center - obj.getPosition()
    
    obj.setPosition( v_center )
    
    vertexIter = obj.getVertexIter()
    while not vertexIter.isDone():
        oldPos = vertexIter.position()
        vertexIter.setPosition( oldPos - v_move )
        vertexIter.next()
        
    cmds.CenterPivot()    
    obj.setPosition( MVector())
    cmds.ResetTransformations()
    cmds.DeleteHistory()    
    
    

