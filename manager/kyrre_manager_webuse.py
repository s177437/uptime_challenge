from Queue import *
from Config import *
from WebUseMath import *
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
        math=WebUseMath()
        strengthlist = math.createTimeList()
        position=0
        while True:
            config = Config()
            newconfig = config.initDbConfig()
            userinfo = config.requestUserCreation(newconfig)
            grouplist = newconfig.findGroupnames(newconfig.getAccount().get_groups())
            self.interpreterServer.createAccounts(userinfo)
            path = newconfig.get_script_path()
            # worklist=[path+"traffic.sh 100 10",path+"traffic.sh 100 10"]
            # worklist=["python "+path+ "check_http.py db.no","python "+path+ "check_http.py vg.no", "python "+path+ "check_http.py facebook.com","python "+path+ "check_http.py arngren.net", "python "+path+ "check_http.py db.no","python "+path+ "check_http.py db.no"]
            # worklist = [path + "traffic.sh 100 10"]
            #worklist = [path + "webuse.pl -U 128.39.121.59 -r '10/10/10/10'"]
            executable_string=path + "webuse.pl -U 128.39.121.59 -r '10/10/10/10'"
            index=10
            for i in grouplist:
                content = math.decideEntry(strengthlist,index)
                listvalues = math.convertToList(content)
                position=math.calculateList(listvalues)
                index+=10
            for i in grouplist:
                strength_value_as_string= math.jumpToNextEntry(strengthlist, position)
                values_in_value_string=math.convertToList(strength_value_as_string)
                position=values_in_value_string[0]
                strength_number= math.calculateList(values_in_value_string)
                worklist = math.create_number_of_scripts(strength_number,executable_string)
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
