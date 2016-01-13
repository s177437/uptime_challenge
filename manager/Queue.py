import pika
from Report import *

'''
Created on 1. sep. 2015

@author: stianstrom
'''
import time


class Queue():
    """
    This module is the Queue class.
    """
    queuename = ""
    # comment
    # time=0
    time = time.time()
    queuecontent = ""

    def setQueueContent(self, value):
        """
        This sets the Queue content to be used later.
        :param value:
        :type value:
        :return:
        :rtype:
        """
        self.queuecontent = value

    def getQueueContent(self):
        """
        Return the queue content
        :return:
        :rtype:
        """
        return self.queuecontent

    def connectToRabbitMQ(self):
        """
        Connect to the rabbitmq server.
        :return:
        :rtype:
        """
        credentials = pika.PlainCredentials(***REMOVED***, ***REMOVED***)
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', credentials))
        return connection

    def createQueue(self, quename, content):
        """
        Create a queue with a given name and fill it with some content
        :param quename:
        :type quename:
        :param content:
        :type content:
        :return:
        :rtype:
        """
        connection = self.connectToRabbitMQ()
        channel = connection.channel()
        channel.queue_declare(queue=quename)
        channel.basic_publish(exchange='', routing_key=quename, body=str(content))
        connection.close()

    def listenContinouslyToQueue(self, quename):
        """
        Listen continously to the queue.
        :param quename:
        :type quename:
        :return:
        :rtype:
        """
        connection = self.connectToRabbitMQ()
        channel = connection.channel()
        channel.queue_declare(queue=quename)
        channel.basic_consume(self.callback, queue=quename, no_ack=True)
        channel.start_consuming()

    def callback(self, channel, method, properties, body):
        """
        Fetch the report from the queue and build a report to be sent to the interpreter. s
        :param channel:
        :type channel:
        :param method:
        :type method:
        :param properties:
        :type properties:
        :param body:
        :type body:
        :return:
        :rtype:
        """
        report = Report()
        report.buildReport(body)

    def setTime(self, t=0):
        """
        Set time for the execution interval
        :param t:
        :type t:
        :return:
        :rtype:
        """
        self.time = t

    def getTime(self):
        """
        Return the execution time interval
        :return:
        :rtype:
        """
        return self.time

    def receiveOneMessageFromQ(self, queuename, interval):
        """
        Recursive listen method that is used to continously listen to the reportqueue within the execution interval
        :param queuename:
        :type queuename:
        :param timevalue:
        :type timevalue:
        :param interval:
        :type interval:
        :return:
        :rtype:
        """
        timestart = time.time()
        while (time.time()-timestart) <=float(interval) :
            stringValue = ""
            connection = self.connectToRabbitMQ()
            channel = connection.channel()
            channel.queue_declare(queue=queuename)
            try:
                method_frame, header_frame, body = channel.basic_get(queue=queuename)
                if method_frame.NAME == 'Basic.GetEmpty':
                    connection.close()
                else:
                    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                    connection.close()
                    report = Report()
                    report.buildReport(body)
            except AttributeError:
                print "Waiting for answer.. time used:", str((time.time()-timestart)), " interval:", interval
                time.sleep(1)
                connection.close()

