import time
import os
import sys

#if len(sys.argv)<2:
#  print "usage: "+sys.argv[0]+" traceName"
#  exit()

year = range(2001,2014,3)
month = range(1,4)
day = [15]


nbHashFct = [1]
outputSize = [2,4,8,16,32,64,128,256,512,1024];

astuteThreshold = 3.0
astuteTimeBin = [9]

cmdExp = """hadoop jar /opt/cloudera/parcels/CDH/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.4.0.jar \
 -D mapred.reduce.tasks=1 \
-file /home/romain/Projets/NECOMA/hadoop_astute/astute.py    -mapper "/home/romain/Projets/NECOMA/hadoop_astute/astute.py {threshold} {timeBin}" \
-file /home/romain/Projets/NECOMA/hadoop_astute/reducer.py -file /home/romain/Projets/NECOMA/hadoop_astute/admd.py   -reducer "/home/romain/Projets/NECOMA/hadoop_astute/reducer.py {outputDir} {timeBin}" \
-input /user/romain/{inputFiles} -output /user/romain/astute/{outputDir}"""

timeCount = []

for timeBin in astuteTimeBin:
 for ye in year:
   for mo in month:
     for da in day:
       traceName = "{0}{1:02d}{2:02d}1400.ipsum".format(ye,mo,da)
       inputDir = "hashedTraffic/"+traceName+"_block4G/" 

       timeCount.append([])
       for nbHash in nbHashFct:
         for hashSize in outputSize:
           inputFiles = inputDir+str(nbHash)+"hash_"+str(hashSize)+"sketch/hash*"
           outputDir = inputDir+str(nbHash)+"hash_"+str(hashSize)+"sketch_t"+str(astuteThreshold)+"_bin"+str(timeBin)+"/"
           cmd = cmdExp.format(inputFiles=inputFiles, outputDir=outputDir,threshold=astuteThreshold, timeBin=timeBin)
		
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
print "#timeBin"
print astuteTimeBin
print "#Detection time for all files:"
print timeCount
