'''
Created on 1. sep. 2015

@author: stianstrom
'''
from Queue import *
class Report():
    queue = Queue()

    groupname=""
    course=""
    def createReportQueue(self, queuename,content):
        self.queue.createQueue(queuename, content)

    def buildReport(self, content):
        return content

    def writeReportToDatabase(self,content):
        self.createReportQueue("dbreportq", content)





    
    
    