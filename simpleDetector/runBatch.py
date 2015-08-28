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

# Parameters for the simple Detector
threshold = config.get("SimpleDetector","threshold")
outputHdfsPath = config.get("SimpleDetector", "outputHdfsPath")

cmdExp = """hadoop jar {streamingLib} \
 -D mapred.reduce.tasks=1 \
-mapper "mapper_pkt.py {threshold}" \
-reducer "reducer.py {outputHdfsPath}{outputDir} {threshold}" \
-input {sketchesHdfsPath}{inputFiles} -output {outputHdfsPath}{outputDir} \
-files ./mapper_pkt.py,./reducer.py,./admd.py
"""

timeCount = []

for ye in years:
    for mo in months:
        for da in days:
            traceName = "{0}{1:02d}{2:02d}1400.ipsum".format(ye,mo,da)
            inputDir = traceName+"/" 

            inputFiles = inputDir+str(nbHash)+"hash_"+str(hashSize)+"sketch/hash*"
            outputDir = inputDir+str(nbHash)+"hash_"+str(hashSize)+"sketch_pkt/"
            cmd = cmdExp.format(inputFiles=inputFiles, outputDir=outputDir,
                    sketchesHdfsPath=sketchesHdfsPath, outputHdfsPath=outputHdfsPath,
                    threshold=threshold,streamingLib = streamingLib)
            
            start = time.time()         
            os.system(cmd)
            timeCount.append(time.time() - start)

print "#Year"
print years
print "#Month"
print months
print "#Day"
print days
print "#Detection time for all files:"
print timeCount
