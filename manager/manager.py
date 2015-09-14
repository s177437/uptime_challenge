from Queue import *
from Config import *
import pika
import couchdb

class Manager():
    def fetchConfig(self):
        #worklist=["returnTrue","returnTrue", "returnTrue","returnTrue", "returnTrue", "returnTrue"]
        config=Config()
        newconfig=config.initDbConfig()
        #queue.createQueue("mainq", "account_manager")
        #usercontent=config.requestUserCreation(newconfig)
        #config.sendUsersToQueue(usercontent)
        #newconfig.createWorkQ(newconfig.get_queue_name(),worklist)
        #queue.listenContinouslyToQueue("reportq")
        print ""
        
    
manager=Manager()
manager.fetchConfig()        
         
