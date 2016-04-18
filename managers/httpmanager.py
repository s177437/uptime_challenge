from Queues import *
from Config import *
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
        while True:
            config = Config()
            config.get_account()
            newconfig = config.init_db_config()
            userinfo = config.request_user_creation(newconfig)
            grouplist = newconfig.find_groupnames(newconfig.get_account().get_groups())
            self.interpreterServer.createAccounts(userinfo)
            path = newconfig.get_script_path()
            # worklist=[path+"traffic.sh 100 10",path+"traffic.sh 100 10"]
            # worklist=["python "+path+ "check_http.py db.no","python "+path+ "check_http.py vg.no", "python "+path+ "check_http.py facebook.com","python "+path+ "check_http.py arngren.net", "python "+path+ "check_http.py db.no","python "+path+ "check_http.py db.no"]
            # worklist = [path + "traffic.sh 100 10"]
            worklist = ["python " + path + "check_http.py db.no"]
            print worklist
            for i in grouplist:
                groupdict = {}
                groupdict.update({i: worklist})
                newconfig.create_work_queue(newconfig.get_queue_name(), groupdict)
                queue = Queues()
            # queue.listen_continously_to_queue("reportq")
            timestart = time.time()
            while (time.time() - timestart <= float(newconfig.get_interval())):
                print time.time() - timestart
                queue.receive_one_message_from_q("reportq", (time.time() - timestart), newconfig.get_interval())


manager = Httpmanager()
manager.fetchConfig()
