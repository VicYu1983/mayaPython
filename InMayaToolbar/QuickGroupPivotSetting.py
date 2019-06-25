import sys
import maya.cmds as cmds
from maya.api.OpenMaya import *

target_child = cmds.ls(sl=True, dag=True, type=['transform'])
v_targets = {}
for child_name in target_child:
    group_name = child_name.split('|')[0]
    if group_name not in v_targets:
        v_targets[group_name] = {'v_min':MVector(sys.maxint,sys.maxint,sys.maxint), 'v_max':-MVector(sys.maxint,sys.maxint,sys.maxint)}
    
    bbox = cmds.exactWorldBoundingBox( child_name )
    
    bbox_min = MVector(bbox[0],bbox[1],bbox[2])
    bbox_max = MVector(bbox[3],bbox[4],bbox[5])    
    
    v_min = v_targets[group_name]['v_min']
    v_max = v_targets[group_name]['v_max']
    
    v_min.x = min( v_min.x, bbox_min.x )
    v_min.y = min( v_min.y, bbox_min.y )
    v_min.z = min( v_min.z, bbox_min.z )    
    
    v_max.x = max( v_max.x, bbox_max.x )
    v_max.y = max( v_max.y, bbox_max.y )
    v_max.z = max( v_max.z, bbox_max.z )    

for group_name in v_targets:
    v_min = v_targets[group_name]['v_min']
    v_max = v_targets[group_name]['v_max']    
    v_targets[group_name]['v_target'] =  MVector((v_min.x+v_max.x)/2, (v_min.y+v_max.y)/2, v_min.z)

target = cmds.ls(sl=True)
for name in target:
    obj_pos = MVector(cmds.getAttr('%s.translate' % name )[0])
    v_target = v_targets[group_name]['v_target']
    v_move = v_target - obj_pos
    
    cmds.select( name )
    cmds.move( *v_target, ls=1 )
    
    for child_name in target_child:
        inGroup = child_name.find( name ) != -1
        if inGroup:         
            child_old_pos = MVector(cmds.getAttr('%s.translate' % child_name )[0])
            cmds.select( child_name )
            cmds.move( *(child_old_pos - v_move), ls=1 )

cmds.select(cl=1)        
for name in target:
    cmds.select( name, add=1 )
cmds.move(0,0,0)    
cmds.FreezeTransformations()
cmds.ResetTransformations()

    

    
    

