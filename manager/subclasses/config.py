'''
Created on 1. sep. 2015

@author: stianstrom
'''

from queue import *
from account import *
import json
import ConfigParser
class Config:
    '''
    classdocs
    '''
    
    queue_name=""
    interval=0
    account=Account()
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
        file=open('config.ini','a')
        file.write(key+ " = "+value+"\n" )
    
    def readConfigFromFile(self):
        config=ConfigParser.SafeConfigParser()
        config.read("config.ini")
        configclass=Config()
        configclass.getAccount().set_course(config.get("Account,","course"))
        configclass.getAccount.set_group(config.get("Account","group"))
        configclass.set_interval(config.get("Global","interval"))
        configclass.set_queue_name(config.get("Global", "queue_name"))
        return configclass
    def get_queue_name(self):
        return self.__queue_name

    def get_interval(self):
        return self.__interval


    def set_queue_name(self, value):
        self.__queue_name = value
    def getAccount(self):
        return self.account
    def setAccount(self, a):
        self.account=a
    def set_interval(self, value):
        self.__interval = value




  