import ast
import pika
from ConfigFile import *
import time

def requestConfig():
	credentials = pika.PlainCredentials('guest', 'guest')
	connection = pika.BlockingConnection(pika.ConnectionParameters('10.1.0.56',5672, '/', credentials))
	channel = connection.channel() 
	channel.queue_declare(queue="requestconfigq")
	channel.basic_publish(exchange='', routing_key='requestconfigq',body="configrequest")
	connection.close()
def receiveConfig() :
	credentials = pika.PlainCredentials('guest', 'guest')
	connection = pika.BlockingConnection(pika.ConnectionParameters('10.1.0.56',5672, '/', credentials))
	channel=connection.channel() 
	channel.queue_declare(queue='sendconfig')
	try : 
		method_frame, header_frame, body = channel.basic_get(queue = 'sendconfig')  
		if method_frame.NAME == 'Basic.GetEmpty' :
			connection.close()
		else : 
			channel.basic_ack(delivery_tag=method_frame.delivery_tag)
			connection.close() 
			configdict= ast.literal_eval(body)
			configfile=bin.ConfigFile()
			configfile.writeConfig(configdict)	
	except AttributeError : 
		print "Waiting for answer.."
		receiveConfig()

requestConfig()
#print "sleeping while waiting for answer"
#time.sleep(5)
receiveConfig()
