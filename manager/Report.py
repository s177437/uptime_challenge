from Queue import *
'''
Created on 1. sep. 2015

@author: stianstrom
'''
class Report():
    groupname=""
    course=""

    def createReportQueue(self, queuename,content):
        queue=Queue()
        queue.createQueue(queuename, content)

    def buildReport(self, content):
        list= content.split()
        print list

    def writeReportToDatabase(self,content):
        self.createReportQueue("dbreportq", content)