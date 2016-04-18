from Queues import *
from Config import *
from WebUseMath import *
import pika
import couchdb
import Pyro4
import time
import logging


class Httperfmanager():
    """
    This module is the main class for the httperf manager. This module takes care of the execution of the functions.
    """
    interpreterServer = Pyro4.Proxy("PYRONAME:interpreter")
    logging.basicConfig(filename='/var/log/manager.log',level=logging.DEBUG)

    # comment
    def run_httperf(self):
        """
        This function uses workload-profiles to generate a set of tests per deployment. This manager needs the file
        transsine.dat to successfully execute.
        :return:
        :rtype:
        """	
        math=WebUseMath()
        strengthlist = math.create_time_list()
        position=0
        config = Config()
        newconfig = config.init_db_config()
        grouplist=newconfig.get_account().get_groups()
        path = newconfig.get_script_path()
        executable_string=path + "traffic.sh"

        index=0
        logging.info("Interval: "+ str(newconfig.get_interval()))
        positiondict = {}
        for i in grouplist:
            ip =""
            userconfig = self.interpreterServer.getFileAndOffsetFromUser(i)
            ipconfig = self.interpreterServer.getIpFromUser(i)
            ip=ipconfig["ipaddress"]
            index = int(userconfig["offset"])
            logging.info("INDEX: "+ str(index))
            content = math.decide_entry(strengthlist,index)
            worklist=[]
            listvalues = math.convert_to_list(content)
            position= int(listvalues[0])
            logging.info("USER: "+ str(i)+" POSITION: "+ str(position))
            strength_number=math.calculatelist(listvalues)
            worklist = math.create_httperf_executable_string(ip, strength_number,executable_string)
            groupdict = {}
            groupdict.update({i: worklist})
            newconfig.create_work_queue(newconfig.get_queue_name(), groupdict)
            worklist = []
            positiondict.update({i:position})
        while True:
            for i, position in positiondict.iteritems():
                logging.info("USER: "+ str(i)+" POSITION: "+ str(position))
                ip =""
                ipconfig = self.interpreterServer.getIpFromUser(i)
                ip=ipconfig["ipaddress"]
                strength_value_as_string= math.jump_to_next_entry(strengthlist, int(position))
                values_in_value_string=math.convert_to_list(strength_value_as_string)
                strength_number = math.calculatelist(values_in_value_string)
                worklist = math.create_httperf_executable_string(ip, strength_number,executable_string)
                groupdict = {}
                groupdict.update({i: worklist})
                if position == 288 :
                    positiondict[i]=0
                else :
                    positiondict[i]=position+1
                newconfig.create_work_queue(newconfig.get_queue_name(), groupdict)
                queue = Queues()
            queue.receive_one_message_from_q("httperfreportq", newconfig.get_interval())


manager = Httperfmanager()
manager.run_httperf()
