﻿# -*- coding: utf-8 -*-
class DataManager:
    __instance = None

    @staticmethod
    def getInstance():
        if DataManager.__instance == None:
            DataManager()
        return DataManager.__instance
        
    def __init__(self):
        self.__data = {}
        if DataManager.__instance != None:
            raise Exception('這是單例模式')
        else:
            DataManager.__instance = self
            
    def setData(self, key, value ):
        if self.hasData( key ):
            print('已經有資料了，覆寫它! key:' + str(key))
        self.__data[key] = value
        
    def getData(self, key ):
        if self.hasData( key ):
            return self.__data[key]
        return None
        
    def hasData(self, key ):
        try:
            self.__data[key]
            return True
        except:
            return False
            
    def removeData( self, key ):
        if self.hasData(key):
            del self.__data[key] 
            
    def getDataPoint(self):
        return self.__data
        
'''
#example  
m = DataManager.getInstance()
m.setData('id', 3)

print( m.getData('id'))

m.removeData('id')
print( m.getData('id'))

m.removeData('id')
'''

from maya.api.OpenMaya import *
from maya.cmds import *

class GameObj():
    def __init__(self, name, dynamicBounding = True):
        self.friction = .9
        selection = MGlobal.getSelectionListByName( name )
        self.__name = name
        self.__transform = MFnTransform(selection.getDagPath(0).transform())  
        self.__dynamicBounding = dynamicBounding  
        if self.__dynamicBounding:
            self.__bounding = MFnDagNode( selection.getDagPath(0) )
        else:
            self.__bounding = MFnDagNode( selection.getDagPath(0) ).boundingBox.transformUsing( self.getMatrix().inverse() )
        self.velocity = MVector()
        
    def getPosition(self):
        return self.__transform.translation( MSpace.kTransform )
        
    def setPosition(self, pos):
        self.__transform.setTranslation( pos, MSpace.kTransform )
        
    def getRotation(self):
        return self.__transform.rotation( MSpace.kTransform ) 
        
    def setRotation( self, rot ):
         self.__transform.setRotation( rot, MSpace.kTransform ) 
        
    def getBoundingBox(self):
        if self.__dynamicBounding:
            return self.__bounding.boundingBox
        else:
            globalBoundingBox = MBoundingBox( self.__bounding )
            globalBoundingBox.transformUsing( self.getMatrix() )
            return globalBoundingBox
        
    def checkHit( self, gameObj ):
        return self.getBoundingBox().intersects( gameObj.getBoundingBox() )
        
    def getMatrix( self ):
        return self.__transform.transformation().asMatrix()
        
    def clone( self ):
        cloneObj = duplicate( self.__name )
        return GameObj( cloneObj[0] )
        
    def setName( self, name ):
        select( self.__name )
        rename( name )
        select( clear=True )
        
    def update(self):
        position = self.getPosition()
        position += self.velocity
        self.velocity *= self.friction
        self.setPosition( position )
        
    
        
    
        
    