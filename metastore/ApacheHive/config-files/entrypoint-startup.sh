#!/bin/sh

echo "#################################"
echo "export environment variables"
# java
echo export JAVA_HOME=/opt/jdk
# apache-hadoop
echo export HADOOP_HOME=/opt/apache-hadoop
echo export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
echo export LD_LIBRARY_PATH=$HADOOP_HOME/lib/native
# apache hive
echo export HIVE_HOME=/opt/apache-hive
echo export HIVE_AUX_JARS_PATH=/opt/apache-hive/lib
echo export PATH=$PATH:$JAVA_HOME:$JAVA_HOME/bin:$HIVE_HOME:$HIVE_HOME/bin:$HIVE_AUX_JARS_PATH:$HADOOP_HOME:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$HADOOP_COMMON_LIB_NATIVE_DIR:$LD_LIBRARY_PATH

# update root password + create database objects if is the first time the container is started
INIT_FILE=/home/hive/initialized.log
if [ ! -f "$INIT_FILE" ]; then
	echo "-> stop mysql service"
	sudo service mysql stop

	echo "-> update root password"
	sudo mysqld_safe --skip-grant-tables --init-file=/home/hive/update-root-password.sql

	sudo service mysql restart

	echo "-> update root password + create hive metastore database objects"
	sudo mysql --user=root --password=root -e "CREATE DATABASE IF NOT EXISTS metastore;SHOW DATABASES;"
	sudo mysql --user=root --password=root metastore < /opt/apache-hive/scripts/metastore/upgrade/mysql/hive-schema-3.1.0.mysql.sql
	sudo mysql --user=root --password=root -e "USE metastore; SHOW TABLES;"

	echo "-> create hiveuser on metastore database objects"
	sudo mysql --user=root --password=root -e "USE metastore;CREATE USER IF NOT EXISTS 'hiveuser'@'%' IDENTIFIED BY 'hiveuserpsswd';"
	echo "-> GRANT PRIVILEGES to hiveuser on metastore daabase objects"
	sudo mysql --user=root --password=root -e "USE metastore;GRANT ALL PRIVILEGES ON *.*  TO 'hiveuser'@'%';FLUSH PRIVILEGES;SHOW GRANTS FOR 'hiveuser';"

	echo "1" > $INIT_FILE
fi

echo "#################################"
echo "-> start mysql service"
sudo service mysql restart

echo "#################################"
echo "-> check status mysql status"
sudo service mysql status

echo "#################################"
#Extra line added in the script to run all command line arguments
exec "$@";
