import os
import time
import sys

#if len(sys.argv)<2:
#  print "usage: "+sys.argv[0]+" traceName"
#  exit()


year = range(2001,2014,3)
month = range(1,4)
day = [15]

timeCount = []

for ye in year:
  for mo in month:
    for da in day:

      traceName = "{0}{1:02d}{2:02d}1400.ipsum".format(ye,mo,da)
      outputDir = "hashedTraffic/"+traceName+"_block4G/" 
      
      nbHashFct = [1]
      outputSize = [2,4,8,16,32,64,128,256,512,1024];
      
      #hadoopBlockSize = 134217728 # 128MB
      hadoopBlockSize = 4294967296 # 4GB block size! means that there will be no splitted sketch(? to verify)


      cmdExp = """hadoop jar /opt/cloudera/parcels/CDH/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.4.0.jar \
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

      timeCount.append([])

      for nbHash in nbHashFct:
        for hashSize in outputSize:
            outputPath=outputDir+str(nbHash)+"hash_"+str(hashSize)+"sketch"
            nbReducer = hashSize
            
            #set parameters in the command line
            cmd = cmdExp.format(traceName=traceName, outputPath=outputPath, nbHash=nbHash, hashSize=hashSize, nbReducer=nbReducer, hadoopBlockSize=hadoopBlockSize);      

            start = time.time()
            os.system(cmd)
            timeCount[-1].append(time.time() - start)
            print timeCount
            #subprocess.call()
            #print cmd

print "#Elapsed time for all files:"
print timeCount
