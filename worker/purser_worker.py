import sys
#sys.path.insert(0, '/root/uptime_challenge_master/testscript')
from purser import *
import pika
import ast
import subprocess
import time
import StringIO


class worker():
    """
    This function is the worker class that listen to the workqueue and executed the job scripts
    """
    groupname = ""

    def fetchJobFromQ(self):
        """
        Listen to the workqueue, perform a job and return the report.
        :return:
        :rtype:
        """

        # do :
        # sloop=False
        while 1:
                credentials = pika.PlainCredentials(***REMOVED***, ***REMOVED***)
                connection = pika.BlockingConnection(pika.ConnectionParameters(***REMOVED***, 5672, '/', credentials))
                channel = connection.channel()
                channel.queue_declare(queue='purserq')
                try:
                    method_frame, header_frame, body = channel.basic_get(queue='purserq')
                    if method_frame.NAME == 'Basic.GetEmpty':
                        connection.close()
                    else:
                        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                        print "Received job:", body, "starting job to reply"
                        self.replyToMaster(body)
                        connection.close()
                        time.sleep(2)
                except AttributeError:
                    print "No content"
                    connection.close()
                    time.sleep(2)



    def doJob(self, variabledict):
        p = Purser()
	filepath=variabledict["filepath"]+variabledict["ip"]+"/"+variabledict["file"]
        dict= p.runPurser(variabledict["ip"], variabledict["file"], filepath, variabledict["sentance"])
        dict.update({"worker": self.getHostName()})
        dict.update({"group": self.get_group_name()})
	p.deleteDirectory("/root/uptime_challenge_master/worker/"+variabledict["ip"])
	#print dict
        return str(dict)

    def replyToMaster(self, content):
        outerdict = ast.literal_eval(content)
	innerdict=outerdict.values()[0]
        self.set_group_name(outerdict.keys()[0])
        message = self.doJob(innerdict)
        #print message
        credentials = pika.PlainCredentials(***REMOVED***, ***REMOVED***)
        connection = pika.BlockingConnection(pika.ConnectionParameters(***REMOVED***, 5672, '/', credentials))
        channel = connection.channel()
        channel.queue_declare(queue="purser_report_q")
        channel.basic_publish(exchange='', routing_key='purser_report_q', body=message)
        connection.close()

    def getcommandoutput(self, command):
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, error) = p.communicate()
        return output


    def runcommand(self, command):
        """
        Execute bash command in python
        :param command:
        :type command:
        :return:
        :rtype:
        """
        subprocess.call(command, shell=True)

    def getHostName(self):
        """
        return the hostname of the worker
        :return:
        :rtype:
        """
        return self.getcommandoutput("hostname").strip("\n")

    def set_group_name(self, name):
        """
        Set groupname to the report.
        :param name:
        :type name:
        :return:
        :rtype:
        """
        self.groupname = name

    def get_group_name(self):
        """
        Return the groupname to the report
        :return:
        :rtype:
        """
        return self.groupname


worker = worker()
worker.fetchJobFromQ()
