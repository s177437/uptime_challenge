import pika
import subprocess
import time
def fetchJobFromQ():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.1.0.56',5672, '/', credentials))
    channel=connection.channel() 
    channel.queue_declare(queue='testq')
    try : 
        method_frame, header_frame, body = channel.basic_get(queue = 'testq')  
        if method_frame.NAME == 'Basic.GetEmpty' :
	    print "You end up here"
            connection.close()
        else : 
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            print "Received job:", body, "starting job to reply"
            replyToMaster(body)
            connection.close() 
            fetchJobFromQ()
    except AttributeError : 
        print "No content"
	time.sleep(2)
	fetchJobFromQ()



def doJob(command):
    outputdata=getcommandoutput(command)
    return outputdata

def replyToMaster(content):
    message=doJob(content)
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.1.0.56',5672, '/', credentials))
    channel = connection.channel() 
    channel.queue_declare(queue="reportq")
    channel.basic_publish(exchange='', routing_key='reportq',body=message)
    connection.close()


def getcommandoutput(self, command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, error) = p.communicate()
    return output

def runcommand(self, command):
    subprocess.call(command, shell=True)

fetchJobFromQ()
