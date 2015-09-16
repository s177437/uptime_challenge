from Queue import *
import ast
import Pyro4
'''
Created on 1. sep. 2015

@author: stianstrom
'''
class Report():
    groupname=""
    course=""
    interpreterServer=Pyro4.Proxy("PYRONAME:interpreter")

    def createReportQueue(self, queuename,content):
        queue=Queue()
        queue.createQueue(queuename, content)

    def buildReport(self, content):
	    dict = ast.literal_eval(content)
	    self.writeReportToDatabase(dict)



    def writeReportToDatabase(self,reportdict):
        self.interpreterServer.postReportToDatabase(reportdict)

