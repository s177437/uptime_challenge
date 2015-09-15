from Queue import *
from Config import *
import pika
import couchdb
import Pyro4

class Manager():
    interpreterServer=Pyro4.Proxy("PYRONAME:interpreter")
    def fetchConfig(self):
        queue=Queue()
        worklist=["python /root/uptime_challenge_master/testscript/check_http.py db.no","python /root/uptime_challenge_master/testscript/check_http.py vg.no", "python /root/uptime_challenge_master/testscript/check_http.py facebook.com","python /root/uptime_challenge_master/testscript/check_http.py arngren.net", "python /root/uptime_challenge_master/testscript/check_http.py db.no","python /root/uptime_challenge_master/testscript/check_http.py db.no"]
        config=Config()
        newconfig=config.initDbConfig()
        userinfo=config.requestUserCreation(newconfig)
        print userinfo
        self.interpreterServer.createAccounts(userinfo)
        newconfig.createWorkQ(newconfig.get_queue_name(),worklist)
        queue.listenContinouslyToQueue("reportq")
        
    
manager=Manager()
manager.fetchConfig()        
         
