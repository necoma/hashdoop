#!/usr/bin/env python2

# This mapper reads an ipsumdump trace and reports IP addresses that send or 
# receive significantly more bytes than the others (mean value + 3 std deviation).

# Notice: We assume the trace is obtained with the option -tsSdDlpF (see ipsumdump documentation)
#         and is in text format.

import sys
import numpy as np

nbStd = 3; # report hosts that have 3 std more bytes

bytePerHost = dict()  # Counter for the number of bytes

# input comes from STDIN (standard input)
for line in sys.stdin:

    # ignore header
    if line.startswith("!"):
      continue
    
    # get each fields of the tuple 
    fields = line.split()
    
    ipSrc = fields[1]
    ipDst = fields[3]
    nbBytes = int(fields[5])

    if ipSrc in bytePerHost:
      bytePerHost[ipSrc] += nbBytes
    else:
      bytePerHost[ipSrc] = nbBytes
      
    if ipDst in bytePerHost:
      bytePerHost[ipDst] += nbBytes
    else:
      bytePerHost[ipDst] = nbBytes
      
  
# compute the threshold based on the mean and standard deviation
byteCount = np.array(bytePerHost.values())
mean = byteCount.mean()
std = byteCount.std()
threshold = mean + nbStd*std


for host, val in bytePerHost.iteritems():
  # Report IP addresses with values higher than the threshold
  if val > threshold:
    print('{0}\t{1}'.format(host,1))