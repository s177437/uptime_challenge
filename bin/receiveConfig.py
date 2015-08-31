import ast
import pika
from Config import *
configdict={}
def receiveConfig() : 
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.1.0.56',5672, '/', credentials))
    channel=connection.channel() 
    channel.queue_declare(queue='sendconfig')
    channel.basic_consume(callback, queue='sendconfig', no_ack=True)
    channel.start_consuming()

def callback(channel, method, properties, body) :
    configdict= ast.literal_eval(body)
    print configdict 
def getConfig():
    return configdict

receiveConfig()
