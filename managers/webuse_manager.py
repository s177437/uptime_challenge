from Queues import *
from Config import *
import logging
from WebUseMath import *
import pika
import couchdb
import Pyro4
import time

__author__ = 'Stian Stroem Anderssen'


class Httpmanager():
    """
    This module is the main class for the manager project. This module takes care of the execution of the functions.
    """
    interpreterServer = Pyro4.Proxy("PYRONAME:interpreter")

    def fetch_config(self):
        """
        This function is the main method where everything is governed on the manager.
        :return:
        :rtype:
        """
        math = WebUseMath()
        strengthlist = math.create_time_list()
        position = 0
        config = Config()
        newconfig = config.initDbConfig()
        grouplist = newconfig.getAccount().get_groups()
        path = newconfig.get_script_path()
        index = 0
        logging.info("Interval" + str(newconfig.get_interval()))
        positiondict = {}
        ip = ""
        for i in grouplist:
            userconfig = self.interpreterServer.getFileAndOffsetFromUser(i)
            ipconfig = self.interpreterServer.getIpFromUser(i)
            ip = ""
            ip = ipconfig["ipaddress"]
            executable_string = path + "webuse.pl -U " + ip + " -r '10:10:10:10'"
            logging.info(str(userconfig))
            index = int(userconfig["offset"])
            logging.info("INDEX " + str(index))
            content = math.decideEntry(strengthlist, index)
            worklist = []
            listvalues = math.convertToList(content)
            position = int(listvalues[0])
            strength_number = math.calculateList(listvalues)
            worklist = math.create_number_of_scripts(strength_number, executable_string)
            groupdict = {}
            groupdict.update({i: worklist})
            newconfig.createWorkQ(newconfig.get_queue_name(), groupdict)
            worklist = []
            positiondict.update({i: position})
        while True:
            for i, position in positiondict.iteritems():
                worklist = []
                ip = ""
                ipconfig = self.interpreterServer.getIpFromUser(i)
                ip = ipconfig["ipaddress"]
                executable_string = path + "webuse.pl -U " + ip + " -r '10:10:10:10'"
                logging.info("USER: " + str(i) + " POSITION: " + str(position))
                strength_value_as_string = math.jumpToNextEntry(strengthlist, int(position))
                values_in_value_string = math.convertToList(strength_value_as_string)
                strength_number = math.calculateList(values_in_value_string)
                worklist = math.create_number_of_scripts(strength_number, executable_string)
                groupdict = {}
                groupdict.update({i: worklist})
                if position == 288:
                    positiondict[i] = 0
                else:
                    positiondict[i] = position + 1
                newconfig.createWorkQ(newconfig.get_queue_name(), groupdict)
                queue = Queues()
            queue.receive_one_message_from_q("webusereportq", newconfig.get_interval())


manager = Httpmanager()
manager.fetch_config()
