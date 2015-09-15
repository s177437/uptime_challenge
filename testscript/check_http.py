import urllib
import time
import sys
class check_http() :
    def checkstatus(self, sitename):
        return urllib.urlopen("http://"+sitename).getcode()

    def giveAward(self,time):
        coins= 0
        if(float(time)>0.5) :
            #print "The time has passed ", time , "seconds"
            coins=1000
        elif (float(time)>=0.25 and float(time)<=0.5 ) :
            #print "The time has passed", time , "seconds"
            coins= 2000
        elif (float(time)<0.24) :
            #print "The time has passed", time, "seconds"
            coins = 4000
        else :
            #print "The time has passed", time, "seconds"
            coins = 50
        return coins


starttime= time.time()
httpclass= check_http()
site = sys.argv[1]
#time= sys.argv[2]
code = httpclass.checkstatus(site)
systime=(time.time()-starttime)
response_time=format(round(systime,2))
resultdict={}
resultdict.update({"Site": site, "Response time": response_time,"Response Code": code,"Award": httpclass.giveAward(response_time)})
print resultdict



