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
            time.sleep(2)
            try:
                credentials = pika.PlainCredentials(***REMOVED***, ***REMOVED***)
                connection = pika.BlockingConnection(pika.ConnectionParameters(***REMOVED***, 5672, '/', credentials))
                channel = connection.channel()
                channel.queue_declare(queue='clerkq')
                method_frame, header_frame, body = channel.basic_get(queue='clerkq')
                if method_frame.NAME == 'Basic.GetEmpty':
                    connection.close()
                else:
                    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                    print "Received job:", body, "starting job to reply"
                    connection.close()
                    self.replyToMaster(body)
            except AttributeError:
                print "No content"
                connection.close()
            except pika.exceptions.ConnectionClosed :
                print "You get Connection Closed"
                continue


    def doJob(self, command):
        outputdata = self.getcommandoutput(command)
        try:
            dict = ast.literal_eval(outputdata)
            dict.update({"worker": self.getHostName()})
            dict.update({"group": self.get_group_name()})
            return str(dict)
        except SyntaxError:
            print "This is not a dict"
            dict = self.convertOutPutToDict(outputdata)
            dict.update({"worker": self.getHostName()})
            dict.update({"group": self.get_group_name()})
            return str(dict)

    def replyToMaster(self, content):
        dict = ast.literal_eval(content)
        job = dict.values()[0]
        self.set_group_name(dict.keys()[0])
        message = self.doJob(job)
        print message
        credentials = pika.PlainCredentials(***REMOVED***, ***REMOVED***)
        connection = pika.BlockingConnection(pika.ConnectionParameters(***REMOVED***, 5672, '/', credentials))
        channel = connection.channel()
        channel.queue_declare(queue="clerk_reportq")
        channel.basic_publish(exchange='', routing_key='clerk_reportq', body=message)
        connection.close()

    def getcommandoutput(self, command):
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, error) = p.communicate()
        return output

    def convertOutPutToDict(self, content):
        """
        Convert test result to a dictionary
        :param content:
        :type content:
        :return:
        :rtype:
        """
        reportdict={}
        reportdict.update({"Message": "Something went very vrong"})
        return reportdict

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