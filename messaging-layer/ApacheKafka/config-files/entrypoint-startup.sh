#!/bin/sh

echo "#################################"
echo "export environment variables"
export JAVA_HOME=/opt/jdk
export KAFKA_HOME=/opt/apache-kafka
export KAFKA_OPTS="-Djava.security.auth.login.config=/opt/apache-kafka/config/kafka_server_jaas.conf"
export PATH=$PATH:$JAVA_HOME:$JAVA_HOME/bin:$KAFKA_HOME:$KAFKA_HOME/bin:$KAFKA_OPTS

echo "#################################"
echo "restart ssh service"
sudo service ssh restart

echo "############################ STOP KAFKA BROKERS ##############################"
echo "stop Apache Kafka service...BROKER=0"
/opt/apache-kafka/bin/kafka-server-stop.sh /opt/apache-kafka/config/server-00.properties
#service kafka-broker-00 stop

echo "stop Apache Kafka service...BROKER=1"
/opt/apache-kafka/bin/kafka-server-stop.sh /opt/apache-kafka/config/server-01.properties
#service kafka-broker-01 stop

echo "stop Apache Kafka service...BROKER=2"
/opt/apache-kafka/bin/kafka-server-stop.sh /opt/apache-kafka/config/server-02.properties
#service kafka-broker-02 stop
sleep 5

echo "<<<<<<<<############################ START KAFKA BROKER=0 ##############################>>>>>>>>>"
nohup /opt/apache-kafka/bin/kafka-server-start.sh /opt/apache-kafka/config/server-00.properties &>/dev/null &
#service kafka-broker-00 start
sleep 3

echo "<<<<<<<<############################ START KAFKA BROKER=1 ##############################>>>>>>>>>"
nohup /opt/apache-kafka/bin/kafka-server-start.sh /opt/apache-kafka/config/server-01.properties &>/dev/null &
#service kafka-broker-01 start
sleep 3

echo "<<<<<<<<############################ START KAFKA BROKER=2 ##############################>>>>>>>>>"
nohup /opt/apache-kafka/bin/kafka-server-start.sh /opt/apache-kafka/config/server-02.properties &>/dev/null &
#service kafka-broker-02 start
sleep 3

echo "<<<<<<<<############################ STATUS KAFKA BROKER=0 ##############################>>>>>>>>>"
service kafka-broker-00 status
echo "<<<<<<<<############################ STATUS KAFKA BROKER=1 ##############################>>>>>>>>>"
service kafka-broker-01 status
echo "<<<<<<<<############################ STATUS KAFKA BROKER=2 ##############################>>>>>>>>>"
service kafka-broker-02 status

echo "############################## create or update admin user in Kafka ##############################"
#/opt/apache-kafka/bin/kafka-configs.sh --zookeeper zookeeper_worker_01:2181,zookeeper_worker_02:2181,zookeeper_worker_03:2181 --alter --add-config 'SCRAM-SHA-512=[password=admin-secret]' --entity-type users --entity-name admin
/opt/apache-kafka/bin/kafka-configs.sh --bootstrap-server kafka:9092,kafka:9093,kafka:9094 --alter --add-config 'SCRAM-SHA-512=[password=admin-secret]' --entity-type users --entity-name admin --command-config /opt/apache-kafka/config/config.properties
sleep 3

#echo "<<<<<<<<############################ START KAFKA PRODUCER ##############################>>>>>>>>>"
#sleep 10
#python /home/kafka/app/kafkaproducer.py

echo "#################################"
#Extra line added in the script to run all command line arguments
exec "$@";