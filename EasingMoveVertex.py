# -*- coding: utf-8 -*-
import maya.api.OpenMaya as om
import maya.cmds as cmds
import sys

def maya_useNewAPI():
    pass

registerId = -1
tempData = []

def doOneObj(obj):
    currentObj = obj['target']
    dagPath = obj['dagPath']
    vertexTarget = obj['vertexTarget']
    vertexCurrent = obj['vertexCurrent']
    vertexTargetNormalized = obj['vertexTargetNormalized']
    previousLocation = obj['previousLocation']

    objTransform = om.MFnTransform(dagPath.transform())
    objMatrix = objTransform.transformation().asMatrix()
    objMatrixInv = objMatrix.inverse()

    currentLocation = objTransform.translation(om.MSpace.kTransform )
    velocity = currentLocation - previousLocation
    obj['previousLocation'] = currentLocation

    vertexIter = om.MItMeshVertex(currentObj)
    while not vertexIter.isDone():
        vertId = vertexIter.index()
        vtxTargetPos = vertexTarget[vertId]
        vtxTargetPosNormalized = vertexTargetNormalized[vertId]
        vtxCurrentPos = vertexCurrent[vertId] * objMatrixInv
        diffVector = vtxTargetPos - vtxCurrentPos

        # 利用每個頂點到物件的坐標向量計算和前進方向的重合程度，越重合力量越大，結果為-1~1
        faceAlongVelocity = vtxTargetPosNormalized * velocity.normalize()
        # 把上述結果轉爲0~1
        faceAlongVelocity += 1
        faceAlongVelocity /= 2
        # 計算力道
        easingForce = faceAlongVelocity * .8 + .2

        # 如果距離差距過小，直接定位，不計算
        if diffVector.length() < .005:
            vtxCurrentPos.x = vtxTargetPos.x
            vtxCurrentPos.y = vtxTargetPos.y
            vtxCurrentPos.z = vtxTargetPos.z
        else:
            vtxCurrentPos += diffVector * easingForce
        vertexCurrent[vertId] = vtxCurrentPos * objMatrix
        vertexIter.setPosition( vtxCurrentPos )
        vertexIter.updateSurface()
        vertexIter.next()

def doEffect():  
    global registerId, tempData     
     
    def onTimeUpdate(*args):
        for obj in tempData:
            doOneObj( obj )

    if registerId == -1:
        registerId = om.MDGMessage.addTimeChangeCallback(onTimeUpdate)
    
    selectList = om.MGlobal.getActiveSelectionList()
    geoList = om.MItSelectionList(selectList, om.MFn.kGeometric)

    while not geoList.isDone():
        currentObj = geoList.getDependNode()
        dagPath = geoList.getDagPath()
        objTransform = om.MFnTransform(dagPath.transform())
        objData = {
            # 原來的頂點位置(local)
            'vertexTarget':[],
            # 假定的頂點位置(global)
            'vertexCurrent':[],
            # 把頂點的位置做單位向量后快取起來(local)
            'vertexTargetNormalized':[],
            # 目標物件
            'target':currentObj,
            # 目標物件的transform等資料
            'dagPath':dagPath,
            # 目標物件的上一個frame的位置，用來計算速度
            'previousLocation':objTransform.translation(om.MSpace.kTransform)
        }
        tempData.append(objData)
        vertexIter = om.MItMeshVertex(currentObj)
        while not vertexIter.isDone():
            objData['vertexTarget'].append(vertexIter.position())
            objData['vertexTargetNormalized'].append(om.MVector( vertexIter.position()).normalize())
            objData['vertexCurrent'].append(vertexIter.position())
            vertexIter.next()
        geoList.next()

def resetVertex():
    selectList = om.MGlobal.getActiveSelectionList()
    geoList = om.MItSelectionList(selectList, om.MFn.kGeometric)

    while not geoList.isDone():
        needResetObj = geoList.getDependNode()
        for obj in tempData:
            currentObj = obj['target']
            if needResetObj == currentObj:
                vertexTarget = obj['vertexTarget']
                vertexIter = om.MItMeshVertex(currentObj)
                while not vertexIter.isDone():
                    vertId = vertexIter.index()
                    vertexIter.setPosition( vertexTarget[vertId] )
                    vertexIter.next()
        geoList.next()                

def clearEffect():
    selectList = om.MGlobal.getActiveSelectionList()
    geoList = om.MItSelectionList(selectList, om.MFn.kGeometric)

    while not geoList.isDone():
        needDeleteObj = geoList.getDependNode()
        for obj in tempData:
            currentObj = obj['target']
            if needDeleteObj == currentObj:
                tempData.remove(obj)
        geoList.next()

class EasingMoveVertex(om.MPxCommand):
    kPluginCmdName = 'EasingMoveVertex'

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return EasingMoveVertex()

    def doIt(self, args):
        doEffect()

class EasingMoveVertexReset(om.MPxCommand):
    kPluginCmdName = 'EasingMoveVertexReset'

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return EasingMoveVertexReset()

    def doIt(self, args):
        resetVertex() 

class EasingMoveVertexClear(om.MPxCommand):
    kPluginCmdName = 'EasingMoveVertexClear'

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return EasingMoveVertexClear()

    def doIt(self, args):
        clearEffect()                    

def initializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.registerCommand(
            EasingMoveVertex.kPluginCmdName, EasingMoveVertex.cmdCreator
        )
        pluginFn.registerCommand(
            EasingMoveVertexReset.kPluginCmdName, EasingMoveVertexReset.cmdCreator
        )
        pluginFn.registerCommand(
            EasingMoveVertexClear.kPluginCmdName, EasingMoveVertexClear.cmdCreator
        )
    except:
        sys.stderr.write(
            "Failed to register command: %s\n" % EasingMoveVertex.kPluginCmdName
        )
        raise

def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        if registerId != -1:
            om.MMessage.removeCallback(registerId)
        pluginFn.deregisterCommand(EasingMoveVertex.kPluginCmdName) 
        pluginFn.deregisterCommand(EasingMoveVertexReset.kPluginCmdName) 
        pluginFn.deregisterCommand(EasingMoveVertexClear.kPluginCmdName) 
    except:
        sys.stderr.write(
            "Failed to unregister command: %s\n" % EasingMoveVertex.kPluginCmdName
        )