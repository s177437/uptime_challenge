from Queues import *
from Account import *
import json
import ConfigParser
import couchdb
import ast
import Pyro4
import random
import logging

__author__ = 'Stian Stroem Anderssen'


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
    interpreterserver = Pyro4.Proxy("PYRONAME:interpreter")

    @staticmethod
    def convert_json_to_dictionary(self, data):
        """
        A function to convert JSON contents to a dict.
        :param data:
        :type data:
        :return:
        :rtype:
        """
        jsondict = json.loads(data)[0]
        return jsondict

    @staticmethod
    def request_user_creation(self, configobject):
        """
        Build dictionary containtaining courseinformation that is sent to the interpreter based on the content of the
        config object.
        :param configobject:
        :type configobject:
        :return listtosend:
        :rtype list:
        """
        listtosend = []
        teacherdict = {"teacher": [configobject.get_account().get_teacher()]}
        listtosend.append(teacherdict)
        semesterdict = {"semester": [configobject.get_account().get_semester()]}
        listtosend.append(semesterdict)
        coursedict = {"course": [configobject.get_account().get_course()]}
        listtosend.append(coursedict)
        groupsdict = {}
        groupsandmembers = configobject.get_account().get_groups()
        tempdict = groupsandmembers[0]
        groupsdict.update({"groups": tempdict})
        listtosend.append(groupsdict)
        return listtosend

    @staticmethod
    def send_users_to_queue(self, accountlist):
        """
        OUTDATED- This function converts the accountlist to a string that can be sent over a queue.
        :param accountlist:
        :type accountlist:
        :return:
        :rtype:
        """
        listtostring = accountlist
        queue = Queues()
        queue.create_queue("createuserq", str(listtostring))

    @staticmethod
    def find_groupnames(self, grouplist):
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

    def write_config(self, configdata):
        """
        Write config from the database to the config.ini file
        :param configdata:
        :type configdata:
        :return:
        :rtype:
        """
        for key, value in configdata.iteritems():
            self.write_to_file(key, str(value))

    @staticmethod
    def write_to_file(self, key, value):
        """
        Write config to config.ini
        :param key:
        :type key:
        :param value:
        :type value:
        :return:
        :rtype:
        """
        with open('/root/uptime_challenge_master/manager/config.ini', 'r') as f:
            words = f.read().split()
            if key in words:
                logging.info("No need to write to file, key is present")
            else:
                file = open('/root/uptime_challenge_master/manager/config.ini', 'a')
                file.write(key + " = " + value + "\n")

    def read_config_from_file(self):
        """
        Read static config provided in config.ini and build an account object.
        :return configclass:
        :rtype Config:
        """
        config = ConfigParser.SafeConfigParser()
        config.read("/root/uptime_challenge_master/manager/config.ini")
        configclass = Config()
        configclass.set_account(self.account)
        configclass.get_account().set_course(config.get("Account", "course"))
        configclass.get_account().set_groups(json.loads(config.get("Account", "groups")))
        configclass.get_account().set_teacher(config.get("Account", "teacher"))
        configclass.get_account().set_semester(config.get("Account", "semester"))
        configclass.set_config_dbname(config.get("Global", "configdbname"))
        configclass.set_script_path(config.get("Global", "scriptpath"))
        configclass.set_dbserver(config.get("Global", "dbserver"))
        configclass.set_queserver(config.get("Global", "queueserver"))
        return configclass

    def init_db_config(self):
        """
        Build the final config object after the DbConfig is initialized along with the local config
        :return config :
        :rtype Config:
        """
        config = self.initiate_users()
        configdict = self.interpreterserver.fetchConfig(config.get_account().get_teacher())
        # self.write_config(configdict)
        configparser = ConfigParser.SafeConfigParser()
        configparser.read("/root/uptime_challenge_master/manager/config.ini")
        config.set_interval(configparser.get("Global", "interval"))
        config.set_queue_name(configparser.get("Global", "queue_name"))
        return config

    @staticmethod
    def create_user_list(self, usersdictlist):
        userlist = []
        for userdict in usersdictlist:
            userlist.append(userdict["group"])
        return userlist

    def initiate_users(self):
        usersdictlist = self.interpreterserver.getEnabledUsers()
        config = ConfigParser.SafeConfigParser()
        config.read("/root/uptime_challenge_master/manager/config.ini")
        userlist = self.create_user_list(usersdictlist)
        configclass = Config()
        configclass.set_account(self.account)
        configclass.get_account().set_course(config.get("Account", "course"))
        configclass.get_account().set_teacher(config.get("Account", "teacher"))
        configclass.get_account().set_semester(config.get("Account", "semester"))
        configclass.get_account().set_groups(userlist)
        configclass.set_config_dbname(config.get("Global", "configdbname"))
        configclass.set_script_path(config.get("Global", "scriptpath"))
        configclass.set_dbserver(config.get("Global", "dbserver"))
        configclass.set_queserver(config.get("Global", "queueserver"))
        return configclass

    @staticmethod
    def create_work_queue(self, queuename, joblist):
        """
        Function to create a workqueue that is used to put jobs on
        :param queuename:
        :type String:
        :param joblist:
        :type list:
        :return:
        :rtype:
        """
        queue = Queues()
        for group, job in joblist.iteritems():
            for j in job:
                jobdict = {}
                jobdict.update({group: j})
                queue.create_queue(queuename, jobdict)

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

    def set_config_dbname(self, value):
        """
        Set the dbname of the couchdb
        :param value:
        :type value:
        :return:
        :rtype:
        """
        self.configdbname = value

    def get_config_dbname(self):
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

    def get_account(self):
        """
        Return accountobject.
        :return:
        :rtype:
        """
        return self.account

    def set_account(self, a):
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

    def set_config_instance(self, value):
        """
        Set the configobject before the database config is applied. This is used instead of using a global variable

        :param value:
        :type value:
        :return:
        :rtype:
        """
        self.configinstance = value

    def get_config_instance(self, value):
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
        Return the path to the executable location of the test on the LeeshoreWorker.
        :return:
        :rtype:
        """
        return self.scriptpath

    def set_script_path(self, path):
        """
        Set the script path on the LeeshoreWorker.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        self.scriptpath = path

    @staticmethod
    def function(self, x):
        return -0.25 * x ** 2 + 50

    @staticmethod
    def derived_off_function(self, x):
        return -0.5 * x

    def return_load(self, x):
        answer = []
        load = self.function(x)
        derivative = self.derived_off_function(x)
        answer.append(float(load))
        answer.append(float(derivative))
        return answer
