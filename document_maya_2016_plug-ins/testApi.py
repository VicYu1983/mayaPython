import sys
import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya

def maya_useNewAPI():
    pass

kPluginCmdName = 'pyPrintPaths'

class printPathsCmd(OpenMaya.MPxCommand):
    def __init__(self):
        OpenMaya.MPxCommand.__init__(self)

    def doIt(self, args):
        selectionList = OpenMaya.MGlobal.getActiveSelectionList()
        iter = OpenMaya.MItSelectionList(selectionList, OpenMaya.MFn.kDagNode )

        if iter.isDone():
            print '====================='
            print ' SCENE GRAPH (DAG):  '
            print '====================='
            self.printScene()
        else:
            print '======================='
            print ' SELECTED DAG OBJECTS: '
            print '======================='
            self.printSelectionDagPaths(iter)

    def printSelectionDagPaths( self, pSelectionListIter):
        dagFn = OpenMaya.MFnDagNode()

        while( not pSelectionListIter.isDone() ):
            dagPath = pSelectionListIter.getDagPath()
            try:
                dagPath.extendToShape()
            except:
                pass
            #print(  dagPath) 
            dagObject = dagPath.node()
            dagFn.setObject(dagObject)
            name = dagFn.name()
            #print( dagFn.name() )

            fntypes = []
            fntypes = OpenMaya.MGlobal.getFunctionSetList(dagObject)

            print name + ' (' + dagObject.apiTypeStr + ')'
            print '\tDAG path: [' + str( dagPath.fullPathName() ) + ']'
            print '\tCompatible function sets: ' + str( fntypes )

            pSelectionListIter.next()

    def printScene(self):
        dagNodeFn = OpenMaya.MFnDagNode()
        dagIterator = OpenMaya.MItDag( OpenMaya.MItDag.kDepthFirst, OpenMaya.MFn.kInvalid )

        while(not dagIterator.isDone()):
            dagObject = dagIterator.currentItem()
            depth = dagIterator.depth()
            dagNodeFn.setObject(dagObject)
            name = dagNodeFn.name()
            output = ''
            for i in range(0, depth):
                output += '\n'

            output += name + ' (' + dagObject.apiTypeStr + ')'
            print( output )
            dagIterator.next()

def cmdCreator():
    return printPathsCmd()

def initializePlugin(mobject):
    mplugin = OpenMaya.MFnPlugin(mobject)
    try:
        mplugin.registerCommand(kPluginCmdName, cmdCreator)
    except:
        sys.stderr.write("Failed to register command: %s\n" % kPluginCmdName )

def uninitializePlugin(mobject):
    mplugin = OpenMaya.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(kPluginCmdName)
    except:
        sys.stderr.write( "Failed to unregister command: %s\n" % kPluginCmdName )