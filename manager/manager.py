from Queue import *
from Config import *
import pika
import couchdb

class Manager():
    def fetchConfig(self):
        queue=Queue()
        config=Config()
        newconfig=config.initDbConfig()
        print newconfig.get_queue_name()
        
        
manager=Manager()
manager.fetchConfig()        
         
