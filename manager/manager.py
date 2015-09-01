from Queue import *
from Config import *

import pika
import couchdb

class Manager():
    def fetchConfig(self):
        queue=Queue()
        config=Config()
        config.initDbConfig()
        
        
        
         