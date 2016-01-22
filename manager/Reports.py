#import pdb;pdb.set_trace() 
from Queues import *
import ast
import Pyro4
import time

'''
Created on 1. sep. 2015

@author: stianstrom
'''
from Queues import *

class Reports():
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
        queue = Queues()
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
        dbname = "accounts"
	added_to_database_already=0
        for key, value in reportdict.iteritems():
            if "Award" in key:
                self.interpreterServer.updateBalance(dbname, groupname, str(value))
                self.interpreterServer.postReportToDatabase(reportdict)
		added_to_database_already=1
            elif "Lookup status" in key :
                new_reportdict= self.calculateAward(reportdict)
                self.interpreterServer.postReportToDatabase(new_reportdict)
		added_to_database_already=1
	if added_to_database_already ==0:
	    self.interpreterServer.postReportToDatabase(reportdict)

    def calculateAward(self, reportdict):
        dbname="accounts"
        userconfig = self.interpreterServer.getUserConfig(reportdict["group"],"couchdb")
        hourly_rate=userconfig["hourly_rate"]
        last_check=userconfig["last_check"]
        partial_ok_punishment_decrease=userconfig["partial_ok_punishment_decrease"]
        now= time.time()
        reward = 0.0
        if (last_check<reportdict["Check timestamp"]) :
            if reportdict["Test status"] == "OK" :
                reward = float(hourly_rate)*((now-last_check)/3600)
                self.calculateBonus(reportdict,userconfig)
            elif "Partial" in  reportdict["Test status"] :
                reward = ((hourly_rate)*((now-last_check)/3600))*partial_ok_punishment_decrease
            elif reportdict["Test status"] == "Not Approved" :
                reward = ((hourly_rate)*((now-last_check)/3600))*(-1)
            else :
                reward = 0
        else :
            reportdict.update({"Message": "This test finished after a newer one finished."})
            reward= 0
        self.interpreterServer.updateBalance(dbname, reportdict["group"], reward)
        self.interpreterServer.modify_key("couchdb", "accounts", "group", reportdict["group"], "last_check", reportdict["Check timestamp"])
        return reportdict


    def calculateBonus(self, reportdict,userconfig):
        bonus_value=userconfig["bonus"]
        time_used=reportdict["Time used to download"]
        bonus_time_cutoff= userconfig["bonus_time_cutoff"]
        bonus= (bonus_time_cutoff/time_used)*bonus_value
        self.interpreterServer.updateBalance("accounts", reportdict["group"], bonus)







