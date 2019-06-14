import maya.cmds as cmds
import pymel.core as pm

def copyKeys(fromObj, toObj, frameCopyStart = 0, frameCopyEnd = 100):
    cmds.copyKey(fromObj, time=(frameCopyStart, frameCopyEnd))
    cmds.pasteKey(toObj, o='replace', time=(frameCopyStart, frameCopyEnd))
    
def bakeAnimation(fromObj, toObj, frameCopyStart = 0, frameCopyEnd = 100):
    cmds.select(cl=True)
    cmds.select(fromObj)
    cmds.select(toObj, add=True)   
    cmds.parentConstraint(mo=False, weight=1)
    
def createLocator( fromName, pos ):
    locaName = cmds.spaceLocator()
    bakeAnimation( fromName, locaName )
    return locaName[0]


# get selected mesh
objs = cmds.ls(sl=True, o=True)

# collect mesh vertex count
pushObj = []
for obj in objs:
    cmds.select(obj)
    pushObj.append({'name':obj, 'count':cmds.polyEvaluate( v=True )})

# combine all mesh
cmds.select(objs)
cmds.polyUnite(n='result')

# create root bone
rootLocator = cmds.spaceLocator()

# create bone on every mesh position and constraint
locators = []
for obj in objs:
    pos = cmds.getAttr("%s.translate" % obj)
    locators.append( createLocator( obj.__str__(), pos[0] ))

# link all bone to root bone
cmds.select(clear=True)
cmds.select(locators)
cmds.parent( locators, rootLocator )

# bake all bone animation 
cmds.bakeResults( locators,
                    simulation=True,
                    t=(1,120),
                    sampleBy=1,
                    disableImplicitControl=True,
                    preserveOutsideKeys=False,
                    sparseAnimCurveBake=False,
                    removeBakedAttributeFromLayer=False,
                    bakeOnOverrideLayer=False,
                    minimizeRotation=False,
                    at=['tx','ty','tz','rx','ry','rz'] )
                  
# collect all bones and root bone for skin
skinLocators = [rootLocator[0]]
skinLocators.extend( locators )

# select all bones and root bone
cmds.select(cl=True)
cmds.select( skinLocators )

# add select with result mesh
cmds.select('result', add=True)

# skin
cmds.skinCluster(tsb=False,tst=True, bm=0, sm=0, nw=1, wd=0, mi=5, rui=True, ihs=False)

# set skin weight 
vertex_start = 0
vertex_end = 0
for loca, mesh in zip(locators, pushObj):
    vertex_end += mesh['count']
    cmds.skinPercent( 'skinCluster1', 'result.vtx[{}:{}]'.format(vertex_start, vertex_end), transformValue=[(loca, 1)])
    vertex_start += mesh['count']








