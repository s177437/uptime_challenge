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
                credentials = pika.PlainCredentials('guest', 'guest')
                connection = pika.BlockingConnection(pika.ConnectionParameters('10.1.1.175', 5672, '/', credentials))
                channel = connection.channel()
                channel.queue_declare(queue='testq')
                try:
                    method_frame, header_frame, body = channel.basic_get(queue='testq')
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
        #print message
        credentials = pika.PlainCredentials('guest', 'guest')
        connection = pika.BlockingConnection(pika.ConnectionParameters('10.1.1.175', 5672, '/', credentials))
        channel = connection.channel()
        channel.queue_declare(queue="reportq")
        channel.basic_publish(exchange='', routing_key='reportq', body=message)
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
	lower_content= content.lower()
        buf = StringIO.StringIO(lower_content.strip("\n"))
	#print lower_content
        #buf = StringIO.StringIO(content)
        templist = []
        list = []
        reportdict = {}
        for i in buf.readlines():
            templist.append(i)
	statusmessage = ""
	if "</html>" in templist: 
                statusstring = " ".join(templist[templist.index("<html>\n"):templist.index("</html>")+1])
                del[templist[templist.index("<html>\n"):templist.index("</html>")+1]]
                statusmessage= statusstring.replace("\n","")
	elif "ok\t</html>" in templist : 
		statusstring = " ".join(templist[templist.index("<html>\n"):templist.index("ok\t</html>")+1])
		del[templist[templist.index("<html>\n"):templist.index("ok\t</html>")+1]]
		statusmessage= statusstring.replace("\n","")
        for i in templist:
            content = i.replace("\n", "")
            if content != "":
                list.append(content)
        for i in list:
            j = i.split(":")
            if len(j) == 1:
                reportdict.update({"message": j[0]})
            elif (len(j) >= 2):
                reportdict.update({j[0]: "".join(j[1:len(j)])})
        reportdict.update({"status": statusmessage})
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
