import pika
import ast
import subprocess
import time
import StringIO

__author__ = 'Stian Stroem Anderssen'


class LeeshoreWorker():
    """
    This is the leeshore-worker class.
    """
    groupname = ""

    def fetch_job_from_queue(self):
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
                credentials = pika.PlainCredentials('USER', 'PASSWORD')
                connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', credentials))
                channel = connection.channel()
                channel.queue_declare(queue='leeshoreq')
                method_frame, header_frame, body = channel.basic_get(queue='leeshoreq')
                if method_frame.NAME == 'Basic.GetEmpty':
                    connection.close()
                else:
                    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                    print "Received job:", body, "starting job to reply"
                    connection.close()
                    self.reply_to_master(body)
            except AttributeError:
                print "No content"
                connection.close()
            except pika.exceptions.ConnectionClosed:
                print "You get Connection Closed"
                continue

    def do_job(self, command):
        outputdata = self.getcommandoutput(command)
        try:
            dict = ast.literal_eval(outputdata)
            dict.update({"worker": self.get_host_name()})
            dict.update({"group": self.get_group_name()})
            return str(dict)
        except SyntaxError:
            print "This is not a dict"
            dict = self.convert_output_to_dict(outputdata)
            dict.update({"worker": self.get_host_name()})
            dict.update({"group": self.get_group_name()})
            return str(dict)

    def reply_to_master(self, content):
        dict = ast.literal_eval(content)
        job = dict.values()[0]
        self.set_group_name(dict.keys()[0])
        message = self.do_job(job)
        print message
        credentials = pika.PlainCredentials('USER', 'PASSWORD')
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', credentials))
        channel = connection.channel()
        channel.queue_declare(queue="leeshore_reportq")
        channel.basic_publish(exchange='', routing_key='leeshore_reportq', body=message)
        connection.close()

    @staticmethod
    def getcommandoutput(self, command):
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, error) = p.communicate()
        return output

    @staticmethod
    def runcommand(self, command):
        """
        Execute bash command in python
        :param command:
        :type command:
        :return:
        :rtype:
        """
        subprocess.call(command, shell=True)

    def get_host_name(self):
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


worker = LeeshoreWorker()
worker.fetch_job_from_queue()
