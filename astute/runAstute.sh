hadoop jar /usr/local/hadoop-1.1.2/contrib/streaming/hadoop-streaming-1.1.2.jar \
-file /home/romain/Projects/hadoop_astute/astute.py    -mapper /home/romain/Projects/hadoop_astute/astute.py \
-file /home/romain/Projects/hadoop_astute/reducer.py   -reducer /home/romain/Projects/hadoop_astute/reducer.py \
-input /user/hadoop/romain/2013-10-26_TestPerf/sketch/hash* -output /user/hadoop/romain/2013-11-11_testAstute
