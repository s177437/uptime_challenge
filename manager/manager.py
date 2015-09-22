from Queue import *
from Config import *
import pika
import couchdb
import Pyro4
import time

class Manager():
    interpreterServer=Pyro4.Proxy("PYRONAME:interpreter")
#comment
    def fetchConfig(self):
        while True :
            queue=Queue()
            #queue.setTime(time.time())
            config=Config()
            config.getAccount()
            newconfig=config.initDbConfig()
            userinfo=config.requestUserCreation(newconfig)
            grouplist= newconfig.findGroupnames(newconfig.getAccount().get_groups())
            self.interpreterServer.createAccounts(userinfo)
            path = newconfig.get_script_path()
            #worklist=[path+"traffic.sh 100 10",path+"traffic.sh 100 10"]
            #worklist=["python "+path+ "check_http.py db.no","python "+path+ "check_http.py vg.no", "python "+path+ "check_http.py facebook.com","python "+path+ "check_http.py arngren.net", "python "+path+ "check_http.py db.no","python "+path+ "check_http.py db.no"]
            worklist=[path+"traffic.sh 100 10"]
            for i in grouplist :
                groupdict={}
                groupdict.update({i:worklist})
                newconfig.createWorkQ(newconfig.get_queue_name(),groupdict)
            queue.listenContinouslyToQueue("reportq")
        
    
manager=Manager()
manager.fetchConfig()
         
