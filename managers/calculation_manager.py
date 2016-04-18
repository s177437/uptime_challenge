from Queues import *
from Config import *
import pika
import couchdb
import Pyro4
import time
import random


class Manager():
    """
     A sample manager that can be used to deploy jobs by using a mathematical formula.
    """
    interpreterServer = Pyro4.Proxy("PYRONAME:interpreter")
    # comment
    def run_manager(self):
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
            config.get_account()
            newconfig = config.init_db_config()
            interval = newconfig.get_interval()
            userinfo = config.request_user_creation(newconfig)
            grouplist = newconfig.find_groupnames(newconfig.get_account().get_groups())
            self.interpreterServer.createAccounts(userinfo)
            path = newconfig.get_script_path()
            hour = 0
            fetchload = []
            while (hour < 3600):
                fetchload = newconfig.return_load(time_of_day)
                currentload = float(fetchload[0])
                # print currentload
                loadincrease = float(fetchload[1]) / 10
                time_elapsed = 0
                worklist = [path + "traffic.sh " + str((int(currentload) * 5)) + " " + str(int(currentload))]
                while (time_elapsed < 900):
                    for i in grouplist:
                        groupdict = {}
                        groupdict.update({i: worklist})
                        newconfig.create_work_queue(newconfig.get_queue_name(), groupdict)
                        queue = Queues()
                    # queue.listenContinouslyToQueue("reportq")
                    timestart = time.time()
                    while (time.time() - timestart <= float(newconfig.get_interval())):
                        print time.time() - timestart
                        queue.receiveOneMessageFromQ("reportq", (time.time() - timestart), newconfig.get_interval())
                    if currentload + loadincrease < 0:
                        loadincrease *= (-1)
                    currentload += loadincrease
                    worklist = [path + "traffic.sh " + str((int(currentload) * 5)) + " " + str(int(currentload))]
                    time_elapsed += float(interval)
                    hour += float(interval)
                time_of_day += (24. / 96)


manager = Manager()
manager.run_manager()
