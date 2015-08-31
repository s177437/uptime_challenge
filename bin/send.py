import pika 
import sys


def connect(message) : 
	credentials = pika.PlainCredentials('guest', 'guest')
	connection = pika.BlockingConnection(pika.ConnectionParameters('10.1.0.56',5672, '/', credentials))
	channel = connection.channel() 
	channel.queue_declare(queue="stianstestq")
	channel.basic_publish(exchange='', routing_key='stianstestq',body=message)
	print message
	connection.close()
def addConfigToCouch() : 
	configdict=["{'queue_names':'testq'}","{'interval':'2'}"]
	for c in configdict :  
		connect(c)
addConfigToCouch()
	 
