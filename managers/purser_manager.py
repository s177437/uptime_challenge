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
    This module is the main class for the purser manager. One test is deployed for each user per deployment.
    """
    interpreterServer = Pyro4.Proxy("PYRONAME:interpreter")
    logging.basicConfig(filename='/var/log/manager.log', level=logging.CRITICAL)

    # comment
    def fetchConfig(self):
        """
        This function is the main method where everything is governed on the manager.
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
                worklist = [{"ip": ip, "sentance": userconfig["Sentance"], "filepath": userconfig["filepath"],
                             "file": userconfig["file"], "timestamp": time.time()}]
                groupdict = {}
                groupdict.update({i: worklist})
                logging.critical(str(i) + " " + str(worklist))
                newconfig.create_work_queue(newconfig.get_queue_name(), groupdict)
                worklist = []
            queue = Queues()
            queue.receive_one_message_from_q("purser_report_q", str(newconfig.get_interval()))


manager = Httpmanager()
manager.fetchConfig()
