from Queue import *
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
            config.getAccount()
            newconfig = config.initDbConfig()
            userinfo = config.requestUserCreation(newconfig)
            grouplist = newconfig.findGroupnames(newconfig.getAccount().get_groups())
            self.interpreterServer.createAccounts(userinfo)
            path = newconfig.get_script_path()
            # worklist=[path+"traffic.sh 100 10",path+"traffic.sh 100 10"]
            # worklist=["python "+path+ "check_http.py db.no","python "+path+ "check_http.py vg.no", "python "+path+ "check_http.py facebook.com","python "+path+ "check_http.py arngren.net", "python "+path+ "check_http.py db.no","python "+path+ "check_http.py db.no"]
            # worklist = [path + "traffic.sh 100 10"]
            worklist = ["python " + path + "check_http.py db.no"]
            for i in grouplist:
                groupdict = {}
                groupdict.update({i: worklist})
                newconfig.createWorkQ(newconfig.get_queue_name(), groupdict)
                queue = Queue()
            # queue.listenContinouslyToQueue("reportq")
            timestart = time.time()
            while (time.time() - timestart <= float(newconfig.get_interval())):
                print time.time() - timestart
                queue.receiveOneMessageFromQ("reportq", (time.time() - timestart), newconfig.get_interval())


manager = Httpmanager()
manager.fetchConfig()