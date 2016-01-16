#DRAVis
###Visualizing Domain Reputation & Attribution
#####Terry Nelms, Kulsoom Abdullah, & Joshua Kimball
======
![Alt text](https://github.com/kulsoom-abdullah/Draviz/blob/master/screenshots/Draviz.jpg "Optional Title")
I audited Data and Visual Analytics, a Computer Science course at Georgia Tech.  This repository includes 
* Python and D3 code from the group project that Spring 2014.
* Screenshots of the D3 visualization
* **dravis_final.pdf** - PDF of the slides from the project presentation which includes screenshots of the d3 visualization.

The D3 demo can be run by downloading *draviz.html*, and the d3 folder (which contains *d3.min.js* and *colorbrewer.v1.min.js*), then clicking on draviz2.html or opening it with your web browzer.  

####Summary:
Malware operators continue their activity and passing on instructions to their bots (machines they have control over) by using agility in domains, which helps to avoid takedown and being blacklisted.
To find their new malicious domain names, we leverage DNS agility for reputation & attribution.  Domains can be clustered domains on their common network relationships.  Network IPs are expensive and generally not changed as frequently as domain names can be.

Data Sources:
Passive DNS Database:

" 22 Billion per day.
" 8 Trillion per year.
DNS Records From
"  ISPs
Telcos 
Enterprises

￼pDNSDB - Related Historic IP Addresses
IP addresses that a domain has ever resolved to
￼pDNSDB - Related Historic Domain Names
Domain names that have ever resolved to an IP address

Cluster method
•  Features.
–  Total IPs & networks.
–  IP address, BGP prefix, ASN, country code.
•  Algorithm. –  K-means.
–  sparse matrix.
•  Domain annotation.
–  Identify cluster with domain of interest.
–  Label blacklist domains.
–  Euclidean distance from domains in cluster.

Initial evaluation led analyst to correctly classify approximately 80% of the “unlabeled” domains
•  Generally,clustering and visualization is a good approach for this problem:
–  Only mechanism to communicate & analyze inordinately large, complex structures, i.e. IP networks
•  More levels of indirection exponen2ally increases the number of nodes in the graph
–  Helps to improve accuracy, reliability of blacklists. [Blacklists are created for different purposes; seeing blacklisted firms in or near one cluster is helpful.]
–  Reveal new, potentially interesting features: hyphenated names, # of total blacklist / # of domains in combined cluster
