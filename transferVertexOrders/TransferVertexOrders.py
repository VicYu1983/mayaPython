import maya.api.OpenMaya as om
import sys

sys.setrecursionlimit(2000)
debugLog = False

def getVertexInfo(objectList, objectNumber):
    vertexInfo = {}
    vertexInfo['locations'] = []
    def doPerVertex( vertexIter ):
        vertex = vertexIter.position()
        vertexInfo['locations'].append( vertex )
        
    loopVertexAndDo( objectList, objectNumber, doPerVertex )   
    return vertexInfo
            
def printPoint( position ):
    if debugLog:
        print 'location:' + str(position[0]) + ' ' + str(position[1]) + ' ' + str(position[2])    

def loopVertexAndDo( objectList, objectNumber, method ):
    count = 0
    iter = om.MItSelectionList(objectList, om.MFn.kGeometric)
    while not iter.isDone():
        count += 1
        connectedVerts = om.MIntArray()
        if (count != objectNumber):
            iter.next()
        else:
            selectedObject = iter.getDependNode()
            vertexIter = om.MItMeshVertex(selectedObject)
            while not vertexIter.isDone():
                method( vertexIter )
                vertexIter.next()
                
def loopFacesAndDo( objectList, objectNumber, method ):
    count = 0
    iter = om.MItSelectionList(objectList, om.MFn.kGeometric)
    while not iter.isDone():
        count += 1
        connectedVerts = om.MIntArray()
        if (count != objectNumber):
            iter.next()
        else:
            selectedObject = iter.getDependNode()
            faceItor = om.MItMeshFaceVertex(selectedObject)
            while not faceItor.isDone():
                method( faceItor )
                faceItor.next()
                
def getFacesInfo(objectList, objectNumber):
    meshInfo = []
    def saveFaces(faceIter):
        vertId = faceIter.vertexId()
        faceId = faceIter.faceId()
        try:
            meshInfo[faceIter.faceId()]
        except:
            meshInfo.append([])
        meshInfo[faceId].append(vertId)
    loopFacesAndDo( objectList, objectNumber, saveFaces )    
    return meshInfo    
    
def findFaceIdByVertice( faceInfo, vertice ):
    findFaces = []
    for i, f in enumerate(faceInfo):
        inFace = True
        for v in vertice:
            if v not in f:
                inFace = False
        if inFace:
            findFaces.append(i)
    return findFaces      
    
def findNextFaceAssign(faceInfo, faceId, assign):
    face = faceInfo[faceId]
    newAssign = []
    if debugLog:
        print 'current vertex of face:' + str(face)    
    for i, vertexId in enumerate( face ):
        if i == 0:
            v0 = face[len(face) - 1]
        else:
            v0 = face[i - 1]
        v1 = face[i]
        if i == len(face) - 1:
            v2 = face[0]
        else:
            v2 = face[i+1]
        if v0 in assign and v1 in assign and v1 is assign[0]:
            newAssign = [v1, v2]
            break
        if v1 in assign and v2 in assign and v1 is assign[0]:
            newAssign = [v0, v1]   
            break
    if debugLog:
        print 'get new assign:' + str( newAssign )      
    return newAssign
           
    
def loopFaceAndCurrectPosition(faceInfo, needFixFace, needFixVertex, targetFaceId, assign):
    face = faceInfo[targetFaceId]
    
    if targetFaceId not in needFixFace:
        needFixFace.append( targetFaceId )
    else:
        print 'faceId: %s already processed! skip it.' % str(targetFaceId)
        return
    
    print 'faceId: %s is processing' % str(targetFaceId)
    if debugLog:
        print 'assign: %s ' % str( assign )
    
    resortArrayByAssign = []
    newFirst = -1
    for i, vertexId in enumerate( face ):
        v1 = face[i]
        if i == len(face) - 1:
            v2 = face[0]
        else:
            v2 = face[i+1]
        if v1 in assign and v2 in assign:
            newFirst = i-1
            break
    newFirstTemp = newFirst
    while len( resortArrayByAssign ) < len( face ):
        newFirstTemp += 1
        if newFirstTemp > len( face ) - 1:
            newFirstTemp %= len( face )
        resortArrayByAssign.append( face[newFirstTemp] )
            
    if debugLog:
        print 'resortArrayByAssign: %s' % str( resortArrayByAssign )            
    
    for i, vertexId in enumerate( resortArrayByAssign ):
        v1 = resortArrayByAssign[i]
        if i == len(resortArrayByAssign) - 1:
            v2 = resortArrayByAssign[0]
        else:
            v2 = resortArrayByAssign[i+1]
        
        if v1 not in needFixVertex:
            needFixVertex.append( v1 )
        if v2 not in needFixVertex:
            needFixVertex.append( v2 )
        
        findFaces = findFaceIdByVertice( faceInfo, [v1, v2] )
        if debugLog:
            print 'next faced: %s' % str( findFaces )
        for f in findFaces:
            if f not in needFixFace:
                newAssign = findNextFaceAssign( faceInfo, f, [v1, v2] )
                loopFaceAndCurrectPosition( faceInfo, needFixFace, needFixVertex, f, newAssign )
                
def executeCommand():            
    selectionList = om.MGlobal.getActiveSelectionList()
    
    faceInfo = getFacesInfo( selectionList, 1 )
    #print faceInfo
    
    faceInfo2 = getFacesInfo( selectionList, 2 )
    #print faceInfo2
    
    vertexInfo2 = getVertexInfo( selectionList, 2 )
    #print vertexInfo2['locations'][0]
    
    needFixFace = []
    needFixVertex = []
    
    #test cube
    loopFaceAndCurrectPosition( faceInfo, needFixFace, needFixVertex, 1, [5, 4] )
    
    # head model setting
    #loopFaceAndCurrectPosition( faceInfo, needFixFace, needFixVertex, 0, [2, 3] )
    
    needFixFace2 = []
    needFixVertex2 = []
    
    #test cube
    loopFaceAndCurrectPosition( faceInfo2, needFixFace2, needFixVertex2, 2, [4, 0] )
    
    # head model setting
    #loopFaceAndCurrectPosition( faceInfo2, needFixFace2, needFixVertex2, 0, [2, 3] )
    
    if debugLog:
        print needFixFace
        print needFixFace2
        print needFixVertex
        print needFixVertex2
    
    def setPosition( vertexIter ):
        mapIndex = needFixVertex.index( vertexIter.index() )
        targetIndex = needFixVertex2[mapIndex]
        vertexIter.setPosition( vertexInfo2['locations'][targetIndex] )
        
    loopVertexAndDo( selectionList, 1, setPosition )
    
    
    '''
    def setIndex( vertexIter ):
        mapIndex = needFixVertex2.index( vertexIter.index() )
        targetIndex = needFixVertex[mapIndex]
        vertexIter.setIndex(1)
       
    
    loopVertexAndDo( selectionList, 2, setIndex )
    '''
    
executeCommand()    