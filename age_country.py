#!/usr/bin/env python
import sys
import os
import sqlite3
import random
from datetime import datetime
import urllib2

def days_between(d1, d2):
    #d1 = datetime.strptime(d1, "%Y%m%d") going to be a datetime obj not string
    d2 = datetime.strptime(d2, "%Y%m%d")
    return abs((d2 - d1).days)

def oldest_date(dates):
    datetime_list=[]
    
    for day in dates:
        datetime_list.append(datetime.strptime(day, "%Y%m%d"))
            
    if len(datetime_list)==1:
        return datetime_list[0]
    #sorted (dates, key=lambda x: abs (x-one_date))[0]
    print min(datetime_list)
    return min(datetime_list)

class RHIPDN:

    def __init__(self, dbfile):
        self.conn = sqlite3.connect(dbfile)
        self.db = self.conn.cursor()


    def DBClose(self):
        self.conn.close()
        
    # get ALL domains that we want to examine
    def getDoms(self):
        return self.db.execute("Select name from doms")

    # get Related Historic IP Address form domain dom
    def getRHIP(self, dom):
        return self.db.execute("Select ip from rips, doms, doms_rips "\
                                "where doms.did = doms_rips.did "\
                                "and rips.riid = doms_rips.riid "\
                                "and name = ?", (dom,))
    def getRHIP_AGE(self, dom):
        return self.db.execute("Select ip, fdate, ldate from rips, doms, doms_rips "\
                           "where doms.did = doms_rips.did "\
                           "and rips.riid = doms_rips.riid "\
                           "and name = ?", (dom,))
    

    # get Related Historic Domain Names on IP address ip
    def getRHDN(self, ip):
        return self.db.execute("Select name, days from rips, rdoms, rdoms_rips "\
                                "where ip = ?"\
                                "and rdoms.rdid = rdoms_rips.rdid "\
                                "and rips.riid = rdoms_rips.riid ", (ip,))



def main():
    if len(sys.argv) != 2:
        print sys.argv[0], "db"
        sys.exit(2)

    rh = RHIPDN(sys.argv[1])

    domList = []

    for dom in rh.getDoms():
        domList.append(dom[0])

    lastDate = "20140315"

    while True:
        #print "len domlist", len(domList) 437 answer
        # randomly select a domain to inspect
        random.shuffle(domList)

        dom = domList[0]
        #rhip = rh.getRHIP(dom)
        #rhip, fdate, ldate = rh.getRHIP_AGE(dom)
        rhip = rh.getRHIP_AGE(dom)

        ipList = []
        fdateList = []
        ldateList = []
        daysList = []

        for ip in rhip:
            ipList.append(ip[0])
            fdateList.append(ip[1])
            ldateList.append(ip[2])
        #print "fdate", ip[1]#, "ldate", ip[2]
            #print days_between(ip[1], ip[2]) #correct lifetime of domain

        oldestDate = oldest_date(fdateList)
        age = days_between(oldestDate, lastDate)
        print "oldest Date", oldestDate
        for p in fdateList: print "fDateList", p


        #for date in fdate:
        #    fdateList.append(fdate[0])
    
        #make a request to the server, and place response in a variable
        url="http://www.geoplugin.net/php.gp?ip="+format(ipList[0])
        response = urllib2.urlopen(url)

        #read the data from the response into a string
        html_string = response.read()
        index=html_string.find("countryCode");#\";s;2:\"")
        #print html_string
        index=index+18
        #print index
        print "Country Code", html_string[index:index+2]
    
    #do something with html_string
    
        if len(ipList):
            print ""
            print "Inspecting Domain: {0}".format(dom)
            print ""
            print "RHIP Total {0}:".format(len(ipList))
            for ip in ipList:
                print "\t", ip
            #for days in daysList:
            #    print "\t", "days", days
            break
    print ""
    print "age of domain", age
    
    for ip in ipList:
        rhdnList = []
        rhdnDaysList = []
        rhdn = rh.getRHDN(ip)
        print "RHDN on {0}:".format(ip)
        
        for dom in rhdn:
            rhdnList.append(dom[0])
            rhdnDaysList.append(dom[1])
            # limit the number of domains
            # since this is an example
            if len(rhdnList) > 100000:
                break

        # randomly select related domains to show
        #random.shuffle(rhdnList)
        if len(rhdnList) > 10:
            rhdnList = rhdnList[:10]
            rhdnDaysList = rhdnDaysList[:10]
        for dom in rhdnList:
            print "\t", dom


        print ""

    rh.DBClose()
           
    
if __name__ == '__main__':
    sys.exit(main())
    
        
