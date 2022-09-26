#!/bin/sh

echo "#################################"
echo "export environment variables"
export JAVA_HOME=/opt/jdk
export FLUME_HOME=/opt/apache-flume
#export FLUME_CLASSPATH=/opt/apache-flume/lib
#export PATH=$PATH:$JAVA_HOME:$JAVA_HOME/bin:$FLUME_HOME:$FLUME_HOME/bin:$FLUME_CLASSPATH
export PATH=$PATH:$JAVA_HOME:$JAVA_HOME/bin:$FLUME_HOME:$FLUME_HOME/bin

echo "#################################"
echo "restart ssh service"
sudo service ssh restart

echo "#################################"
echo "start Apache Flume Agent for Twitter (background)..."
nohup /home/flume/twitter_agent.sh &

echo "#################################"
#Extra line added in the script to run all command line arguments
exec "$@";