import os
import time
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

# Go through all traces
for ye in years:
    for mo in months:
        for da in days:

            traceName = "{0}{1:02d}{2:02d}1400.ipsum".format(ye,mo,da)
            outputDir = traceName+"/" 

            cmdExp = """hadoop jar {streamingLib} \
        -D map.output.key.field.separator=, \
        -D mapred.text.key.partitioner.options=-k1,2 \
        -D mapred.reduce.tasks={nbReducer} \
        -D dfs.blocksize={hadoopBlockSize} \
        -libjars customMultiOutput.jar \
        -outputformat com.custom.CustomMultiOutputFormat \
        -file ./sketch_ipsum_mapper.py  \
        -mapper "./sketch_ipsum_mapper.py {nbHash} {hashSize}" \
        -file ./sketch_ipsum_reducer.py \
        -reducer ./sketch_ipsum_reducer.py \
        -input {tracesHdfsPath}{traceName} \
        -output {sketchesHdfsPath}{outputPath} \
        -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner"""

            outputPath=outputDir+str(nbHash)+"hash_"+str(hashSize)+"sketch"
            nbReducer = hashSize
            
            #set parameters in the command line
            cmd = cmdExp.format(traceName=traceName, outputPath=outputPath, 
                    nbHash=nbHash, hashSize=hashSize, nbReducer=nbReducer, 
                    hadoopBlockSize=hadoopBlockSize, streamingLib=streamingLib,
                    sketchesHdfsPath=sketchesHdfsPath, tracesHdfsPath=tracesHdfsPath);      

            start = time.time()
            os.system(cmd)
            print "Hashed %s in %s sec." % (traceName, time.time() - start)
