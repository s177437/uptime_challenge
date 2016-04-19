from Queues import *
from Config import *
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
    # comment
    def fetch_config(self):
        """
        This function is the main method where everything is governed on the manager.
        :return:
        :rtype:
        """
        while True:
            config = Config()
            config.get_account()
            newconfig = config.init_db_config()
            userinfo = config.request_user_creation(newconfig)
            grouplist = newconfig.find_groupnames(newconfig.get_account().get_groups())
            self.interpreterServer.createAccounts(userinfo)
            path = newconfig.get_script_path()
            worklist = ["python " + path + "check_http.py db.no"]
            for i in grouplist:
                groupdict = {}
                groupdict.update({i: worklist})
                newconfig.create_work_queue(newconfig.get_queue_name(), groupdict)
                queue = Queues()
            timestart = time.time()
            while time.time() - timestart <= float(newconfig.get_interval()):
                queue.receive_one_message_from_q("reportq", time.time() - timestart, newconfig.get_interval())


manager = Httpmanager()
manager.fetch_config()
