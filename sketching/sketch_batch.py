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

# Parameters for hashing
nbHash = config.get("Hashing", "nbHash")
hashSize = config.get("Hashing", "hashSize")

for ye in years:
    for mo in months:
        for da in days:

            traceName = "{0}{1:02d}{2:02d}1400.ipsum".format(ye,mo,da)
            outputDir = "hashedTraffic/"+traceName+"_block4G/" 

            cmdExp = """hadoop jar {streamingLib} \
        -D map.output.key.field.separator=, \
        -D mapred.text.key.partitioner.options=-k1,2 \
        -D mapred.reduce.tasks={nbReducer} \
        -D dfs.blocksize={hadoopBlockSize} \
        -libjars customMultiOutput.jar \
        -outputformat com.custom.CustomMultiOutputFormat \
        -file /home/romain/Projets/NECOMA/hadoop_sketching3/sketch_ipsum_mapper.py  \
        -mapper "/home/romain/Projets/NECOMA/hadoop_sketching3/sketch_ipsum_mapper.py {nbHash} {hashSize}" \
        -file /home/romain/Projets/NECOMA/hadoop_sketching3/sketch_ipsum_reducer.py \
        -reducer /home/romain/Projets/NECOMA/hadoop_sketching3/sketch_ipsum_reducer.py \
        -input /user/romain/data/{traceName} \
        -output /user/romain/{outputPath} \
        -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner"""

            outputPath=outputDir+str(nbHash)+"hash_"+str(hashSize)+"sketch"
            nbReducer = hashSize
            
            #set parameters in the command line
            cmd = cmdExp.format(traceName=traceName, outputPath=outputPath, 
                    nbHash=nbHash, hashSize=hashSize, nbReducer=nbReducer, 
                    hadoopBlockSize=hadoopBlockSize, streamingLib=streamingLib);      

            start = time.time()
            os.system(cmd)
            print time.time() - start
