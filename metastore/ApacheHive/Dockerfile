FROM ubuntu:latest

# Updates e instalações
RUN \
  apt-get update && apt-get install -y \
  openssh-server \
  openssh-client \
  python3 \
  rsync \
  mysql-server \
  mysql-client \
  sudo \
  arp-scan \
  net-tools \
  iputils-ping \
  vim \
  && apt-get clean

# Cria usuário para a instalação do Hadoop
RUN useradd -m hive && echo "hive:supergroup" | chpasswd && adduser hive sudo && echo "hive ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && cd /usr/bin/ && sudo ln -s python3 python

# Copia os binários do JDK + Apache Hadoop + Apache Hive + MySQL Connector JAR (que servira de metastore)
ADD ./binaries/jdk /opt/jdk
ADD ./binaries/apache-hadoop /opt/apache-hadoop
ADD ./binaries/apache-hive /opt/apache-hive
ADD ./binaries/mysql/mysql-connector/mysql-connector-j-8.0.31.jar /opt/apache-hive/lib
ADD ./binaries/delta-lake/delta-hive-assembly_2.13-0.5.0.jar /opt/apache-hive/lib/delta-hive-assembly_2.13-0.5.0.jar

# Variáveis de ambiente - docker
# java
ENV JAVA_HOME=/opt/jdk
# apache-hadoop
ENV HADOOP_HOME=/opt/apache-hadoop
ENV HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
ENV LD_LIBRARY_PATH=$HADOOP_HOME/lib/native
# apache hive
ENV HIVE_HOME=/opt/apache-hive
ENV HIVE_AUX_JARS_PATH=/opt/apache-hive/lib
ENV PATH=$PATH:$JAVA_HOME:$JAVA_HOME/bin:$HIVE_HOME:$HIVE_HOME/bin:$HIVE_AUX_JARS_PATH:$HADOOP_HOME:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$HADOOP_COMMON_LIB_NATIVE_DIR:$LD_LIBRARY_PATH

# Muda o usuário
USER hive

# Variáveis de ambiente
# java
RUN echo "export JAVA_HOME=/opt/jdk" >> ~/.bashrc
# apache-hadoop
RUN echo "export HADOOP_HOME=/opt/apache-hadoop" >> ~/.bashrc
RUN echo "export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native" >> ~/.bashrc
RUN echo "export LD_LIBRARY_PATH=$HADOOP_HOME/lib/native" >> ~/.bashrc
# apache hive
RUN echo "export HIVE_HOME=/opt/apache-hive" >> ~/.bashrc
RUN echo "export HIVE_AUX_JARS_PATH=/opt/apache-hive/lib" >> ~/.bashrc
RUN echo "export PATH=$PATH:$JAVA_HOME:$JAVA_HOME/bin:$HIVE_HOME:$HIVE_HOME/bin:$HIVE_AUX_JARS_PATH:$HADOOP_HOME:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$HADOOP_COMMON_LIB_NATIVE_DIR:$LD_LIBRARY_PATH" >> ~/.bashrc

# Muda o usuário
USER root

# Copia os arquivos de configuração do Hadoop
ADD ./config-files/update-root-password.sql /home/hive/update-root-password.sql
ADD ./config-files/ssh_config /etc/ssh/ssh_config
ADD ./config-files/entrypoint-startup.sh /home/hive/entrypoint-startup.sh
ADD ./config-files/hive-site.xml /opt/apache-hive/conf/hive-site.xml
ADD ./config-files/hive-env.sh /opt/apache-hive/conf/hive-env.sh
ADD ./config-files/core-site.xml /opt/apache-hadoop/etc/hadoop/core-site.xml
ADD ./config-files/hadoop-env.sh /opt/apache-hadoop/etc/hadoop/hadoop-env.sh
ADD ./config-files/hdfs-site.xml /opt/apache-hadoop/etc/hadoop/hdfs-site.xml
ADD ./config-files/create-hive-metadata-from-delta-lake.hql /opt/apache-hive/conf/create-hive-metadata-from-delta-lake.hql

# Ajuste dos privilégios
RUN sudo chown -R hive:hive /opt/jdk
RUN sudo chown -R hive:hive /opt/apache-hive
RUN sudo chown -R hive:hive /opt/apache-hadoop
RUN sudo chown -R hive:hive /home/hive
RUN sudo chmod +x /home/hive/entrypoint-startup.sh

# adjust/clean format shell script file
RUN sudo sed -i -e 's/\r$//' /home/hive/update-root-password.sql
RUN sudo sed -i -e 's/\r$//' /etc/ssh/ssh_config
RUN sudo sed -i -e 's/\r$//' /home/hive/entrypoint-startup.sh
RUN sudo sed -i -e 's/\r$//' /opt/apache-hive/conf/hive-site.xml
RUN sudo sed -i -e 's/\r$//' /opt/apache-hive/conf/hive-env.sh
RUN sudo sed -i -e 's/\r$//' /opt/apache-hadoop/etc/hadoop/core-site.xml
RUN sudo sed -i -e 's/\r$//' /opt/apache-hadoop/etc/hadoop/hadoop-env.sh
RUN sudo sed -i -e 's/\r$//' /opt/apache-hadoop/etc/hadoop/hdfs-site.xml
RUN sudo sed -i -e 's/\r$//' /opt/apache-hive/conf/create-hive-metadata-from-delta-lake.hql

# Muda o usuário
USER hive

ENTRYPOINT ["/home/hive/entrypoint-startup.sh"]

# Portas que poderão ser usadas
EXPOSE 3306 9083