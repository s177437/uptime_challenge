'''
Created on 1. sep. 2015

@author: stianstrom
'''

from Queue import *
from Account import *
import json
import ConfigParser
import couchdb
class Config:
       
    queue_name=""
    interval=0
    account=Account()
    configdbname=""
    dbserver=""
    queserver=""
    configinstance="None"
    
    
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
        configclass.setConfigDbName(config.get("Global", "configdbname"))
        configclass.set_dbserver(config.get("Global","dbserver"))
        configclass.set_queserver(config.get("Glocal","queueserver"))
        return configclass
        
    def initDbConfig(self):
        config = self.readConfigFromFile()
        print config.get_dbserver()
    def get_queue_name(self):
        return self.__queue_name

    def get_interval(self):
        return self.__interval

    def setConfigDbName(self,value):
        self.configdbname=value
    def getConfigDbName(self):
        return self.configdbname
    def set_queue_name(self, value):
        self.__queue_name = value
    def getAccount(self):
        return self.account
    def setAccount(self, a):
        self.account=a
    def set_interval(self, value):
        self.__interval = value
        
    def get_dbserver(self):
        return self.__dbserver

    def get_queserver(self):
        return self.__queserver

    def set_dbserver(self, value):
        self.__dbserver = value

    def set_queserver(self, value):
        self.__queserver = value
    def setConfigInstance(self, value):
        self.configinstance=value
    def getConfigInstance(self, value):
        return self.configinstance
          





  