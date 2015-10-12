from Queue import *
from Config import *
import pika
import couchdb
import Pyro4
import time
import random


class Manager():
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
        interval = 0
        intervaltime = 900
        time_of_day = random.uniform(-12, 12)
        while True:
            if time_of_day > 12:
                time_of_day -= 24
            print time_of_day
            config = Config()
            config.getAccount()
            newconfig = config.initDbConfig()
            interval = newconfig.get_interval()
            userinfo = config.requestUserCreation(newconfig)
            grouplist = newconfig.findGroupnames(newconfig.getAccount().get_groups())
            self.interpreterServer.createAccounts(userinfo)
            path = newconfig.get_script_path()
            hour = 0
            fetchload = []
            # worklist = ["python " + path + "check_http.py db.no"]
            while (hour < 3600):
                fetchload = newconfig.returnLoad(time_of_day)
                currentload = float(fetchload[0])
                #print currentload
                loadincrease = float(fetchload[1]) / 10
                time_elapsed = 0
                worklist = [path + "traffic.sh " + str((currentload * 30)) + " " + str(currentload)]
                while (time_elapsed < 900):
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
                    if currentload + loadincrease < 0:
                        loadincrease *= (-1)
                    currentload += loadincrease
                    worklist = [path + "traffic.sh " + str((currentload * 30)) + " " + str(currentload)]
                    time_elapsed += float(interval)
                    hour += float(interval)
                time_of_day += (1 / 96)


manager = Manager()
manager.fetchConfig()
