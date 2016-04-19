import pika
import ast
import subprocess
import time
import StringIO

__author__ = 'Stian Stroem Anderssen'

class HttperfWorker():
    """
    This is the httperf-worker class
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
                channel.queue_declare(queue='httperfq')
                method_frame, header_frame, body = channel.basic_get(queue='httperfq')
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
        """
        Execute received job
        :param command:
        :type command:
        :return:
        :rtype:
        """
        outputdata = self.getcommandoutput(command)
        try:
            dict = ast.literal_eval(outputdata)
            dict.update({"worker": self.get_host_name()})
            dict.update({"group": self.get_group_name()})
            return str(dict)
        except SyntaxError:
            print "This is not a dict"
            dict = self.convert_outout_to_dict(outputdata)
            dict.update({"worker": self.get_host_name()})
            dict.update({"group": self.get_group_name()})
            dict.update({"check_timestamp": time.time()})
            return str(dict)

    def reply_to_master(self, content):
        """
        Port report to report-queue
        :param content:
        :type content:
        :return:
        :rtype:
        """
        dict = ast.literal_eval(content)
        job = dict.values()[0]
        self.set_group_name(dict.keys()[0])
        message = self.do_job(job)
        credentials = pika.PlainCredentials('USER', 'PASSWORD')
        connection = pika.BlockingConnection(pika.ConnectionParameters('IP', 5672, '/', credentials))
        channel = connection.channel()
        channel.queue_declare(queue="httperfreportq")
        channel.basic_publish(exchange='', routing_key='httperfreportq', body=message)
        connection.close()

    @staticmethod
    def getcommandoutput(self, command):
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
    def convert_outout_to_dict(self, content):
        """
        Convert test result to a dictionary
        :param content:
        :type content:
        :return:
        :rtype:
        """
        lower_content = content.lower()
        buf = StringIO.StringIO(lower_content.strip("\n"))
        templist = []
        list = []
        reportdict = {}
        for i in buf.readlines():
            templist.append(i)
        statusmessage = ""
        if "</html>" in templist:
            statusstring = " ".join(templist[templist.index("<html>\n"):templist.index("</html>") + 1])
            del [templist[templist.index("<html>\n"):templist.index("</html>") + 1]]
            statusmessage = statusstring.replace("\n", "")
        elif "ok\t</html>" in templist:
            statusstring = " ".join(templist[templist.index("<html>\n"):templist.index("ok\t</html>") + 1])
            del [templist[templist.index("<html>\n"):templist.index("ok\t</html>") + 1]]
            statusmessage = statusstring.replace("\n", "")
        for i in templist:
            content = i.replace("\n", "")
            if content != "":
                list.append(content)
        for i in list:
            j = i.split(":")
            if len(j) == 1:
                reportdict.update({"message": j[0]})
            elif len(j) >= 2:
                reportdict.update({j[0]: "".join(j[1:len(j)])})
        reportdict.update({"status": statusmessage})
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


worker = HttperfWorker()
worker.fetch_job_from_queue()
