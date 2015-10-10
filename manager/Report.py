from Queue import *
import ast
import Pyro4

'''
Created on 1. sep. 2015

@author: stianstrom
'''


class Report():
    groupname = ""
    course = ""
    interpreterServer = Pyro4.Proxy("PYRONAME:interpreter")

    def createReportQueue(self, queuename, content):
        queue = Queue()
        queue.createQueue(queuename, content)

    def buildReport(self, content):
        dict = ast.literal_eval(content)
        self.writeReportToDatabase(dict)

    # comment


    def writeReportToDatabase(self, reportdict):
        groupname = reportdict['group']
        dbname = "testaccounts"
        for key, value in reportdict.iteritems():
            if "Award" in key:
                self.interpreterServer.updateBalance(dbname, groupname, value)
        self.interpreterServer.postReportToDatabase(reportdict)
