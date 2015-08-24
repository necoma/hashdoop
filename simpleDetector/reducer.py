#!/usr/bin/env python

import sys
import math
import datetime

import admd

__version__ = 0.2

def newAnnotation(threshold, trace):
  root = admd.annotation_t()
  
  algo = admd.algorithm_t()
  algo.set_name("Simple MapReduce Detector (packet based)")
  algo.set_version(__version__)
  algo.set_parameter("tau={0}".format(threshold))
  root.set_algorithm(algo)
  
  analy = admd.analysis_t()
  analy.set_datetime(datetime.datetime.today())
  analy.set_description("MAWILab")
  analy.set_analyst("Romain Fontugne")
  analy.set_organization("National Institute of Informatics")
  root.set_analysis(analy)
  
  data = admd.dataset_t()
  data.set_description("MAWI")
  data.set_name(trace)
  root.set_dataset(data)
  
  return root

def newAnomaly(flow, ts, te, count):
  slice = admd.slice_t()
  filt = admd.filter_t()
  srcDst = flow.split()
  srcIP,srcPort = srcDst[0].split(":")
  dstIP,dstPort = srcDst[1].split(":")
  if srcIP != "*":
    filt.set_src_ip(srcIP)
  if srcPort != "*":
    filt.set_src_port(int(srcPort))
  if dstIP != "*":
    filt.set_dst_ip(dstIP)
  if dstPort != "*":
    filt.set_dst_port(int(dstPort))
  
  slice.add_filter(filt)

  ano = admd.anomaly_t()
  ano.set_description(str(count))
  ano.add_slice(slice)
  ts = ts.split(".")
  tsSec = int(ts[0])
  tsUsec= int(ts[1])
  te = te.split(".")
  teSec = int(te[0])
  teUsec= int(te[1])
  tsS = admd.timestamp_t(sec=tsSec, usec=tsUsec)
  tsE = admd.timestamp_t(sec=teSec, usec=teUsec)
  ano.set_from(tsS)
  ano.set_to(tsE)
  ano.set_type("")

  return ano

if len(sys.argv)<3:
   sys.stderr.write("usage: "+sys.argv[0]+" traceName threshold\n")
   exit()

current_flow = None
current_count = 0
current_ts = 0
current_te = 0
flow = None

root = newAnnotation(sys.argv[2],sys.argv[1])

# input comes from STDIN
for line in sys.stdin:
    # parse the input we got from mapper.py
    anomaly, count = line.split('\t', 1)
    ano = anomaly.split(";")
    flow = ano[0]
    te = float(ano[2])
    # convert count (currently a string) to int
    try:
        count = int(count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: host) before it is passed to the reducer
    if current_flow == flow:
        current_count += count
        if te > current_te:
          current_te = te
    else:
        if current_flow:
          # write result to the admd structure
          root.add_anomaly(newAnomaly(current_flow, ano[1], ano[2], count))
          #  print('{0};{2};{3}\t{1}'.format(current_flow, current_count, current_ts, current_te))

        current_count = count
        current_flow = flow
        current_ts = float(ano[1])
        current_te = te

# do not forget to output the last host if needed!
if current_flow == flow and current_flow!=None:
    #print('{0};{2};{3}\t{1}'.format(current_flow, current_count, current_ts, current_te))
    root.add_anomaly(newAnomaly(current_flow, ano[1], ano[2], count))


root.export(sys.stdout,1,namespace_='', name_='admd:annotation', namespacedef_='xmlns:admd="http://www.nict.go.jp/admd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nict.go.jp/admd admd.xsd"')
