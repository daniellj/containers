#!/bin/sh

echo "#################################"
echo "export environment variables"
export JAVA_HOME=/opt/jdk
export ZOOKEEPER_HOME=/opt/apache-zookeeper
export KAFKA_OPTS="-Djava.security.auth.login.config=/opt/apache-zookeeper/conf/zoo_jaas.conf"
export SERVER_JVMFLAGS="-Djava.security.auth.login.config=/opt/apache-zookeeper/conf/zoo_jaas.conf"
export PATH=$PATH:$JAVA_HOME:$JAVA_HOME/bin:$ZOOKEEPER_HOME:$ZOOKEEPER_HOME/bin:$KAFKA_OPTS:$SERVER_JVMFLAGS

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