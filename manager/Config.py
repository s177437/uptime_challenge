'''
Created on 1. sep. 2015

@author: stianstrom
'''

from Queue import *
from Account import *
import json
import ConfigParser
import couchdb
import ast
import Pyro4
import random


class Config:
    """
    This module aims to build and keep track of the manager objet during runtime. Every time a user creation is
    requested. This module is called.
    """
    queue_name = ""
    scriptpath = ""
    interval = 0
    configdbname = ""
    dbserver = ""
    queserver = ""
    configinstance = "None"
    account = Account()
    interpreterServer = Pyro4.Proxy("PYRONAME:interpreter")

    def convertJSONToDictionary(self, data):
        """
        A function to convert JSON contents to a dict.
        :param data:
        :type data:
        :return:
        :rtype:
        """
        jsondict = json.loads(data)[0]
        return jsondict

    def requestUserCreation(self, configobject):
        """
        Build dictionary containtaining courseinformation that is sent to the interpreter based on the content of the
        config object.
        :param configobject:
        :type configobject:
        :return listtosend:
        :rtype list:
        """
        listtosend = []
        teacherdict = {"teacher": [configobject.getAccount().get_teacher()]}
        listtosend.append(teacherdict)
        semesterdict = {"semester": [configobject.getAccount().get_semester()]}
        listtosend.append(semesterdict)
        coursedict = {"course": [configobject.getAccount().get_course()]}
        listtosend.append(coursedict)
        groupsdict = {}
        groupsandmembers = configobject.getAccount().get_groups()
        tempdict = groupsandmembers[0]
        groupsdict.update({"groups": tempdict})
        listtosend.append(groupsdict)
        return listtosend

    def sendUsersToQueue(self, accountlist):
        """
        OUTDATED- This function converts the accountlist to a string that can be sent over a queue.
        :param accountlist:
        :type accountlist:
        :return:
        :rtype:
        """
        listtostring = accountlist
        queue = Queue()
        queue.createQueue("createuserq", str(listtostring))

    def findGroupnames(self, grouplist):
        """
        Return a list of the groupnames
        :param grouplist:
        :type grouplist:
        :return groupnames:
        :rtype:
        """
        groupnames = []
        for i, j in grouplist[0].iteritems():
            groupnames.append(i)
        return groupnames

    def writeConfig(self, configdata):
        """
        Write config from the database to the config.ini file
        :param configdata:
        :type configdata:
        :return:
        :rtype:
        """
        for key, value in configdata.iteritems():
            self.writeToFile(key, str(value))

    def writeToFile(self, key, value):
        """
        Write config to config.ini
        :param key:
        :type key:
        :param value:
        :type value:
        :return:
        :rtype:
        """
        with open('config.ini', 'r') as f:
            words = f.read().split()
            if key in words:
                print "No need to write to file, key is present"
            else:
                file = open('config.ini', 'a')
                file.write(key + " = " + value + "\n")

    def readConfigFromFile(self):
        """
        Read static config provided in config.ini and build an account object.
        :return configclass:
        :rtype Config:
        """
        config = ConfigParser.SafeConfigParser()
        config.read("config.ini")
        configclass = Config()
        configclass.setAccount(self.account)
        configclass.getAccount().set_course(config.get("Account", "course"))
        configclass.getAccount().set_groups(json.loads(config.get("Account", "groups")))
        configclass.getAccount().set_teacher(config.get("Account", "teacher"))
        configclass.getAccount().set_semester(config.get("Account", "semester"))
        configclass.setConfigDbName(config.get("Global", "configdbname"))
        configclass.set_script_path(config.get("Global", "scriptpath"))
        configclass.set_dbserver(config.get("Global", "dbserver"))
        configclass.set_queserver(config.get("Global", "queueserver"))
        return configclass

    def initDbConfig(self):
        """
        Build the final config object after the DbConfig is initialized along with the local config
        :return config :
        :rtype Config:
        """
        config = self.readConfigFromFile()
        configdict = self.interpreterServer.fetchConfig(config.getAccount().get_teacher())
        self.writeConfig(configdict)
        configparser = ConfigParser.SafeConfigParser()
        configparser.read("config.ini")
        config.set_interval(configparser.get("Global", "interval"))
        config.set_queue_name(configparser.get("Global", "queue_name"))
        return config

    def createWorkQ(self, queuename, joblist):
        """
        Function to create a workqueue that is used to put jobs on
        :param queuename:
        :type String:
        :param joblist:
        :type list:
        :return:
        :rtype:
        """
        queue = Queue()
        for group, job in joblist.iteritems():
            for j in job:
                jobdict = {}
                jobdict.update({group: j})
                queue.createQueue(queuename, jobdict)

    def get_queue_name(self):
        """
        Return queue_name
        :return:
        :rtype:
        """
        return self.__queue_name

    def get_interval(self):
        """
        Rrturn interval used in the dbconfig
        :return:
        :rtype:
        """
        return self.__interval

    def setConfigDbName(self, value):
        """
        Set the dbname of the couchdb
        :param value:
        :type value:
        :return:
        :rtype:
        """
        self.configdbname = value

    def getConfigDbName(self):
        """
        Get the dbname of the couchdb.
        :return:
        :rtype:
        """
        return self.configdbname

    def set_queue_name(self, value):
        """
        Set queuename to be used
        :param value:
        :type value:
        :return:
        :rtype:
        """
        self.__queue_name = value

    def getAccount(self):
        """
        Return accountobject.
        :return:
        :rtype:
        """
        return self.account

    def setAccount(self, a):
        """
        Set accountobject
        :param a:
        :type a:
        :return:
        :rtype:
        """
        self.account = a

    def set_interval(self, value):
        """
        Set interval
        :param value:
        :type value:
        :return:
        :rtype:
        """
        self.__interval = value

    def get_dbserver(self):
        """
        Return dbservername
        :return:
        :rtype:
        """
        return self.__dbserver

    def get_queserver(self):
        """
        Return queueservername
        :return:
        :rtype:
        """
        return self.__queserver

    def set_dbserver(self, value):
        """
        set dbservername
        :param value:
        :type value:
        :return:
        :rtype:
        """
        self.__dbserver = value

    def set_queserver(self, value):
        """
        set queueserver name
        :param value:
        :type value:
        :return:
        :rtype:
        """
        self.__queserver = value

    def setConfigInstance(self, value):
        """
        Set the configobject before the database config is applied. This is used instead of using a global variable

        :param value:
        :type value:
        :return:
        :rtype:
        """
        self.configinstance = value

    def getConfigInstance(self, value):
        """
        Return the config class object.
        :param value:
        :type value:
        :return:
        :rtype:
        """
        return self.configinstance

    def get_script_path(self):
        """
        Return the path to the executable location of the test on the worker.
        :return:
        :rtype:
        """
        return self.scriptpath

    def set_script_path(self, path):
        """
        Set the script path on the worker.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        self.scriptpath = path
    def function(self, x):
        return -0.25 * x ** 2 + 50

    def derivedOfFunction(self, x):
        return -0.5 * x

    def returnLoad(self, x):
        answer = []
        load = self.function(x)
        derivative = self.derivedOfFunction(x)
        answer.append(int(load))
        answer.append(int(derivative))
        return answer

