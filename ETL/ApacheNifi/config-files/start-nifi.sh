#!/bin/sh

# as a service
#sudo /opt/apache-nifi/bin/nifi.sh install

#sudo service nifi stop
#sudo service nifi start
#sudo service nifi status

echo "runing nifi background..."
/opt/apache-nifi/bin/nifi.sh start

echo "checking nifi status..."
/opt/apache-nifi/bin/nifi.sh status

echo "checking nifi port listening..."
netstat -ant|grep LISTEN|grep 59595