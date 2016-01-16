#!/usr/bin/env python
import sys
import os
import sqlite3
import random
import gzip

g_alpha = frozenset(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                     'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't' 'u', 'v', 'w', 'x', 'y', 'z'])
g_numeric = frozenset(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])


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
        return self.db.execute("Select ip from rips, doms, doms_rips "
                               "where doms.did = doms_rips.did "
                               "and rips.riid = doms_rips.riid "
                               "and name = ?", (dom,))

    # get Related Historic Domain Names on IP address ip
    def getRHDN(self, ip):
        return self.db.execute("Select name from rips, rdoms, rdoms_rips "
                               "where ip = ?"
                               "and rdoms.rdid = rdoms_rips.rdid "
                               "and rips.riid = rdoms_rips.riid ", (ip,))


def calcUniGramsEx(dom):
    unigrams = {}

    for c in dom:
        unigrams[c] = unigrams.get(c, 0) + 1

    ug = unigrams.items()

    ug.sort(key=lambda x: x[0])

    return ug


def calcCorseFeat(dom):
    cFeat = []

    dlen = len(dom)
    cFeat.append(dlen)

    tmp = dom.split(".")

    dlvls = len(tmp)
    cFeat.append(dlvls)

    if tmp[0] == "www":
        cFeat.append(1)
    else:
        cFeat.append(0)

    lAlpha = 0
    lNum = 0
    lSpec = 0

    for c in tmp[0]:

        if c in g_alpha:
            lAlpha += 1
        elif c in g_numeric:
            lNum += 1
        else:
            lSpec += 1
    cFeat.append(lAlpha)
    cFeat.append(lNum)
    cFeat.append(lSpec)

    mAlpha = 0
    mNum = 0
    mSpec = 0

    for t in tmp[1:-1]:
        if c in g_alpha:
            mAlpha += 1
        elif c in g_numeric:
            mNum += 1
        else:
            mSpec += 1

    cFeat.append(mAlpha)
    cFeat.append(mNum)
    cFeat.append(mSpec)

    rUG = calcUniGramsEx(tmp[-1])

    cFeat.append(rUG)

    return cFeat


def extractCoarseFeat(dom, fpOut):
    cf = calcCorseFeat(dom)

    fpOut.write("{0} {1} {2} {3} {4} {5} {6} {7} {8} {9}".format(dom, cf[0], cf[1],
                                                                 cf[2], cf[
                                                                     3], cf[4],
                                                                 cf[5], cf[6], cf[7], cf[8]))

    for c, v in cf[9]:
        fpOut.write(" {0}${1}".format(c, v))

    fpOut.write("\n")


def fsGetRHDN(ip, rhdn_path):
    fp = gzip.open(os.path.join(rhdn_path, ip + ".gz"))

    rhdn = []

    for line in fp:
        line = line.strip()
        if len(line) == 0:
            continue

        dom = line.split()[0]

        rhdn.append((dom,))

    return rhdn


def main():
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print sys.argv[0], "db domain fdir [rhdn_folder]"
        sys.exit(2)

    rh = RHIPDN(sys.argv[1])

    checkDom = sys.argv[2]

    print "Grabbing RHIPs"
    rhip = rh.getRHIP(checkDom)

    ipList = []

    for ip in rhip:
        ipList.append(ip[0])

    if len(ipList) == 0:
        print "No IPs associated with {0}".format(checkDom)
        sys.exit(-1)

    for ip in ipList:
        print "Grabbing RHDN on {0}:".format(ip)
        if len(sys.argv) == 4:
            rhdn = rh.getRHDN(ip)
        else:
            rhdn = fsGetRHDN(ip, sys.argv[4])

        fpOut = open(os.path.join(
            sys.argv[3], checkDom + "_" + ip + ".txt"), "w")

        dset = set()

        for dom in rhdn:
            dset.add(dom[0])

            extractCoarseFeat(dom[0], fpOut)

        if checkDom not in dset:
            extractCoarseFeat(checkDom, fpOut)

        fpOut.close()

    rh.DBClose()


if __name__ == '__main__':
    sys.exit(main())
