hadoop jar /usr/local/hadoop-1.1.2/contrib/streaming/hadoop-streaming-1.1.2.jar \
 -D map.output.key.field.separator=, \
 -D mapred.text.key.partitioner.options=-k1,2 \
 -D mapred.reduce.tasks=16 \
 -D fs.local.block.size=134217728 \
 -libjars custom.jar \
 -outputformat com.custom.CustomMultiOutputFormat \
 -file /home/romain/Projects/hadoop_sketching3/sketch_ipsum_mapper.py  \
 -mapper "/home/romain/Projects/hadoop_sketching3/sketch_ipsum_mapper.py 1 128" \
 -file /home/romain/Projects/hadoop_sketching3/sketch_ipsum_reducer.py \
 -reducer /home/romain/Projects/hadoop_sketching3/sketch_ipsum_reducer.py \
 -input /user/hadoop/romain/Data/200408281400.ipsum \
 -output /user/hadoop/romain/20040828_block128MB/1hash_128sketch \
 -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner


