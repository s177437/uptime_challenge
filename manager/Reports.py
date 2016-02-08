#import pdb;pdb.set_trace() 
from Queues import *
import ast
import Pyro4
import time
import logging
'''
Created on 1. sep. 2015

@author: stianstrom
'''
from Queues import *
from Invoice import *

class Reports():

    """
    This module aims to build a report
    """
    groupname = ""
    course = ""
    interpreterServer = Pyro4.Proxy("PYRONAME:interpreter")
    logging.basicConfig(filename='/var/log/manager.log',level=logging.CRITICAL)

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
            elif "vmcount" in key :
                self.charge(value,groupname,dbname)
        if added_to_database_already ==0:
            self.interpreterServer.postReportToDatabase(reportdict)

    def calculateAward(self, reportdict):
        dbname="accounts"
        userconfig = self.interpreterServer.getUserConfig(reportdict["group"],"couchdb")
        hourly_rate=userconfig["hourly_rate"]
        last_check=userconfig["last_check"]
        partial_ok_punishment_decrease=userconfig["partial_ok_punishment_decrease"]
        reward = 0
        if (last_check<reportdict["Check timestamp"]) :
            if reportdict["Test status"] == "OK" :
                reward = float(hourly_rate)*((time.time()-last_check)/3600)
                self.calculateBonus(reportdict,userconfig)
            elif "Partial" in  reportdict["Test status"] :
                reward=0
                reward = (((hourly_rate)*(time.time()-float(last_check)))/3600)*partial_ok_punishment_decrease
                logging.critical("Group: "+reportdict["group"]+" Hourly rate: "+str(hourly_rate)+ " Time since last check: " + str((time.time()-float(last_check)))+ " POC: "+ str(partial_ok_punishment_decrease)+ " Reward " + str(reward))
            elif reportdict["Test status"] == "Not Approved" :
                reward = ((hourly_rate)*((time.time()-float(last_check))/3600))*(-1)
            else :
                reward = 0
        else :
            logging.critical("The timestamp on the report is older than a newer already written to the database")
            reportdict["Test status"]="The timestamp on this report is older than a previous posted one"
            reward= 0
        self.interpreterServer.updateBalance(dbname, reportdict["group"], reward)
        reward=0
        self.interpreterServer.modify_key("couchdb", "accounts", "group", reportdict["group"], "last_check", reportdict["Check timestamp"])
        return reportdict


    def calculateBonus(self, reportdict,userconfig):
        bonus_value=userconfig["bonus"]
        time_used=reportdict["Time used to download"]
        bonus_time_cutoff= userconfig["bonus_time_cutoff"]
        bonus= ((bonus_time_cutoff/time_used)*bonus_value)/12
        self.interpreterServer.updateBalance("accounts", reportdict["group"], bonus)


    def charge(self,vmcountdict,groupname,dbname):
        i = Invoice()
        price=i.calculatePrice(vmcountdict)
        self.interpreterServer.updateBalance(dbname, groupname,price)
        print "Price is updated on user", groupname, "with price", price








