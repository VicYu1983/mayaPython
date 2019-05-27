import maya.api.OpenMaya as om
import maya.cmds as cmds
import pymel.core as pm
import sys, os, json

def maya_useNewAPI():
    pass

pm.loadPlugin('fbxmaya')

# change by function [doEffect]
fromPath = ''
toPath = ''

def makeDir( path ):
    if not os.path.exists(path):
        os.makedirs(path)

def loopDir( path, do ):
    list = cmds.getFileList(folder=path)
    if list != None:
        for name in list:
            subPath = path + '\\' + name 
            if name.find('.') == -1:
                loopDir( subPath, do )
            elif name.find('.mb') != -1:
                do( subPath, name )
                
def exportFBX( filePath, fileName ):
    exportPath = filePath.replace( fromPath, toPath )
    folderName = exportPath.replace( '\\' + fileName, '')    
    fileName = exportPath.replace( '.mb', '.fbx' )
    makeDir( folderName )
    cmds.file(filePath, o=True)
    pm.mel.FBXExport(f=fileName)

def doEffect( params ):
    params = json.loads(params[0])

    global fromPath, toPath
    fromPath = params[0]
    toPath = params[1]
    loopDir( fromPath, exportFBX )    

class BatchExportFBX( om.MPxCommand ):
    kPluginCmdName = 'BatchExportFBX'

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return BatchExportFBX()
    
    def doIt(self, args):
        doEffect( args.asStringArray(0) )

def initializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.registerCommand(
            BatchExportFBX.kPluginCmdName, BatchExportFBX.cmdCreator
        )
    except:
        sys.stderr.write(
            "Failed to register command: %s\n" % BatchExportFBX.kPluginCmdName
        )
        raise

def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)     
    try:
        pluginFn.deregisterCommand(BatchExportFBX.kPluginCmdName) 
    except:
        sys.stderr.write(
            "Failed to unregister command: %s\n" % BatchExportFBX.kPluginCmdName
        )



