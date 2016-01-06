import time
import subprocess
import urllib
import os


class Purser:
    def downloadSiteAndReturnTheTime(self, hostname):
        starttime = time.time()
        self.runcommand("wget -t 2 -T 5 -p -q http://"+hostname+"/index.php")
        return time.time() - starttime

    def deleteDirectory(self, directory_name):
        # self.runcommand("rm -rf 128.39.121.59")
        self.runcommand("rm -rf " + directory_name)

    def checkIfFileExists(self, filename, directory_name):
        full_directory_path = os.path.dirname(os.path.abspath(__file__)) + "/" + directory_name + "/"
        return os.path.exists(full_directory_path + filename)

    def getFilePath(self, filename, directory_name):
        full_directory_path = os.path.dirname(os.path.abspath(__file__)) + "/" + directory_name + "/"
        return full_directory_path + filename

    def readFileAndCheckIfSentanceExistInTheFile(self, filepath, sentance):
        lines = [line.rstrip('\n') for line in open(filepath)]
        notfound="Not found"
        for line in lines :
            if sentance in line :
                return sentance+" is found in " + filepath + " at line " + str(lines.index(line))
        return sentance + " not found in " + filepath


    def getcommandoutput(self, command):
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, error) = p.communicate()
        return output

    def getResponseCode(self, sitename):
        return urllib.urlopen("http://" + sitename).getcode()

    def runcommand(self, command):
        subprocess.call(command, shell=True)

    def runPurser(self, ip, filename, filepath, sentance):
        result={}
        file_found="File not found"
        time_used_to_download = self.downloadSiteAndReturnTheTime(ip)
        file_exists_in_directory_tree = self.checkIfFileExists(filename, ip)
        sentance_found="Word not found"
        if file_exists_in_directory_tree :
            sentance_found = self.readFileAndCheckIfSentanceExistInTheFile(filepath, sentance)
        result["Http response code"]=self.getResponseCode(ip)
        result["Time used to download"]=time_used_to_download
        result["File exists"]=file_exists_in_directory_tree
        result["File"] = filename
        result["Sentance"] = sentance
        result["Hostname"]=ip
        result["Check timestamp"]=time.time()
        result["Lookup status"]=sentance_found

        if result["File exists"] and result["Http response code"] == 200 and "not found" in sentance_found:
            result["Test status"] = "Partial OK"
        elif result["File exists"] == False :
            result["Test status"] = "Not Approved"
        else :
            result["Test status"]= "OK"
        return result






p = Purser()
#print p.downloadSiteAndReturnTheTime()
#print p.checkIfFileExists("index.php", "128.39.121.59")
#print p.readFileAndCheckIfSentanceExistInTheFile("/Users/stianstrom/PycharmProjects/uptime_challenge_master/testscript/128.39.121.59/index.php", "Users")
#p.runPurser()
#p.deleteDirectory("128.39.121.59")

