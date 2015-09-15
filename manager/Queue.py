import pika
from Report import *
'''
Created on 1. sep. 2015

@author: stianstrom
'''

class Queue():
    '''
    classdocs
    '''
    queuename=""
    queuecontent=""
    def setQueueContent(self,value): 
        self.queuecontent=value
    def getQueueContent(self):
        return self.queuecontent
    def connectToRabbitMQ(self):
        credentials = pika.PlainCredentials('guest', 'guest')
        connection = pika.BlockingConnection(pika.ConnectionParameters('10.1.0.56',5672, '/', credentials))
        return connection
    
    def createQueue(self, quename,content):
        connection = self.connectToRabbitMQ()
        channel = connection.channel() 
        channel.queue_declare(queue=quename)
        channel.basic_publish(exchange='', routing_key=quename,body=content)
        connection.close()
    
    def listenContinouslyToQueue(self, quename):
        connection=self.connectToRabbitMQ()
        channel=connection.channel() 
        channel.queue_declare(queue=quename)
        channel.basic_consume(self.callback, queue=quename, no_ack=True)
        channel.start_consuming()
    
    def callback(self,channel, method, properties, body) :
        #print "Status for job:", body
        report = Report()
        report.buildReport(body)
        #create report
    
    def receiveOneMessageFromQ(self,queuename):
        stringValue=""
        connection=self.connectToRabbitMQ()
        channel=connection.channel() 
        channel.queue_declare(queue=queuename)
        try : 
            method_frame, header_frame, body = channel.basic_get(queue = queuename)  
            if method_frame.NAME == 'Basic.GetEmpty' :
                connection.close()
            else : 
                channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                connection.close() 
                self.setQueueContent(body)
                
        except AttributeError : 
            print "Waiting for answer.."
            self.receiveOneMessageFromQ(queuename)
    
        
        
