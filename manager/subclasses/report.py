'''
Created on 1. sep. 2015

@author: stianstrom
'''
from queue import *
class Report():
    queue = Queue()
    
    
    def createReportQueue(self, queuename,content):
        self.queue.createQueue(queuename, content)
    
    
    