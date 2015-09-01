from subclasses import Queue
from subclasses import Config
import pika
import couchdb

class Manager():
    def fetchConfig(self):
        queue=Queue()
        config=Config()
        config.initDbConfig()
        
        
        
         