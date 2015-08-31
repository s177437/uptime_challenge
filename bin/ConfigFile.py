'''
Created on 31. aug. 2015

@author: stianstrom
'''
class ConfigFile(object):
    def writeConfig(self, configdata):
        for key, value in configdata.iteritems() :
            self.writeToFile(key,str(value)) 
    def writeToFile(self, key,value):
        file=open('config.cfg','a')
        file.write(key+ " = "+value+"\n" )
        
        

        
