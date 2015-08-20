 
 
# Generate ipsumdump files
src/ipsumdump -r /mnt/MAWI/2013/10/2013-10-26.gz > ~/Data/2013-10-26


#Upload trace on HDFS with a smaller block size
hadoop fs -D dfs.block.size=33554432 -put ../data/200408281400.ipsum data/