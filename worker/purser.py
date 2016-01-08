import time
import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
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

    def checkIfFileExists(self, filepath, filename):
	ls_check= self.getcommandoutput("ls "+ filepath)	
	if filename in ls_check : 
		return "True"
	else : 
		return "False"

    def readFileAndCheckIfSentanceExistInTheFile(self, filepath, sentance):
        data= urllib.urlopen("http://128.39.121.59/index.php")
        lines=[]
        for line in data :
            lines.append(line)
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
        time_used_to_download = self.downloadUrl(ip)
        file_exists_in_directory_tree = self.checkIfFileExists(filepath, filename)
        sentance_found="Word not found"
        if file_exists_in_directory_tree == "True" :
            sentance_found = self.readFileAndCheckIfSentanceExistInTheFile(filepath, sentance)
        result["Http response code"]=self.getResponseCode(ip)
        result["Time used to download"]=time_used_to_download
        result["File exists"]=file_exists_in_directory_tree
        result["File"] = filename
        result["Sentance"] = sentance
        result["Hostname"]=ip
        result["Check timestamp"]=time.time()
        result["Lookup status"]=sentance_found

        if result["File exists"] == "True" and result["Http response code"] == 200 and "not found" in sentance_found:
            result["Test status"] = "Partial OK"
        elif result["File exists"] == "False" :
            result["Test status"] = "Not Approved"
        else :
            result["Test status"]= "OK"
        return result



    def downloadUrl(self,hostname):
        self.runcommand("mkdir "+"/root/uptime_challenge_master/worker/"+hostname)
        starttime=time.time()
        http=httplib2.Http()
        status, response = http.request("http://"+hostname)
        urllib.urlretrieve("http://"+hostname+"/stylesheet.css", "/root/uptime_challenge_master/worker/"+hostname+"/stylesheet.css")
        urllib.urlretrieve("http://"+hostname+"/index.php", "/root/uptime_challenge_master/worker/"+hostname+"/index.php")
        index=0
        for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('img')) :
            filename="/root/uptime_challenge_master/worker/"+hostname+"/picture"+str(index)
            urllib.urlretrieve(link['src'],filename)
            index+=1
        return time.time() - starttime







#p = Purser()
#print p.runPurser("128.39.121.59", "index.php", "/root/uptime_challenge_master/worker/", "Users:")
#print p.downloadSiteAndReturnTheTime()
#print p.checkIfFileExists("index.php", "128.39.121.59")
#print p.readFileAndCheckIfSentanceExistInTheFile("/Users/stianstrom/PycharmProjects/uptime_challenge_master/testscript/128.39.121.59/index.php", "Users")
#p.runPurser()
#p.deleteDirectory("128.39.121.59")

