import time
import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
import subprocess
import urllib
import os

__author__ = 'Stian Stroem Anderssen'


class Purser:
    """
    This class represents the purser-check.
    """

    def return_download_time(self, hostname):
        """
        Download the Bookface site using wget
        :param hostname:
        :type hostname:
        :return:
        :rtype:
        """
        starttime = time.time()
        output = ""
        output = self.get_command_output(
            "wget -t 2 -T 5 -P /root/uptime_challenge_master/worker/ -p -q http://" + hostname + "/index.php")
        if "No route" in output:
            return 0
        else:
            return time.time() - starttime

    def delete_directory(self, directory_name):
        """
        Delete a given directory using bash rm
        :param directory_name:
        :type directory_name:
        :return:
        :rtype:        """
        self.runcommand("rm -rf " + directory_name)

    @staticmethod
    def check_if_file_exists(self, filepath, filename):
        """
        Check if a file exists in a directory.
        :param filepath:
        :type filepath:
        :param filename:
        :type filename:
        :return:
        :rtype:
        """
        ls_check = self.get_command_output("ls " + filepath)
        if filename in ls_check:
            return "True"
        else:
            return "False"

    @staticmethod
    def check_if_word_exists(self, filepath, ip, sentance):
        """
        Check if a word exists on a the frontpage
        :param filepath:
        :type filepath:
        :param ip:
        :type ip:
        :param sentance:
        :type sentance:
        :return:
        :rtype:
        """
        data = urllib.urlopen("http://" + ip + "/index.php")
        lines = []
        for line in data:
            lines.append(line)
        notfound = "Not found"
        print lines
        for line in lines:
            if sentance in line:
                return "Word is found in " + filepath + " at line " + str(lines.index(line))
        return "Word not found in " + filepath

    @staticmethod
    def get_command_output(self, command):
        """
        Get command output from a bash command
        :param command:
        :type command:
        :return:
        :rtype:
        """
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, error) = p.communicate()
        return output

    @staticmethod
    def get_response_code(self, sitename):
        try:
            return urllib.urlopen("http://" + sitename).getcode()
        except IOError:
            return 500

    @staticmethod
    def run_command(self, command):
        """
        Execute a command without saving the output
        :param command:
        :type command:
        :return:
        :rtype:
        """
        subprocess.call(command, shell=True)

    def run_purser(self, ip, filename, filepath, sentance):
        """
        Execute the purser-check  and set test-status
        :param ip:
        :type ip:
        :param filename:
        :type filename:
        :param filepath:
        :type filepath:
        :param sentance:
        :type sentance:
        :return:
        :rtype:
        """
        result = {}
        file_found = "File not found"
        time_used_to_download = self.return_download_time(ip)
        if time_used_to_download == 0:
            result["File exists"] == "False"
            result["Check timestamp"] = time.time()
            result["Lookup status"] = "Cannot find word, since the network is down"
            result["Hostname"] = ip
            result["File"] = filename
            result["Http response code"] = 500
            return result
        else:
            file_exists_in_directory_tree = self.check_if_file_exists(filepath, filename)
            sentance_found = "Word not found"
            if file_exists_in_directory_tree == "True":
                sentance_found = self.check_if_word_exists(filepath, ip, sentance)
            result["Http response code"] = self.get_response_code(ip)
            result["Time used to download"] = time_used_to_download
            result["File exists"] = file_exists_in_directory_tree
            result["File"] = filename
            result["Hostname"] = ip
            result["Check timestamp"] = time.time()
            result["Lookup status"] = sentance_found

            if result["File exists"] == "True" and "not found" in sentance_found:
                result["Test status"] = "Partial OK"
            elif result["File exists"] == "False":
                result["Test status"] = "Not Approved"
            else:
                result["Test status"] = "OK"
            return result

    def download_url(self, hostname):
        """
        Download a given url by using inbuilt python-tools
        :param hostname:
        :type hostname:
        :return:
        :rtype:
        """
        self.runcommand("mkdir " + "/root/uptime_challenge_master/worker/" + hostname)
        starttime = time.time()
        http = httplib2.Http()
        status, response = http.request("http://" + hostname)
        urllib.urlretrieve("http://" + hostname + "/stylesheet.css",
                           "/root/uptime_challenge_master/worker/" + hostname + "/stylesheet.css")
        urllib.urlretrieve("http://" + hostname + "/index.php",
                           "/root/uptime_challenge_master/worker/" + hostname + "/index.php")
        index = 0
        for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('img')):
            filename = "/root/uptime_challenge_master/worker/" + hostname + "/picture" + str(index)
            urllib.urlretrieve(link['src'], filename)
            index += 1
        return time.time() - starttime
