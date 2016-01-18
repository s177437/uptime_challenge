from Queues import *
from Config import *
import logging
from WebUseMath import *
import pika
import couchdb
import Pyro4
import time



class Httpmanager():
    """
    This module is the main class for the manager project. This module takes care of the execution of the functions.
    """
    interpreterServer = Pyro4.Proxy("PYRONAME:interpreter")
    # comment
    def fetchConfig(self):
        """
        This function is the main method where everything is governed on the manager.
        :return:
        :rtype:
        """	
        math=WebUseMath()
        strengthlist = math.createTimeList()
        position=0
        config = Config()
        newconfig = config.initDbConfig()
        #grouplist = newconfig.findGroupnames(newconfig.getAccount().get_groups())
	grouplist=newconfig.getAccount().get_groups()
        path = newconfig.get_script_path()
        #executable_string=path + "webuse.pl -U 128.39.121.59 -r '10:10:10:10'"
        #executable_string=path + "webuse.pl -U 128.39.121.59 -r '10/10/10/10'"
        index=0
        logging.info("Interval"+str(newconfig.get_interval()))
        positiondict = {}
        for i in grouplist:
            userconfig = self.interpreterServer.getFileAndOffsetFromUser(i)
            ipconfig = self.interpreterServer.getIpFromUser(i)
            ip=ipconfig["ipaddress"]
            executable_string=path + "webuse.pl -U " + ip +" -r '10:10:10:10'"
            logging.info(str(userconfig))
            index = int(userconfig["offset"])
            logging.info("INDEX "+str(index))
            content = math.decideEntry(strengthlist,index)
            worklist=[]
            listvalues = math.convertToList(content)
            position= int(listvalues[0])
            logging.info("USER: "+ str(i)+" POSITION: "+ str(position))
            strength_number=math.calculateList(listvalues)
            worklist = math.create_number_of_scripts(strength_number,executable_string)
            groupdict = {}
            groupdict.update({i: worklist})
            newconfig.createWorkQ(newconfig.get_queue_name(), groupdict)
            worklist = []
            positiondict.update({i:position})
        while True:
            for i, position in positiondict.iteritems():
                logging.info("USER: "+ str(i)+" POSITION: "+ str(position))
                strength_value_as_string= math.jumpToNextEntry(strengthlist, int(position))
                values_in_value_string=math.convertToList(strength_value_as_string)
                #position=int(values_in_value_string[0])
                strength_number = math.calculateList(values_in_value_string)
                worklist = math.create_number_of_scripts(strength_number,executable_string)
                groupdict = {}
                groupdict.update({i: worklist})
                if position == 288 :
                    positiondict[i]=0
                else :
                    positiondict[i]=position+1
                newconfig.createWorkQ(newconfig.get_queue_name(), groupdict)
                queue = Queues()
            # queue.listenContinouslyToQueue("reportq")
            queue.receiveOneMessageFromQ("webusereportq", newconfig.get_interval())


manager = Httpmanager()
manager.fetchConfig()
