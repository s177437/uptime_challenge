import pika
import ast
import subprocess
import time
import StringIO

__author__ = 'Stian Stroem Anderssen'


class Worker():
    """
    This is a template class for future workers.
    """
    groupname = ""

    def fetch_job_from_queue(self):
        """
        Listen to the workqueue, perform a job and return the report.
        :return:
        :rtype:
        """
        credentials = pika.PlainCredentials('guest', 'guest')
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', credentials))
        channel = connection.channel()
        channel.queue_declare(queue='testq')
        try:
            method_frame, header_frame, body = channel.basic_get(queue='testq')
            if method_frame.NAME == 'Basic.GetEmpty':
                print "You end up here"
                connection.close()
            else:
                channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                print "Received job:", body, "starting job to reply"
                self.reply_to_master(body)
                connection.close()
                self.fetch_job_from_queue()
        except AttributeError:
            print "No content"
            time.sleep(2)
            self.fetch_job_from_queue()

    def do_job(self, command):
        """
        Execute job and create report
        :param command:
        :type command:
        :return:
        :rtype:
        """
        outputdata = self.get_command_output(command)
        try:
            dict = ast.literal_eval(outputdata)
            dict.update({"WebuseWorker": self.get_host_name()})
            dict.update({"group": self.get_group_name()})
            return str(dict)
        except SyntaxError:
            print "This is not a dict"
            dict = self.convert_output_to_dict(outputdata)
            dict.update({"WebuseWorker": self.get_host_name()})
            dict.update({"group": self.get_group_name()})
            return str(dict)

    @staticmethod
    def reply_to_master(self, content):
        """
        Post report to queue
        :param content:
        :type content:
        :return:
        :rtype:
        """
        dict = ast.literal_eval(content)
        job = dict.values()[0]
        self.set_group_name(dict.keys()[0])
        message = self.do_job(job)
        print message
        credentials = pika.PlainCredentials('USER', 'PASSWORD')
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', credentials))
        channel = connection.channel()
        channel.queue_declare(queue="reportq")
        channel.basic_publish(exchange='', routing_key='reportq', body=message)
        connection.close()

    @staticmethod
    def get_command_output(self, command):
        """
        Execute bash-command and save output
        :param command:
        :type command:
        :return:
        :rtype:
        """
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, error) = p.communicate()
        return output

    @staticmethod
    def convert_output_to_dict(self, content):
        """
        Convert test result to a dictionary
        :param content:
        :type content:
        :return:
        :rtype:
        """
        buf = StringIO.StringIO(content.strip("\n"))
        templist = []
        list = []
        reportdict = {}
        for i in buf.readlines():
            if " " in i[0]:
                nolines = ""
            else:
                templist.append(i)
        for i in templist:
            content = i.replace("\n", "")
            if content != "":
                list.append(content)
        for i in list:
            j = i.split(":")
            if len(j) == 1:
                reportdict.update({"message": j[0]})
            elif len(j) == 2:
                reportdict.update({j[0]: j[1]})
        return reportdict

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
        return self.get_command_output("hostname").strip("\n")

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


worker = Worker()
worker.fetch_job_from_queue()
