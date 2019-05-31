#-*- coding:utf-8 -*- 
import maya.api.OpenMaya as om
import maya.mel as mel
import maya.cmds as cmds
import pymel.core as pm
import sys, os, json

def maya_useNewAPI():
    pass

pm.loadPlugin('fbxmaya')

# change by function [doEffect]
fromPath = ''
toPath = ''

# 如果有卡住的檔案很大的原因是因爲檔案壞了，這邊把壞掉的檔案記下來，直接跳過不導出了
excludeFiles = ['npc_FeMale_combat_idle_NW_90_r_01.ma']

def makeDir( path ):
    if not os.path.exists(path):
        os.makedirs(path)

def loopDir( path, do ):
    list = cmds.getFileList(folder=path)
    if list != None:
        for name in list:
            subPath = path + '/' + name 
            if name.find('.') == -1:
                loopDir( subPath, do )
            else:
                do( subPath, name )

def collectRoot():
    refs = cmds.ls(rn=True)
    rootNodes = []
    for ref in refs:
        if((":root" in ref) and 
        (ref.split(':')[-1]=='root' ) and 
        (not "WP_" in ref[:3])):
            parent = cmds.listRelatives(ref, p=True)
            if parent == None:
                rootNodes.append(ref)
    return len(rootNodes) > 0, rootNodes
                            
def exportFBX( filePath, fileName ):
    if fileName in excludeFiles:
        print( fileName + " is broke file! ignore it!")
        return

    if fileName.find('.ma') != -1 or fileName.find('.mb') != -1:

        exportPath = filePath.replace( fromPath, toPath )
        folderName = exportPath.replace( '/' + fileName, '')    
        fileName = exportPath.replace( '.mb', '.fbx' )
        fileName = fileName.replace( '.ma', '.fbx' )

        if os.path.exists(fileName):
            print( fileName + " already done!")
            return

        # open file
        cmds.file(filePath, o=True, force=True)

        # check has root
        hasRoot, rootNodes = collectRoot()
        if hasRoot:
            
            makeDir( folderName )
            
            cmds.select(cl=True)
            cmds.select(rootNodes[0])
            
            start = cmds.playbackOptions(q=True, ast=True)
            end = cmds.playbackOptions(q=True, aet=True)
            
            # Geometry
            mel.eval("FBXExportSmoothingGroups -v true")
            mel.eval("FBXExportHardEdges -v false")
            mel.eval("FBXExportTangents -v false")
            mel.eval("FBXExportSmoothMesh -v true")
            mel.eval("FBXExportInstances -v false")

            # Animation
            mel.eval("FBXExportBakeComplexAnimation -v true")
            mel.eval("FBXExportAnimationOnly -v false")
            mel.eval("FBXExportBakeComplexStart -v "+ str(start))
            mel.eval("FBXExportBakeComplexEnd -v "+ str(end))
            mel.eval("FBXExportBakeComplexStep -v 1")
            #mel.eval("FBXExportBakeResampleAll -v true")
            mel.eval("FBXExportUseSceneName -v false")
            mel.eval("FBXExportQuaternion -v euler")
            mel.eval("FBXExportShapes -v true")
            mel.eval("FBXExportSkins -v true")
            # Constraints
            mel.eval("FBXExportConstraints -v false")
            # Cameras
            mel.eval("FBXExportCameras -v false")
            # Lights
            mel.eval("FBXExportLights -v false")
            # Embed Media
            mel.eval("FBXExportEmbeddedTextures -v false")
            # Connections
            mel.eval("FBXExportInputConnections -v true")
            mel.eval("FBXExportFileVersion -v \"FBX201400\"")
            # Axis Conversion
            mel.eval("FBXExportUpAxis z")
            # Export
            mel.eval('FBXExport -f "'+ fileName +'" -s')

            # 有時會有error發生，但是try不到，只能crash
            #pm.mel.FBXExport(f=fileName)

            print( fileName + " success!")

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



