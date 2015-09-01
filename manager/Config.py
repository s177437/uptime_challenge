'''
Created on 1. sep. 2015

@author: stianstrom
'''

from Queue import *
from Account import *
import json
import ConfigParser
import couchdb
import ast
class Config:
    queue_name=""
    interval=0
    configdbname=""
    dbserver=""
    queserver=""
    configinstance="None"
    account=Account() 
    
    def convertJSONToDictionary(self,data):
        jsondict=json.loads(data)[0]
        return jsondict
    
    def writeConfig(self, configdata):
        for key, value in configdata.iteritems() :
            self.writeToFile(key,str(value)) 
    
    def writeToFile(self, key,value):
        with open('config.ini','r') as f : 
            words=f.read().split()
            if key in words : 
                print "No need to write to file, key is present" 
            else: 
                file=open('config.ini','a')
                file.write(key+ " = "+value+"\n" )
    
    def readConfigFromFile(self):
        config=ConfigParser.SafeConfigParser()
        config.read("config.ini")
        configclass=Config()
        configclass.setAccount(self.account)
        configclass.getAccount().set_course(config.get("Account","course"))
        configclass.getAccount().set_group(config.get("Account","group"))
        configclass.setConfigDbName(config.get("Global", "configdbname"))
        configclass.set_dbserver(config.get("Global","dbserver"))
        configclass.set_queserver(config.get("Global","queueserver"))
        return configclass
        
    def initDbConfig(self):
        config = self.readConfigFromFile()
        queue=Queue()
        queue.createQueue("requestconfigq", "configrequest")
        queue.receiveOneMessageFromQ("sendconfig")
        configdict= ast.literal_eval(queue.getQueueContent())
        self.writeConfig(configdict)
        configparser=ConfigParser.SafeConfigParser()
        configparser.read("config.ini")
        config.set_interval(configparser.get("Global","interval"))
        config.set_queue_name(configparser.get("Global","queue_name"))
        return config
    def createWorkQ(self,queuename):
        queue=Queue()
        queue.createQueue(queuename, "")
        
        
        
        
       
        
        
        
        

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
          





  
