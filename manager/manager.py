from Queue import *
from Config import *
import pika
import couchdb

class Manager():
    def fetchConfig(self):
        worklist=["returnTrue","returnTrue", "returnTrue"]
        queue=Queue()
        config=Config()
        newconfig=config.initDbConfig()
        newconfig.createWorkQ(newconfig.get_queue_name(),worklist)
        queue.listenContinouslyToQueue("reportq")
        
    
manager=Manager()
manager.fetchConfig()        
         
