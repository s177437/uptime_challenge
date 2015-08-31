import ast
import pika
from config import *
import time
configdict={}
def receiveConfig() :
    start_time=time.time() 
    while (time.time()-start_time<=10.0) : 
        credentials = pika.PlainCredentials('guest', 'guest')
        connection = pika.BlockingConnection(pika.ConnectionParameters('10.1.0.56',5672, '/', credentials))
        channel=connection.channel() 
        channel.queue_declare(queue='sendconfig')
        channel.basic_consume(callback, queue='sendconfig', no_ack=True)
        channel.start_consuming()
    
def callback(channel, method, properties, body) :
    configdict= ast.literal_eval(body)
    setConfigDict(configdict)

    

def createConfigObject() : 
    config=Config()
    configelements=getConfigDict()
    
    for key,value in configelements.iteritems() : 
        if ("queue") in key : 
            config.set_quename(value)
        else :
            config.set_interval(value)
    print "quename", config.get_quename()
    print "interval", config.get_interval()
    
	
def getConfigDict():
    return configdict
def setConfigDict(config) : 
    configdict=config
receiveConfig()
createConfigObject()