import pika
import ast
import subprocess
import time
class worker () :
    groupname=""

    def fetchJobFromQ(self):
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
                self.replyToMaster(body)
                connection.close()
                self.fetchJobFromQ()
        except AttributeError :
            print "No content"
            time.sleep(2)
            self.fetchJobFromQ()



    def doJob(self,command):
        outputdata= self.getcommandoutput(command)
        dict=ast.literal_eval(outputdata)
        dict.update({"worker": self.getHostName()})
        dict.update({"group":self.get_group_name()})
        return str(dict)

    def replyToMaster(self,content):
        dict=ast.literal_eval(content)
        job=dict.values()[0]
        self.set_group_name(dict.keys()[0])
        message=self.doJob(job)
        print message
        credentials = pika.PlainCredentials('guest', 'guest')
        connection = pika.BlockingConnection(pika.ConnectionParameters('10.1.0.56',5672, '/', credentials))
        channel = connection.channel()
        channel.queue_declare(queue="reportq")
        channel.basic_publish(exchange='', routing_key='reportq',body=message)
        connection.close()


    def getcommandoutput(self,command):
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, error) = p.communicate()
        return output

    def runcommand(self, command):
        subprocess.call(command, shell=True)
    def getHostName(self) :
        return self.getcommandoutput("hostname").strip("\n")
    def set_group_name(self, name) :
        self.groupname=name
    def get_group_name(self) :
        return self.groupname
worker= worker()
worker.fetchJobFromQ()
