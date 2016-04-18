from Queues import *
from Config import *
from WebUseMath import *
import pika
import couchdb
import Pyro4
import logging
import time


class ClerkManager():
    """
    This module is the main class for the clerk manager. This module takes care of the execution of the functions.
    """
    interpreterServer = Pyro4.Proxy("PYRONAME:interpreter")
    logging.basicConfig(filename='/var/log/manager.log', level=logging.CRITICAL)

    # comment
    def run_clerk(self):
        """
       This function deploys one test per user by creating an executable string which is sent to the RabbitMQ instance.
        :return:
        :rtype:
        """
        math = WebUseMath()
        config = Config()
        newconfig = config.init_db_config()
        grouplist = newconfig.get_account().get_groups()
        path = newconfig.get_script_path()
        logging.info("Interval: " + str(newconfig.get_interval()))
        positiondict = {}
        while True:
            for i in grouplist:
                userconfig = self.interpreterServer.getUserConfig(i, "couchdb")
                ip = userconfig["ipaddress"]
                worklist = []
                tenant_name = userconfig["tenant_name"]
                executable_string = "/root/uptime_challenge_master/testscript/clerk.pl -n " + tenant_name
                worklist.append(executable_string)
                groupdict = {}
                groupdict.update({i: worklist})
                logging.critical(str(i) + " " + str(worklist))
                newconfig.create_work_queue(newconfig.get_queue_name(), groupdict)
                worklist = []
            queue = Queues()
            queue.receiveOneMessageFromQ("clerk_reportq", str(newconfig.get_interval()))


manager = ClerkManager()
manager.run_clerk()
