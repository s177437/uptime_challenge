from Queue import *
'''
Created on 1. sep. 2015

@author: stianstrom
'''
class Report():
    queue = Queue()
    groupname=""
    course=""
    def createReportQueue(self, queuename,content):
        self.queue.createQueue(queuename, content)

    def buildReport(self, content):
        list= content.split()
        print list

    def writeReportToDatabase(self,content):
        self.createReportQueue("dbreportq", content)





    
    
    
