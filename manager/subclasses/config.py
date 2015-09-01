'''
Created on 1. sep. 2015

@author: stianstrom
'''

from queue import *
import json

class Config:
    '''
    classdocs
    '''
    
    
    def __init__(self, params):
        '''
        Constructor
        '''
    def convertJSONToDictionary(self,data):
        jsondict=json.loads(data)[0]
        return jsondict
    def writeConfig(self, configdata):
        for key, value in configdata.iteritems() :
            self.writeToFile(key,str(value)) 
    def writeToFile(self, key,value):
        file=open('config.cfg','a')
        file.write(key+ " = "+value+"\n" )
    
        