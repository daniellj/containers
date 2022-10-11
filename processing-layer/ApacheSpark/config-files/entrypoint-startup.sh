#!/bin/bash

echo "#################################"
echo "export environment variables"
export JAVA_HOME=/opt/jdk
export SPARK_HOME=/opt/apache-spark
export PATH=$PATH:$JAVA_HOME:$JAVA_HOME/bin:$SPARK_HOME:$SPARK_HOME/bin:$SPARK_HOME/sbin

echo "#################################"
echo "restart ssh service"
sudo service ssh restart

#echo "adjust /etc/hosts"
#grep -xF '172.19.0.250 spark-master' /etc/hosts || echo '172.19.0.250 spark-master' >> /etc/hosts
#grep -xF '172.19.0.251 spark-node1' /etc/hosts || echo '172.19.0.251 spark-node1' >> /etc/hosts
#grep -xF '172.19.0.252 spark-node2' /etc/hosts || echo '172.19.0.252 spark-node2' >> /etc/hosts

echo '### showing /etc/hosts content ###'
cat /etc/hosts

if [ "$HOSTNAME" = spark-master ]; then
	echo '### Send the authorized_keys to another nodes ###'
	NODE1=spark-node1
	NODE2=spark-node2
	#sshpass -p "" scp -o StrictHostKeyChecking=no /home/spark/.ssh/authorized_keys spark@$NODE1:/home/spark/.ssh
	#sshpass -p "" scp -o StrictHostKeyChecking=no /home/spark/.ssh/authorized_keys spark@$NODE2:/home/spark/.ssh
    KEY=$(cat ~/.ssh/id_rsa.pub) || sshpass -p "" ssh -p 22 spark@$NODE1 "if [ -z \"\$(grep \"$KEY\" ~/.ssh/authorized_keys )\" ]; then echo $KEY >> ~/.ssh/authorized_keys; echo key added.; fi;"
	KEY=$(cat ~/.ssh/id_rsa.pub) || sshpass -p "" ssh -p 22 spark@$NODE2 "if [ -z \"\$(grep \"$KEY\" ~/.ssh/authorized_keys )\" ]; then echo $KEY >> ~/.ssh/authorized_keys; echo key added.; fi;"

	echo '### Start in background Apache Spark on master node ###'
	nohup /opt/apache-spark/sbin/start-all.sh &>/dev/null &
	sleep 10
	jps
else
    echo 'This is not a spark-master. Hostname = $HOSTNAME'
	jps
fi
