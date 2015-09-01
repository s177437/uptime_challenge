import pika

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
            print "Received job:", body
            connection.close() 
            fetchJobFromQ()
    except AttributeError : 
        print "No message has not arrived yet"
	fetchJobFromQ()

def doJob():
    return "True"
fetchJobFromQ()
