from Queues import *
from Config import *
from WebUseMath import *
import pika
import couchdb
import Pyro4
import logging
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
        config = Config()
        newconfig = config.initDbConfig()
	#print str(newconfig.get_interval())
        #grouplist = newconfig.findGroupnames(newconfig.getAccount().get_groups())
        #grouplist=newconfig.getAllUsersFromCouchDB()
        grouplist=newconfig.getAccount().get_groups()
        path = newconfig.get_script_path()
        logging.info("Interval: "+str(newconfig.get_interval()))
        positiondict = {}
        while True:
            for i in grouplist:
                userconfig = self.interpreterServer.getUserConfig(i,"couchdb")
                ip=userconfig["ipaddress"]
                worklist=[]
                worklist = [{"ip":ip,"sentance":userconfig["Sentance"],"filepath":userconfig["filepath"],"file":userconfig["file"],"timestamp":time.time()}]
                groupdict = {}
                groupdict.update({i: worklist})
                newconfig.createWorkQ(newconfig.get_queue_name(), groupdict)
                worklist = []
            queue = Queues()
	    #print newconfig.get_interval()
            queue.receiveOneMessageFromQ("purser_report_q", str(newconfig.get_interval()))


manager = Httpmanager()
manager.fetchConfig()
