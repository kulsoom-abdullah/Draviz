#DRAVis
###Visualizing Domain Reputation & Attribution
#####Terry Nelms, Kulsoom Abdullah, & Joshua Kimball
======
![Alt text](https://github.com/kulsoom-abdullah/Draviz/blob/master/screenshots/Draviz.jpg "Optional Title")
This repository includes:
* [dravis_final.pdf] (https://github.com/kulsoom-abdullah/Draviz/blob/master/dravis_final.pdf) - PDF of the slides from the project presentation which includes screenshots of the d3 visualization
* Python and D3 code from the group project that Spring 2014 (I audited Data and Visual Analytics, a Computer Science course at Georgia Tech)
* Screenshots of the D3 visualization

 <!---The D3 demo can be run by downloading *draviz.html*, and the d3 folder (which contains *d3.min.js* and *colorbrewer.v1.min.js*), then clicking on draviz2.html or opening it with your web browser.   --->

####Summary:
Malware operators continue their activity and passing on instructions to their bots (machines they have control over) by using agility in domains, which helps to avoid takedown and being blacklisted.
To find their new malicious domain names, we leverage DNS agility for reputation & attribution.  Domains can be clustered domains on their common network relationships.  Network IPs are expensive and generally not changed as frequently as domain names can be.

#####Data Sources:
1. Passive DNS Database of DNS Records:
 * 22 Billion per day.
 * 8 Trillion per year.
 * From:
   * ISPs 
    * Telcos 
    * Enterprises
2. ￼pDNSDB - Related Historic IP Addresses
  * IP addresses that a domain has ever resolved to
3. ￼pDNSDB - Related Historic Domain Names
  * Domain names that have ever resolved to an IP address

##### Cluster method
* Features.
 * Total IPs & networks.
 * IP address, BGP prefix, ASN, country code.
* Algorithm. –  K-means.
 * sparse matrix.
* Domain annotation.
 * Identify cluster with domain of interest.
 * Label blacklist domains.
 * Euclidean distance from domains in cluster.
 
##### Results
* Initial evaluation led analyst to correctly classify approximately 80% of the “unlabeled” domains
* Generally,clustering and visualization is a good approach for this problem:
   * Only mechanism to communicate & analyze inordinately large, complex structures, i.e. IP networks
     * More levels of indirection exponentially increases the number of nodes in the graph
   * Helps to improve accuracy, reliability of blacklists. [Blacklists are created for different purposes; seeing blacklisted firms in or near one cluster is helpful.]
   * Reveal new, potentially interesting features: hyphenated names, # of total blacklist / # of domains in combined cluster

##### Future Work
* More evaluation!
   * Needs to encompass larger evaluation data set
* Build infrastructure to handle 2 additional levels of indirection for a given domain of interest
   * This adds MM of nodes to the graph
* More features based on network structure needed like different measures of centrality
   * Agility of attacks lends itself to examining network-based features
