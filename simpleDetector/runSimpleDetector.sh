hadoop jar /opt/cloudera/parcels/CDH-4.6.0-1.cdh4.6.0.p0.26/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming.jar \
-file /home/romain/Projets/NECOMA/hadoop_simpleDetector/mapper_byte.py    -mapper /home/romain/Projets/NECOMA/hadoop_simpleDetector/mapper_byte.py \
-file /home/romain/Projets/NECOMA/hadoop_simpleDetector/reducer.py   -reducer /home/romain/Projets/NECOMA/hadoop_simpleDetector/reducer.py \
-input /user/romain/data/200101151400.ipsum -output /user/romain/tmp/test
