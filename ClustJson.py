#!/usr/bin/env python
import sys
import os
import json


class ClustJson:

    def __init__(self, jsonFile):
        fp = open(jsonFile)

        self.clusts = {}

        self.data = json.load(fp)

        self.ipcounts = {}

        for cdata in self.data['ip_clust']:
            self.ipcounts[cdata['ip']] = (
                int(cdata['total_dom_count']), int(cdata['bl_count']))
            self.clusts[cdata['ip']] = cdata['cluster_doms']

        fp.close()

    @property
    def inspectDomName(self):
        return self.data['dom_name']

    @property
    def inspectDomRHIP(self):
        return self.data['rhip']

    def ipCC(self, ip):
        if ip in self.data['ip_info']:
            return self.data['ip_info'][ip]['cc']
        else:
            return 'ZZ'

    def ipASN(self, ip):
        if ip in self.data['ip_info']:
            return self.data['ip_info'][ip]['asn']
        else:
            return 'NA'

    def ipBGP(self, ip):
        if ip in self.data['ip_info']:
            return self.data['ip_info'][ip]['bgp']
        else:
            return 'NA'

    def ipDomCount(self, ip):
        if ip in self.ipcounts:
            return self.ipcounts[ip][0]
        else:
            return 0

    def ipBLDomCount(self, ip):
        if ip in self.ipcounts:
            return self.ipcounts[ip][1]
        else:
            return 0

    def ipClusterDoms(self, ip):
        if ip in self.clusts:
            return self.clusts[ip]
        else:
            return None

    def allClustDoms(self):
        return self.data['all_clust']['doms']

    def allClustBLCount(self):
        return self.data['all_clust']['bl_count']

    def allClustDomCount(self):
        return self.data['all_clust']['total']


def main():
    if len(sys.argv) != 2:
        print sys.argv[0], "json"
        sys.exit(2)

    cj = ClustJson(sys.argv[1])

    print "\nInvestigating Dom: {0} on the follwing RHIPs:", cj.inspectDomName
    for ip in cj.inspectDomRHIP:
        print "\t{0} (CC: {1} - ASN: {2} - BGP: {3}) -- Total Doms: {4} - BlackList: {5}".format(
            ip, cj.ipCC(ip), cj.ipASN(ip), cj.ipBGP(ip), cj.ipDomCount(ip), cj.ipBLDomCount(ip))

    for ip in cj.inspectDomRHIP:
        print '\nIP {0} Cluster ({1} out of {2} - Blacklist: {3}):'.format(ip, len(cj.ipClusterDoms(ip)), cj.ipDomCount(ip), cj.ipBLDomCount(ip))
        for dom in cj.ipClusterDoms(ip):
            print "\t{0} {1} {2}".format(dom['name'], dom['dist'], "BlackList" if dom['bl'] else "")

    print "\nCombined Cluster ({0} out of {1} - Blacklist: {2}):".format(len(cj.allClustDoms()), cj.allClustDomCount(), cj.allClustBLCount())
    for dom in cj.allClustDoms():
        print "\t{0} {1} {2}".format(dom['name'], dom['dist'], "BlackList" if dom['bl'] else "")

    print ""


if __name__ == '__main__':
    sys.exit(main())
