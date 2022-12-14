#!/bin/sh

echo "#################################"
echo "export environment variables"
# java
export JAVA_HOME=/opt/jdk
# apache-hadoop
export HADOOP_HOME=/opt/apache-hadoop
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export LD_LIBRARY_PATH=$HADOOP_HOME/lib/native
# apache hive
export HIVE_HOME=/opt/apache-hive
export HIVE_AUX_JARS_PATH=/opt/apache-hive/lib
export PATH=$PATH:$JAVA_HOME:$JAVA_HOME/bin:$HIVE_HOME:$HIVE_HOME/bin:$HIVE_AUX_JARS_PATH:$HADOOP_HOME:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$HADOOP_COMMON_LIB_NATIVE_DIR:$LD_LIBRARY_PATH

HIVE_BIN=/opt/apache-hive/bin

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
echo "create apache-hive objects..."
$HIVE_BIN/hive -v -f /opt/apache-hive/conf/create-hive-metadata-from-delta-lake.hql

echo "#################################"
echo "show apache-hive objects medatata..."
sudo mysql --user=root --password=root --database metastore -e "USE metastore; select * from CTLGS; select * from DBS; select * from TBLS;"
sudo mysql --user=root --password=root --database metastore -e "USE metastore; select DBS.CTLG_NAME as Catalog_Name, DBS.NAME as Schema_Name, DBS.DESC as Schema_Desc, DBS.DB_LOCATION_URI as Schema_Location, DBS.OWNER_NAME as Schema_Owner, DBS.OWNER_TYPE as Schema_Owner_Type, TBLS.TBL_TYPE as Table_Type, TBLS.TBL_NAME as Table_Name, TBLS.OWNER as Table_Owner, TBLS.OWNER_TYPE as Table_Owner_Type from TBLS INNER JOIN DBS ON TBLS.DB_ID = DBS.DB_ID;"

echo "#################################"
echo "-> start mysql service"
sudo service mysql restart

echo "#################################"
echo "-> check status mysql status"
sudo service mysql status

echo "-> start METASTORE service..."
nohup $HIVE_BIN/hive --service metastore --hiveconf hive.root.logger=INFO,console > /home/hive/metastore.log &

echo "-> start hive SERVER + WebUI..."
nohup $HIVE_BIN/hive --service hiveserver2 --hiveconf hive.root.logger=INFO,console > /home/hive/hiveserver2.log &

echo "-> check status Hive METASTORE + SERVER + WebUI..."
jps
ps -aux
echo ""
echo "METASTORE Log..."
tail -n100 /home/hive/metastore.log
echo "METASTORE listening..."
netstat -vanpt | grep 0.0.0.0:9083
echo ""
echo "HIVESERVER Log..."
tail -n100 /home/hive/hiveserver2.log
echo "HIVESERVER listening..."
netstat -vanpt | grep 0.0.0.0:10000
echo "HIVESERVER Web UI listening..."
netstat -vanpt | grep 0.0.0.0:10002

echo "#################################"
#Extra line added in the script to run all command line arguments
exec "$@";