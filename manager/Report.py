from Queue import *
import ast
import Pyro4

'''
Created on 1. sep. 2015

@author: stianstrom
'''


class Report():
    """
    This module aims to build a report
    """
    groupname = ""
    course = ""
    interpreterServer = Pyro4.Proxy("PYRONAME:interpreter")

    def createReportQueue(self, queuename, content):
        """
        Create the report queue
        :param queuename:
        :type queuename:
        :param content:
        :type content:
        :return:
        :rtype:
        """
        queue = Queue()
        queue.createQueue(queuename, content)

    def buildReport(self, content):
        """
        Build and format the report content
        :param content:
        :type content:
        :return:
        :rtype:
        """
        dict = ast.literal_eval(content)
        self.writeReportToDatabase(dict)

    # comment


    def writeReportToDatabase(self, reportdict):
        """
        Write report to the database and update the balance of the user.
        :param reportdict:
        :type reportdict:
        :return:
        :rtype:
        """
        groupname = reportdict['group']
        dbname = "testaccounts"
        for key, value in reportdict.iteritems():
            if "Award" in key:
                self.interpreterServer.updateBalance(dbname, groupname, value)
        self.interpreterServer.postReportToDatabase(reportdict)
