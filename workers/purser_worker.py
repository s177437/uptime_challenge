import sys
# sys.path.insert(0, '/root/uptime_challenge_master/testscript')
from purser import *
import pika
import ast
import subprocess
import time
import StringIO

__author__ = 'Stian Stroem Anderssen'


class PurserWorker():
    """
    This is the purser-worker class.
    """
    groupname = ""

    def fetch_job_from_queue(self):
        """
        Listen to the workqueue, perform a job and return the report.
        :return:
        :rtype:
        """
        while 1:
            time.sleep(2)
            try:
                credentials = pika.PlainCredentials('USER', 'PASSWORD')
                connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', credentials))
                channel = connection.channel()
                channel.queue_declare(queue='purserq')
                method_frame, header_frame, body = channel.basic_get(queue='purserq')
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

    def do_job(self, variabledict):
        """
        Execute the purser-test by calling the purser check
        :param variabledict:
        :type variabledict:
        :return:
        :rtype:
        """
        p = Purser()
        filepath = variabledict["filepath"] + variabledict["ip"] + "/" + variabledict["file"]
        dict = p.run_purser(variabledict["ip"], variabledict["file"], filepath, variabledict["sentance"])
        dict.update({"worker": self.get_host_name()})
        dict.update({"group": self.get_group_name()})
        p.delete_directory("/root/uptime_challenge_master/worker/" + variabledict["ip"])
        return str(dict)

    @staticmethod
    def reply_to_master(self, content):
        """
        Send the report back to the report-queue
        :param content:
        :type content:
        :return:
        :rtype:
        """
        outerdict = ast.literal_eval(content)
        innerdict = outerdict.values()[0]
        self.set_group_name(outerdict.keys()[0])
        message = self.do_job(innerdict)
        credentials = pika.PlainCredentials('USER', 'PASSWORD')
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', credentials))
        channel = connection.channel()
        channel.queue_declare(queue="purser_report_q")
        channel.basic_publish(exchange='', routing_key='purser_report_q', body=message)
        connection.close()

    @staticmethod
    def get_command_output(self, command):
        """
        Execute bash command and save output
        :param command:
        :type command:
        :return:
        :rtype:
        """
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, error) = p.communicate()
        return output

    @staticmethod
    def run_command(self, command):
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
        return the hostname of the WebuseWorker
        :return:
        :rtype:
        """
        return self.get_command_output("hostname").strip("\n")

    def set_group_name(self, name):
        """
        Set groupname of the report.
        :param name:
        :type name:
        :return:
        :rtype:
        """
        self.groupname = name

    def get_group_name(self):
        """
        Return the groupname to the report
        :return groupname:
        :rtype:
        """
        return self.groupname


worker = PurserWorker()
worker.fetch_job_from_queue()
