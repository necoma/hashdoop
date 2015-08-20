import time
import os
import sys

#if len(sys.argv)<2:
#  print "usage: "+sys.argv[0]+" traceName"
#  exit()

year = range(2001,2014,3)
month = range(1,4)
day = [15]


outputDir = "/home/romain/Projets/NECOMA/experiments/20131129_bigSecSnappy/simpleDetectorPktResultSingleNode/"

cmdExp = """cat {inputFile} | python2 mapper_pkt.py | sort -k1,1 | python2 reducer.py {inputFile} > {outputFile}"""

timeCount = []

for ye in year:
   for mo in month:
     for da in day:
       inputFile = "/home/romain/Projets/NECOMA/data/{0}{1:02d}{2:02d}1400.ipsum".format(ye,mo,da)
       outputFile = outputDir+"simpleDetectorPkt_{0}{1:02d}{2:02d}1400.xml".format(ye,mo,da) 
       if not os.path.exists(outputFile):
         timeCount.append([])
         cmd = cmdExp.format(inputFile=inputFile, outputFile=outputFile)
		
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
print "#Detection time for all files:"
print timeCount
