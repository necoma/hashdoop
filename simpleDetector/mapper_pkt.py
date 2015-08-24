#!/usr/bin/env python2

import sys
import numpy as np

nbStd = float(sys.argv[1]); # Detection threshold

pktPerHost = dict()

binEnd=0
binStart = sys.maxint

# input comes from STDIN (standard input)
for line in sys.stdin:

    # ignore header
    if line.startswith("!"):
      continue
    
    
    # get each fields of the tuple 
    fields = line.split()
    ts = float(fields[0])
    ipSrc = fields[1]
    ipDst = fields[3]

    if ts < binStart:
      binStart=ts

    if ts > binEnd:
      binEnd=ts

    if ipSrc in pktPerHost:
      pktPerHost[ipSrc] += 1
    else:
      pktPerHost[ipSrc] = 1
      
    if ipDst in pktPerHost:
      pktPerHost[ipDst] += 1
    else:
      pktPerHost[ipDst] = 1
      
  
# compute the threshold based on the mean and standard deviation
pktCount = np.array(pktPerHost.values())
mean = pktCount.mean()
std = pktCount.std()
threshold = mean + nbStd*std

# report anomalous IP addresses 
for host, val in pktPerHost.iteritems():
  if val > threshold:
     print(host+":* *:*;"+str(binStart)+";"+str(binEnd)+"\t1")   
     print("*:* "+host+":*;"+str(binStart)+";"+str(binEnd)+"\t1")
