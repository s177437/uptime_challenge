from Queue import *
from Config import *
import pika
import couchdb
import Pyro4

class Manager():
    interpreterServer=Pyro4.Proxy("PYRONAME:interpreter")
    def fetchConfig(self):
        queue=Queue()
        path="/root/uptime_challenge_master/testscript/"
        worklist=["python "+path+ "check_http.py db.no","python "+path+ "check_http.py vg.no", "python "+path+ "check_http.py facebook.com","python "+path+ "check_http.py arngren.net", "python "+path+ "check_http.py db.no","python "+path+ "check_http.py db.no"]
        config=Config()
        config.getAccount()
        newconfig=config.initDbConfig()
        userinfo=config.requestUserCreation(newconfig)
        grouplist= newconfig.findGroupnames(newconfig.getAccount().get_groups())
        self.interpreterServer.createAccounts(userinfo)
        for i in grouplist :
            newconfig.createWorkQ(newconfig.get_queue_name(),worklist)
        queue.listenContinouslyToQueue("reportq")
        
    
manager=Manager()
manager.fetchConfig()        
         
