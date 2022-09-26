#!/bin/sh

# flume-ng -> agent
# --conf -> configuration path
# -f -> configuration file
# -Dflume.root.logger=DEBUG,console -n TwitterAgent -> debug mode in screen for the TwitterAgent within /opt/apache-flume/conf/twitter.conf

/opt/apache-flume/bin/flume-ng agent --conf /opt/apache-flume/conf/ -f /opt/apache-flume/conf/twitter.conf -Dflume.root.logger=DEBUG,console -n TwitterAgent