import StringIO
content = '''
httperf --client=0/1 --server=10.1.0.39 --port=80 --uri=/ --rate=10 --send-buffer=4096 --recv-buffer=16384 --num-conns=100 --num-calls=1
httperf: warning: open file limit > FD_SETSIZE; limiting max. # of open files to FD_SETSIZE
Maximum connect burst length: 1

Total: connections 100 requests 100 replies 100 test-duration 9.902 s

Connection rate: 10.1 conn/s (99.0 ms/conn, <=1 concurrent connections)
Connection time [ms]: min 0.8 avg 1.0 max 1.2 median 0.5 stddev 0.1
Connection time [ms]: connect 0.4
Connection length [replies/conn]: 1.000

Request rate: 10.1 req/s (99.0 ms/req)
Request size [B]: 62.0

Reply rate [replies/s]: min 10.0 avg 10.0 max 10.0 stddev 0.0 (1 samples)
Reply time [ms]: response 0.5 transfer 0.0
Reply size [B]: header 254.0 content 11510.0 footer 0.0 (total 11764.0)
Reply status: 1xx=0 2xx=100 3xx=0 4xx=0 5xx=0

CPU time [s]: user 2.43 system 7.47 (user 24.5% system 75.5% total 100.0%)
Net I/O: 116.6 KB/s (1.0*10^6 bps)

Errors: total 0 client-timo 0 socket-timo 0 connrefused 0 connreset 0
Errors: fd-unavail 0 addrunavail 0 ftab-full 0 other 0
'''
def convertToDict(content):
    buf = StringIO.StringIO(content.strip("\n"))
    templist=[]
    list=[]
    reportdict={}
    for i in buf.readlines() :
        if " " in i[0] :
            nolines=""
        else :
            templist.append(i)
    for i in templist :
        content=i.replace("\n","")
        if content!="" :
            list.append(content)
    for i in list :
        j = i.split(":")
        if len(j)==1 :
            reportdict.update({"message": j[0]})
        elif (len(j)==2) :
            reportdict.update({j[0]:j[1]})
    print reportdict
    for key,value in reportdict.iteritems() :
        print key, value

convertToDict(content)

