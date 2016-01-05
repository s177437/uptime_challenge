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
        config = Config()
        newconfig = config.initDbConfig()
        userinfo = config.requestUserCreation(newconfig)
        grouplist = newconfig.findGroupnames(newconfig.getAccount().get_groups())
        self.interpreterServer.createAccounts(userinfo)
        path = newconfig.get_script_path()
        executable_string=path + "traffic.sh"
        #ip="128.39.121.59"
        #executable_string=path + "webuse.pl -U 128.39.121.59 -r '10/10/10/10'"
        index=0
        print "Interval",newconfig.get_interval()
        positiondict = {}
        for i in grouplist:
            userconfig = self.interpreterServer.getFileAndOffsetFromUser(i)
            print userconfig
            ipconfig = self.interpreterServer.getIpFromUser(i)
            ip=ipconfig["ipaddress"]
            index = int(userconfig["offset"])
            print "INDEX", index
            content = math.decideEntry(strengthlist,index)
            worklist=[]
            listvalues = math.convertToList(content)
            position= int(listvalues[0])
            print "USEREN:", i,"POSITION", position
            strength_number=math.calculateList(listvalues)
            worklist = math.create_HttperfExecutableString(ip, strength_number,executable_string)
            groupdict = {}
            groupdict.update({i: worklist})
            newconfig.createWorkQ(newconfig.get_queue_name(), groupdict)
            worklist = []
            positiondict.update({i:position})
        while True:
            for i, position in positiondict.iteritems():
                print "USER:", i,"POSITION", position
                strength_value_as_string= math.jumpToNextEntry(strengthlist, int(position))
                values_in_value_string=math.convertToList(strength_value_as_string)
                #position=int(values_in_value_string[0])
                strength_number = math.calculateList(values_in_value_string)
                worklist = math.create_HttperfExecutableString(ip, strength_number,executable_string)
                groupdict = {}
                groupdict.update({i: worklist})
                if position == 288 :
                    positiondict[i]=0
                else :
                    positiondict[i]=position+1
                newconfig.createWorkQ(newconfig.get_queue_name(), groupdict)
                queue = Queue()
            # queue.listenContinouslyToQueue("reportq")
            queue.receiveOneMessageFromQ("reportq", newconfig.get_interval())


manager = Httpmanager()
manager.fetchConfig()
