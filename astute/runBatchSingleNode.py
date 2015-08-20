import time
import os
import sys

#if len(sys.argv)<2:
#  print "usage: "+sys.argv[0]+" traceName"
#  exit()

year = range(2001,2014,3)
month = range(1,4)
day = [15]


astuteThreshold = 3.0
astuteTimeBin = [9]

outputDir = "/home/romain/Projets/NECOMA/experiments/20131129_bigSecSnappy/astuteResultSingleNode/"

cmdExp = """cat {inputFile} | python2 astute.py {threshold} {timeBin} | sort -k1,1 | python2 reducer.py {inputFile} {timeBin} > {outputFile}"""

timeCount = []

for timeBin in astuteTimeBin:
 for ye in year:
   for mo in month:
     for da in day:
       inputFile = "/home/romain/Projets/NECOMA/data/{0}{1:02d}{2:02d}1400.ipsum".format(ye,mo,da)
       outputFile = outputDir+"astute_t{3}_bin{4}_{0}{1:02d}{2:02d}1400.xml".format(ye,mo,da,astuteThreshold,timeBin) 
       if not os.path.exists(outputFile):
         timeCount.append([])
         cmd = cmdExp.format(inputFile=inputFile, outputFile=outputFile, threshold=astuteThreshold, timeBin=timeBin)
		
         start = time.time()         
         os.system(cmd)
         timeCount[-1].append(time.time() - start)
         sys.stderr.write(str(timeCount)+"\n")
         #print cmd

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
