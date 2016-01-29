from Queues import *
from Config import *
import pika
import couchdb
import Pyro4
import logging
import time
import datetime
import sys


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
        day=int(sys.argv[1])
        config = Config()
        newconfig = config.initDbConfig()
        grouplist=newconfig.getAccount().get_groups()
        path = newconfig.get_script_path()
        runinterval=int(newconfig.get_interval())/len(grouplist)
        logging.info("Interval: "+str(newconfig.get_interval()))
        positiondict = {}
        while True:
            for i in grouplist: 
                if datetime.datetime.today().weekday() == day : 
                    print "Today is a day of for leeshore"
                    time.sleep(runinterval)
                else: 
                    userconfig = self.interpreterServer.getUserConfig(i,"couchdb")
                    tenant_name=userconfig["tenant_name"]
                    ip=userconfig["ipaddress"]
                    executable_string=""
                    executable_string="/root/uptime_challenge_master/testscript/leeshore_short.pl -n "+tenant_name
                    worklist=[]
                    worklist.append(executable_string)
                    print worklist
                    groupdict = {}
                    groupdict.update({i: worklist})
                    newconfig.createWorkQ(newconfig.get_queue_name(), groupdict)
                    worklist = []
                    queue = Queues()
                    queue.receiveOneMessageFromQ("leeshore_reportq", str(runinterval))


manager = Httpmanager()
manager.fetchConfig()
