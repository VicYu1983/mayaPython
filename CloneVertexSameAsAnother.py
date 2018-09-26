import maya.OpenMaya as om



    
    #print geo1MeshInfo['triangles'][0]
    
    #geo2SeamVerts = getSeamVertsOn(selectionList, 2)

    #pairedVertsDict = pairSeamVerts(geo1SeamVerts, geo2SeamVerts)

def getVertexInfo(objectList, objectNumber):
    
    vertexInfo = {}
    vertexInfo['locations'] = []
    #vertexInfo['triangles'] = []
    
    def doPerVertex( vertexIter ):
        vertex = vertexIter.position()
        #vid = vertexIter.index()
        #connectedVerts = om.MIntArray()
        #vertexIter.getConnectedVertices(connectedVerts)
        #vertexInfo['triangles'].append( connectedVerts )
        vertexInfo['locations'].append( vertex )
        
    loopVertexAndDo( objectList, objectNumber, doPerVertex )   
    return vertexInfo
            
def printPoint( position ):
    print 'location:' + str(position[0]) + ' ' + str(position[1]) + ' ' + str(position[2])    
'''    
def findThirdPointByTwoVertex( tri1, loc2, vid1, vid2, fixedArray ):
    
    print( tri1[vid1] )
    print( tri1[vid2] )
    
    vertex1Conntext = tri1[vid1];
    vertex2Conntext = tri1[vid2];
    
    for v in vertex1Conntext:
        if v in vertex2Conntext and not str(v) in fixedArray:
            fixedArray[v] = loc2[v]
            print 'save: ' + str(v)
            
def makeOneVertexLocationSameAnotherOne(meshInfo1, meshInfo2): 
    locations1 = meshInfo1['locations']
    locations2 = meshInfo2['locations']
    
    tri1 = meshInfo1['triangles']
    tri2 = meshInfo2['triangles']
    
    fixedArray = {}
    fixedArray['4'] = locations2[7]
    findThirdPointByTwoVertex( tri1, locations2, 2, 6, fixedArray )
'''   
def loopVertexAndDo( objectList, objectNumber, method ):
    count = 0
    selectedObject = om.MObject()
    iter = om.MItSelectionList(objectList, om.MFn.kGeometric)
    while not iter.isDone():
        count += 1
        connectedVerts = om.MIntArray()
        if (count != objectNumber):
            iter.next()
        else:
            iter.getDependNode(selectedObject)
            vertexIter = om.MItMeshVertex(selectedObject)
            while not vertexIter.isDone():
                method( vertexIter )
                vertexIter.next()
                
def loopFacesAndDo( objectList, objectNumber, method ):
    count = 0
    selectedObject = om.MObject()
    iter = om.MItSelectionList(objectList, om.MFn.kGeometric)
    while not iter.isDone():
        count += 1
        connectedVerts = om.MIntArray()
        if (count != objectNumber):
            iter.next()
        else:
            iter.getDependNode(selectedObject)
            faceItor = om.MItMeshFaceVertex(selectedObject)
            while not faceItor.isDone():
                method( faceItor )
                faceItor.next()
                
def getFacesInfo(objectList, objectNumber):
    meshInfo = []
    def saveFaces(faceIter):
        vertId = faceIter.vertId()
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
         
    print 'get new assign:' + str( newAssign )      
    return newAssign
           
    
def loopFaceAndCurrectPosition(faceInfo, needFixFace, needFixVertex, targetFaceId, assign):
    face = faceInfo[targetFaceId]
    
    if targetFaceId not in needFixFace:
        needFixFace.append( targetFaceId )
    else:
        print 'faceId: %s fixed!' % str(targetFaceId)
        return
    
    print 'faceId: %s processing' % str(targetFaceId)
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
        print 'next faced: %s' % str( findFaces )
        for f in findFaces:
            newAssign = findNextFaceAssign( faceInfo, f, [v1, v2] )
            loopFaceAndCurrectPosition( faceInfo, needFixFace, needFixVertex, f, newAssign )
                    
geo1Verts = om.MFloatPointArray()
geo2Verts = om.MFloatPointArray()

selectionList = om.MSelectionList()
om.MGlobal.getActiveSelectionList(selectionList)

faceInfo = getFacesInfo( selectionList, 1 )
print faceInfo

faceInfo2 = getFacesInfo( selectionList, 2 )
print faceInfo2

vertexInfo2 = getVertexInfo( selectionList, 2 )
print vertexInfo2['locations'][0]

print '-------------------AAA start-------------'

needFixFace = []
needFixVertex = []
loopFaceAndCurrectPosition( faceInfo, needFixFace, needFixVertex, 1, [5, 4] )

print '-------------------BBB start-------------'

needFixFace2 = []
needFixVertex2 = []
loopFaceAndCurrectPosition( faceInfo2, needFixFace2, needFixVertex2, 2, [4, 0] )

print needFixFace
print needFixFace2
print needFixVertex
print needFixVertex2


def setPosition( vertexIter ):
    mapIndex = needFixVertex.index( vertexIter.index() )
    targetIndex = needFixVertex2[mapIndex]
    vertexIter.setPosition( vertexInfo2['locations'][targetIndex] )
    
loopVertexAndDo( selectionList, 1, setPosition )




#print needFixFace

#makeOneVertexLocationSameAnotherOne( geo1MeshInfo, geo1MeshInfo2 )