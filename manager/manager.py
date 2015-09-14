from Queue import *
from Config import *
import pika
import couchdb
import Pyro4

class Manager():
    interpreterServer=Pyro4.Proxy("PYRONAME:interpreter")
    def fetchConfig(self):
        #worklist=["returnTrue","returnTrue", "returnTrue","returnTrue", "returnTrue", "returnTrue"]
        config=Config()
        newconfig=config.initDbConfig()
        userinfo=config.requestUserCreation(newconfig)
        print self.interpreterServer.createAccounts(userinfo)
        #newconfig.createWorkQ(newconfig.get_queue_name(),worklist)
        #queue.listenContinouslyToQueue("reportq")
        
    
manager=Manager()
manager.fetchConfig()        
         
