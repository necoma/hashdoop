# Hashdoop: A MapReduce framework for network anomaly detection
### Prerequisites:
- Hadoop cluster with Hadoop Streaming installed
- Numpy installed on all hadoop nodes
- [Ipsumdump](http://www.read.seas.harvard.edu/~kohler/ipsumdump/)

Note: to avoid the burden of installing Hadoop, you can also try hashdoop with
the [Matatabi docker image](https://hub.docker.com/r/necoma/matatabi/).

### Basic execution:
The analysis of traffic traces with Hashdoop consists of four main steps:
1.  Convert traffic trace to textual format
2.  Configure Hashdoop
3.  Hash the trace
4.  Detect anomalies

## Data formatting
 
### Generate text files from a pcap trace
Assuming the pcap trace [200704121400.dump.gz](http://mawi.nezu.wide.ad.jp/mawi/samplepoint-F/2007/200704121400.dump.gz)
is in the ~/mawi/ directory. Convert the pcap file to a text file using the
following command:
```
ipsumdump -tsSdDlpF -r ~/mawi/200704121400.dump.gz > ~/mawi/200704121400.ipsum
```

### Upload trace on HDFS
The destination directory should be the same as the tracesHdfsPath variable in 
hashdoop.conf.
 
```
hadoop fs -mkdir -p /user/hashdoop/data/
hadoop fs -put ~/mawi/200704121400.ipsum /user/hashdoop/data/
```

## Running Hashdoop
### Configure Hashdoop
The `hashdoop.conf` file is set by default for the trace and directories
used in this readme. Make sure variables in this file meet your needs.
- `tracesHdfsPath`: HDFS directory where traffic traces are located 
- `sketchesHdfsPath`: HDFS directory where hashed traffic will be stored
- `streamingLib`: jar file of your hadoop streaming
Note that trace names are assumed to be like the ones in the MAWI archive.

### Traffic hashing
Set the “hashSize” parameter in hashdoop.conf.
This parameter controls the  number of sub-traces created with one hash key. Hashdoop uses two
hash keys (i.e. the source and destination address), so it generated `2*hashSize` 
sub-traces.

Execute the (MapReduce) hashing code with the runHashing.py script:
```
python runHashing.py
```

### Anomaly detection 
#### Simple detector:
Set the detection threshold and the output path in the configuration file
(hashdoop.conf), then run:
```
python runSimpleDetector.py
```

#### Astute:
Set the detection threshold, time bin and the output path in the configuration file
(hashdoop.conf), then run:
```
python runAstute.py
```
