# -*- coding: utf-8 -*-
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