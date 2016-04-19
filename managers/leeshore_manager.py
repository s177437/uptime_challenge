from Queues import *
from Config import *
import pika
import couchdb
import Pyro4
import logging
import time
import datetime
import sys

__author__ = 'Stian Stroem Anderssen'


class LeeshoreManager():
    """
    This module is the main class for the leeshore manager. This module takes care of the execution of the functions.
    """
    interpreterServer = Pyro4.Proxy("PYRONAME:interpreter")
    # comment
    def run_leeshore(self):
        """
        This function deploys one leeshore-test per user every second hour. s
        :return:
        :rtype:
        """
        day = int(sys.argv[1])
        config = Config()
        newconfig = config.init_db_config()
        grouplist = newconfig.get_account().get_groups()
        path = newconfig.get_script_path()
        runinterval = int(newconfig.get_interval()) / len(grouplist)
        logging.info("Interval: " + str(newconfig.get_interval()))
        positiondict = {}
        while True:
            for i in grouplist:
                userconfig = self.interpreterServer.getUserConfig(i, "couchdb")
                if datetime.datetime.today().weekday() == day or userconfig["leeshore_enabled"] == 0:
                    logging.critical("Today is a day off for leeshore")
                    time.sleep(runinterval)
                else:
                    tenant_name = userconfig["tenant_name"]
                    ip = userconfig["ipaddress"]
                    executable_string = ""
                    executable_string = "/root/uptime_challenge_master/testscript/leeshore_short.pl -n " + tenant_name
                    worklist = []
                    worklist.append(executable_string)
                    groupdict = {}
                    groupdict.update({i: worklist})
                    newconfig.create_work_queue(newconfig.get_queue_name(), groupdict)
                    worklist = []
                    queue = Queues()
                    queue.receive_one_message_from_q("leeshore_reportq", str(runinterval))


manager = LeeshoreManager()
manager.run_leeshore()
