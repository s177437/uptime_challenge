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
        dict={}
        for i,j in zip(list,list[1:]):
            dict.update({i,j})
        print dict



    def writeReportToDatabase(self,content):
        self.createReportQueue("dbreportq", content)