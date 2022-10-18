#!/bin/sh

echo "#################################"
echo "export environment variables"
export PATH=$PATH
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export LD_LIBRARY_PATH=$HADOOP_HOME/lib/native

echo "#################################"
echo "restart ssh service"
sudo service ssh restart

echo "#################################"
echo "stop hdfs on NameNode"
hdfs --daemon stop namenode

#echo "#################################"
#echo "format NameNode"
#hdfs namenode -format

echo "#################################"
echo "copy authorized keys for ssh servers"
#ssh-copy-id -p 22 -f -i /home/hduser/.ssh/id_rsa.pub hduser@datanode1
#ssh-copy-id -p 22 -f -i /home/hduser/.ssh/id_rsa.pub hduser@datanode2

if [ "$HOSTNAME" = hdpmaster ]; then
	echo '### Send the authorized_keys to another nodes ###'
	NODE1=datanode1
	NODE2=datanode2
    KEY=$(cat ~/.ssh/id_rsa.pub)
	sshpass -p hduser ssh -p 22 hduser@$NODE1 "if [ -z \"\$(grep \"$KEY\" ~/.ssh/authorized_keys )\" ]; then echo $KEY >> ~/.ssh/authorized_keys; echo key added.; fi;"
	sshpass -p hduser ssh -p 22 hduser@$NODE2 "if [ -z \"\$(grep \"$KEY\" ~/.ssh/authorized_keys )\" ]; then echo $KEY >> ~/.ssh/authorized_keys; echo key added.; fi;"

	echo "#################################"
	echo "start hdfs on NameNode"
	hdfs --daemon start namenode

	echo "#################################"
	echo "check status hadoop cluster"
	sleep 10
	jps
else
    echo 'This is not a hduser-master. Hostname = $HOSTNAME'
	jps
fi

echo "#################################"
#Extra line added in the script to run all command line arguments
exec "$@";
