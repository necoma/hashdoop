#!/usr/bin/env python2

import sys

# Output sketches in different files
for line in sys.stdin:
    word = line.partition("\t")
    key = word[0]
    pkt = word[2]
    
    key = key.split(",")
    
    filename = "hash"+key[0]+"_sketch"+key[1]
    sys.stdout.write(filename+"\t"+key[2]+" "+pkt)
