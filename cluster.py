#!/usr/bin/env python
import sys
import os
import sqlite3
import random
import datetime
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction import DictVectorizer
from sklearn import preprocessing
import math


class Dom:

    def __init__(self, db, dom):
        self.db = db
        self.name = dom
        self.fdate = None
        self.ldate = None

        self.ipdates = {}

        self.rips = []
        self.rnets = []

        nets = set()

        self.db.execute("Select ip, fdate, ldate from rdoms "\
                         "where name = ?", (dom,))

        for fields in db.fetchall():
            self.rips.append(fields[0])

            net = ".".join(fields[0].split(".")[:3])

            if net not in nets:
                self.rnets.append(net)
            nets.add(net)

            fdate = datetime.date(int(fields[1][:4]), int(fields[1][4:6]), int(fields[1][6:8]))
            ldate = datetime.date(int(fields[2][:4]), int(fields[2][4:6]), int(fields[2][6:8]))

            self.ipdates[fields[0]] = (fdate, ldate)

            if self.fdate == None:
                self.fdate = fdate
            elif self.fdate > fdate:
                self.fdate = fdate

            if self.ldate == None:
                self.ldate = ldate
            elif self.ldate < ldate:
                self.ldate = ldate

        self.rips.sort()
        self.rnets.sort()


def extractFeatures(db, inspect):
    ips = {}
    nets = {}
    doms = set()

    rdomList = []

    rdomList.append(inspect)

    doms.add(inspect.name)

    for ip in inspect.rips:
        if ip not in ips:
            ips[ip] = set()
        ips[ip].add(inspect)

    for net in inspect.rnets:
        if net not in nets:
            nets[net] = set()
        nets[net].add(inspect)

        db.execute("Select name from rdoms where net = ?", (net,))

        for dom in db.fetchall():
            if dom[0] in doms:
                continue
            doms.add(dom[0])
            
            rdom = Dom(db, dom[0])

            rdomList.append(rdom)

            for rip in rdom.rips:
                if rip not in ips:
                    ips[rip] = set()
                ips[rip].add(rdom)

            for rnet in rdom.rnets:
                if rnet not in nets:
                    nets[rnet] = set()
                nets[rnet].add(rdom)

    return rdomList, ips, nets

def checkMaxMin(maxVal, minVal, newVal):
    if maxVal == None or maxVal < newVal:
        maxVal = newVal

    if minVal == None or minVal > newVal:
        minVal = newVal

    return maxVal, minVal


def normalize(maxVal, minVal, val):
    if maxVal == minVal:
        return 1.0
    
    return round((float(val - minVal) / (maxVal - minVal)), 6)

def createMatrix(domList, ipClust = None):
    M = []

    maxIP = None
    minIP = None

    maxNet = None
    minNet = None

    maxFdate = None
    minFdate = None

    maxLdate = None
    minLdate = None

    maxAge = None
    minAge = None

    maxMinVals = []

    ddate = datetime.date(2010, 1, 1)

    for dom in domList:
        f = {}

        # ip total
        ipTotal = len(dom.rips)
        f['ipTotal'] = ipTotal
        maxIP, minIP = checkMaxMin(maxIP, minIP, ipTotal)

        # net total
        netTotal = len(dom.rnets)
        f['netTotal'] = netTotal
        maxNet, minNet = checkMaxMin(maxNet, minNet, netTotal)

        # first date
        if ipClust != None:
            dates = dom.ipdates[ipClust]
            fdate = (dates[0] - ddate).days
        else:
            fdate = (dom.fdate - ddate).days
        f['fdate'] = fdate
        maxFdate, minFdate = checkMaxMin(maxFdate, minFdate, fdate)
        
        # last date
        if ipClust != None:
            dates = dom.ipdates[ipClust]
            ldate = (dates[1] - ddate).days
        else:
            ldate = (dom.ldate - ddate).days
        f['ldate'] = ldate
        maxLdate, minLdate = checkMaxMin(maxLdate, minLdate, ldate)
        
        # age
        #if ipClust != None:
#            dates = dom.ipdates[ipClust]
#            age = (dates[1] - dates[0]).days
#        else:
#            age = (dom.ldate - dom.fdate).days
#        f['age'] = age
#        maxAge, minAge = checkMaxMin(maxAge, minAge, age)

        # rhips
        for ip in dom.rips:
            f[ip] = 1.0

        # rhnets
        for net in dom.rnets:
            f[net] = 1.0

        M.append(f)

    for f in M:        
        f['ipTotal'] = normalize(maxIP, minIP, f['ipTotal'])
        f['netTotal'] = normalize(maxNet, minNet, f['netTotal'])
        f['fdate'] = normalize(maxFdate, minFdate, f['fdate'])
        f['ldate'] = normalize(maxLdate, minLdate, f['ldate'])
        #f['age'] = normalize(maxAge, minAge, f['age'])
        #if f['ipTotal'] > 1 or f['netTotal'] > 1 or f['fdate']  > 1 or f['ldate'] > 1:
#                print f['ipTotal'], f['netTotal'], f['fdate'], f['ldate']#, f['age'] 

    return M
    


def cluster(M, domList, inspect):
    v = DictVectorizer()

    X = v.fit_transform(M)

    minK = 1
    maxK = min((int((math.sqrt((len(domList) + 1) / 2.0))) * 10, len(domList)))

    k = int((math.sqrt((len(domList) + 1) / 2.0)))

    count = 0

    while True:
        if count >= 1:
            break
        
        km = KMeans(n_clusters=k)

        Y = km.fit_predict(X)

        clust = {}

        cnum = -1

        for i in range(len(domList)):
            if Y[i] not in clust:
                clust[Y[i]] = []

            clust[Y[i]].append(domList[i])
        
            if domList[i].name == inspect.name:
                cnum = Y[i]

        print "Round", count

        if len(clust[cnum]) > 100:
            if k > minK:
                minK = k

            if k >= maxK:
                break
               
            k = k * 2 

            if k > maxK:
                k = maxK
        elif len(clust[cnum]) < 10:
            if k < maxK:
               maxK = k

            if k <= minK:
                break
               
            k = minK + ((maxK - minK)  / 2)
        else:
            break

        count += 1
    print "Done\n"

    return clust[cnum]  



def main():
    if len(sys.argv) != 3:
        print sys.argv[0], "db domain"
        sys.exit(2)

    conn = sqlite3.connect(sys.argv[1])
    db = conn.cursor()

    print "Getting Domain Info"
    inspect = Dom(db, sys.argv[2])

    print "Extracting Features"
    rdomList, ips, nets = extractFeatures(db, inspect)

    print len(ips), len(nets), len(rdomList)

    clusts = []

    for ip in inspect.rips:
        print "Clustering Domains on IP", ip
        print "Creating Feature Vectors"
        domList = list(ips[ip])
        M = createMatrix(domList, ip)

        print "Clustering", ip
        c = cluster(M, domList, inspect)
        clusts.append((c, ip, len(domList)))

    print "Creating Feature Vectors Across All Networks"
    M = createMatrix(rdomList)

    print "Clustering All"
    ac = cluster(M, rdomList, inspect)

    
    for c, ip, tdoms in clusts:
        print "\nIP {0} Cluster ({1} out of {2}):".format(ip, len(c), tdoms)
        for dom in c:
            dates = dom.ipdates[ip]
            print "\t", dom.name, len(dom.rips), len(dom.rnets), dates[0].isoformat(), dates[1].isoformat()#, dom.rips, dom.rnets

    print "\nCombined Cluster ({0} out of {1}):".format(len(ac), len(rdomList))
    for dom in ac:
        print "\t", dom.name, len(dom.rips), len(dom.rnets), dom.fdate.isoformat(), dom.ldate.isoformat()#, dom.rips, dom.rnets
        
    conn.close()

 
           
    

    
    
if __name__ == '__main__':
    sys.exit(main())
    


