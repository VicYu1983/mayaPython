# coding=UTF-8
import maya.cmds as cmds
import maya.api.OpenMaya as om

# 射綫和平面的碰撞檢測
def ray_plane_intersect(plane_normal, plane_a, ray_start, ray_end):
    t = plane_normal * (plane_a-ray_start) / (plane_normal * (ray_end-ray_start))
    return ray_start + t * (ray_end-ray_start)

# 取得選擇的物件
list = cmds.ls(sl=1)
maxLength = 0
plane_a = ''
plane_b = ''

# 把up點先取出來
up_point = om.MVector(cmds.getAttr('%s.translate' % list[len(list)-1])[0])
list.pop()

# 取出最遠的兩個點來當成平面的兩個點
for i in range(0, len(list)):
    for j in range(i+1, len(list)):
        o1 = list[i]
        o2 = list[j]
        v1 = om.MVector(cmds.getAttr('%s.translate' % o1)[0])
        v2 = om.MVector(cmds.getAttr('%s.translate' % o2)[0])
        dist = ( v2 - v1 ).length()
        if dist > maxLength:
            maxLength = dist
            plane_a = v1
            plane_b = v2

# 取得up
up_vector = (up_point - plane_a).normalize()
            
# 取得平面的法向量
plane_normal = ((plane_b - plane_a) ^ up_vector).normalize()

# 把所有的點投影到平面
for obj in list:
    v = om.MVector(cmds.getAttr('%s.translate' % obj)[0])
    ray_start = v
    ray_end = v + plane_normal
    hit_pos = ray_plane_intersect(plane_normal, plane_a, ray_start, ray_end )
    cmds.setAttr('%s.translate' % obj, *hit_pos )
