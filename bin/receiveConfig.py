import ast
import pika
from config import *
from ConfigFile import *
import time
def receiveConfig() :
	credentials = pika.PlainCredentials('guest', 'guest')
        connection = pika.BlockingConnection(pika.ConnectionParameters('10.1.0.56',5672, '/', credentials))
        channel=connection.channel() 
        channel.queue_declare(queue='sendconfig')
	method_frame, header_frame, body = channel.basic_get(queue = 'sendconfig')  
	if method_frame.NAME == 'Basic.GetEmpty':
		connection.close()
	else : 
		channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        	connection.close() 
		configdict= ast.literal_eval(body)
		configfile=ConfigFile()
        configfile.writeConfig(configdict)
		#print configdict
		#setConfigDict(configdict)
		    
#def callback(channel, method, properties, body) :
#    configdict= ast.literal_eval(body)
#    setConfigDict(configdict)

#def createConfigObject(configdict) : 
#    #config=Config()
#    configelements=configdict
#    print configelements    
#    for key,value in configelements.iteritems() : 
#        if ("queue") in key : 
#            config.set_quename(value)
#        else :
#            config.set_interval(value)
#    print "quename", config.get_quename()
#    print "interval", config.get_interval()
    
	

def setConfigDict(config) : 
    configdict=config
receiveConfig()
#createConfigObject()
