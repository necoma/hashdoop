import time
import os
import sys
import ConfigParser
import json

config = ConfigParser.ConfigParser()
config.read("../hashdoop.conf")

# Traces to sketch
years = json.loads(config.get("Traces","years")) 
months = json.loads(config.get("Traces","months")) 
days = json.loads(config.get("Traces","days"))  

# Parameters for the Hadoop cluster
hadoopBlockSize = config.get("Hadoop", "blockSize")
streamingLib = config.get("Hadoop", "streamingLib")
tracesHdfsPath = config.get("Hadoop", "tracesHdfsPath")
sketchesHdfsPath = config.get("Hadoop", "sketchesHdfsPath")

# Parameters for hashing
nbHash = config.get("Hashing", "nbHash")
hashSize = config.get("Hashing", "hashSize")


nbHashFct = [1]
outputSize = [2,4,8,16,32,64,128,256,512,1024];


cmdExp = """hadoop jar {streamingLib} \
 -D mapred.reduce.tasks=1 \
-file mapper_pkt.py    -mapper /home/romain/Projets/NECOMA/hadoop_simpleDetector/mapper_pkt.py \
-file reducer.py -file /home/romain/Projets/NECOMA/hadoop_astute/admd.py   -reducer "/home/romain/Projets/NECOMA/hadoop_astute/reducer.py {outputDir}" \
-input /user/romain/{inputFiles} -output /user/romain/simpleDetector/{outputDir}""".format(streamingLib = streamingLib)

timeCount = []

for ye in years:
   for mo in months:
     for da in days:
       traceName = "{0}{1:02d}{2:02d}1400.ipsum".format(ye,mo,da)
       inputDir = "hashedTraffic/"+traceName+"_block4G/" 

       timeCount.append([])
       for nbHash in nbHashFct:
         for hashSize in outputSize:
           inputFiles = inputDir+str(nbHash)+"hash_"+str(hashSize)+"sketch/hash*"
           outputDir = inputDir+str(nbHash)+"hash_"+str(hashSize)+"sketch_pkt/"
           cmd = cmdExp.format(inputFiles=inputFiles, outputDir=outputDir)
		
           start = time.time()         
           os.system(cmd)
           timeCount[-1].append(time.time() - start)
           sys.stderr.write(str(timeCount)+"\n")
           #print cmd

print "#Hash output"
print outputSize
print "#Year"
print year
print "#Month"
print month
print "#Day"
print day
print "#Detection time for all files:"
print timeCount
