#!/bin/sh

echo "#################################"
echo "export environment variables"
export JAVA_HOME=/opt/jdk
export ZOOKEEPER_HOME=/opt/apache-zookeeper
export PATH=$PATH:$JAVA_HOME:$JAVA_HOME/bin:$ZOOKEEPER_HOME:$ZOOKEEPER_HOME/bin

echo "#################################"
echo "restart ssh service"
sudo service ssh restart

echo "#################################"
echo "stop Apache Zookeeper service..."
#/opt/apache-zookeeper/bin/zkServer.sh stop /opt/apache-zookeeper/conf/zoo.cfg
service zookeeper stop

echo "#################################"
echo "start Apache Zookeeper service..."
#/opt/apache-zookeeper/bin/zkServer.sh start /opt/apache-zookeeper/conf/zoo.cfg
service zookeeper start

echo "#################################"
echo "restart Apache Zookeeper service..."
#/opt/apache-zookeeper/bin/zkServer.sh restart /opt/apache-zookeeper/conf/zoo.cfg
service zookeeper restart

echo "#################################"
echo "check Apache Zookeeper service..."
#/opt/apache-zookeeper/bin/zkServer.sh status
service zookeeper status

echo "#################################"
#Extra line added in the script to run all command line arguments
exec "$@";