from Queue import *
import ast
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
	dict = ast.literal_eval(content)
	print dict	



    def writeReportToDatabase(self,content):
        self.createReportQueue("dbreportq", content)
