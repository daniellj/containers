#!/bin/sh

echo "#################################"
echo "export environment variables"
export HADOOP_HOME=/home/hduser/hadoop
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export LD_LIBRARY_PATH=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$HADOOP_COMMON_LIB_NATIVE_DIR:$LD_LIBRARY_PATH

echo "#################################"
echo "restart ssh service"
sudo service ssh restart

echo "#################################"
echo "stop hdfs on DataNode"
hdfs --daemon stop datanode

#echo "#################################"
#echo "format NameNode"
#hdfs namenode -format

echo "#################################"
echo "start hdfs on DataNode"
hdfs --daemon start datanode

echo "#################################"
echo "check status hadoop cluster"
jps

echo "#################################"

#Extra line added in the script to run all command line arguments
exec "$@";
