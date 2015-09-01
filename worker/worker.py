import pika

def fetchJobFromQ():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.1.0.56',5672, '/', credentials))
    channel=connection.channel() 
    channel.queue_declare(queue='testq')
    try : 
        method_frame, header_frame, body = channel.basic_get(queue = 'testq')  
        if method_frame.NAME == 'Basic.GetEmpty' :
            connection.close()
        else : 
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            if "configrequest" in body :
                print "Received job:", body, "doing job"
            connection.close() 
    except AttributeError : 
        print "No message has not arrived yet"

def doJob():
    return "True"