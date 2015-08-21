
prerequisites:
- Hadoop cluster with Hadoop Streaming installed
- ipsumdump

# Data formatting
 
## Generate text files from a pcap trace
```
ipsumdump -tsSdDlpF -r ./200704121400.dump.gz > ./200704121400.ipsum
```

## Upload trace on HDFS
The destination directory should be the same as the tracesHdfsPath variable in 
hashdoop.conf.
 
```
hadoop fs -put ./200704121400.ipsum /user/romain/data/
```

# Running Hashdoop

## Traffic hashing

## Anomaly detection 
