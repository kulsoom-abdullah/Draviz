#!/usr/bin/env python
import sys
import os
import math
import numpy as np
from sklearn.cluster import KMeans
import random


def cluster(allFeatList, domFeatList, checkDom):
    features = []
    domains = []

    for dom, feat, ugfeat in domFeatList:
        fv = []
        j = 0

        for f in feat:
            fv.append(f)

        for i in range(len(allFeatList)):
            if j < len(ugfeat):
                c, v = ugfeat[j]

                if c == allFeatList[i]:
                    fv.append(v)
                    j += 1
                else:
                    fv.append(0)
            else:
                fv.append(0)

        domains.append(dom)
        features.append(fv)

    X = np.array(features)

    k = int(math.sqrt((len(domains) + 1) / 2.0))

    print "Creating {0} clusters".format(k)

    km = KMeans(n_clusters=k)

    Y = km.fit_predict(X)

    cnum = -1

    clust = {}

    for i in range(len(domains)):
        if Y[i] not in clust:
            clust[Y[i]] = []

        clust[Y[i]].append(domains[i])

        if domains[i] == checkDom:
            cnum = Y[i]

    print "Inspect cluster contains {0} domains".format(len(clust[cnum]))

    if len(clust[cnum]) > 1:
        for dom in clust[cnum]:
            print "\t", dom
    else:
        clist = clust.items()

        random.shuffle(clist)

        cCount = 0

        for num, dlist in clist:
            if cCount > 10:
                break
            cCount += 1

            print "\nCluster {0} - Total {1}".format(num, len(dlist))

            random.shuffle(dlist)

            dCount = 0

            for dom in dlist:
                if dCount > 10:
                    break
                dCount += 1
                print "\t{0}".format(dom)


def getFeatures(fname):
    fp = open(fname)

    ugfset = set()

    domFeatList = []

    for line in fp:
        line = line.strip()

        if len(line) == 0:
            continue

        fields = line.split()

        dom = fields[0]

        feat = []

        for f in fields[1:10]:
            feat.append(f)

        ugfeat = []

        for f in fields[10:]:
            c, v = f.rsplit("$", 1)
            v = int(v)

            ugfset.add(c)

            ugfeat.append((c, v))

        domFeatList.append((dom, feat, ugfeat))

    fp.close()

    allFeatList = list(ugfset)
    allFeatList.sort()

    return allFeatList, domFeatList


def getFiles(fdir, dom):
    fFiles = []

    for f in os.listdir(fdir):
        if f.startswith(dom + "_"):
            fFiles.append(os.path.join(fdir, f))

    return fFiles


def main():
    if len(sys.argv) != 3:
        print sys.argv[0], "domain fdir"
        sys.exit(2)

    fFiles = getFiles(sys.argv[2], sys.argv[1])

    for f in fFiles:
        allFeatList, domFeatList = getFeatures(f)
        cluster(allFeatList, domFeatList, sys.argv[1])


if __name__ == '__main__':
    sys.exit(main())
