#!/bin/sh

echo "#################################"
echo "export environment variables"
export JAVA_HOME=/opt/jdk
export PATH=$PATH:$JAVA_HOME:$JAVA_HOME/bin

echo "#################################"
echo "restart ssh service"
sudo service ssh restart

echo "#################################"
echo "starting Apache Nifi..."
/home/nifi/start-nifi.sh

echo "#################################"
#Extra line added in the script to run all command line arguments
exec "$@";