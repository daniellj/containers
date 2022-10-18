FROM ubuntu:latest

# Updates e instalações
RUN \
  apt-get update && apt-get install -y \
  openssh-server \
  openssh-client \
  python3 \
  rsync \
  sudo \
  arp-scan \
  net-tools \
  iputils-ping \
  vim \
  && apt-get clean

# Cria usuário para a instalação do Hadoop
RUN useradd -m hduser && echo "hduser:supergroup" | chpasswd && adduser hduser sudo && echo "hduser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && cd /usr/bin/ && sudo ln -s python3 python

# Copia o arquivo de configuração do ssh
ADD ./config-files/ssh_config /etc/ssh/ssh_config

RUN echo "hduser:hduser" | chpasswd

# Muda o usuário
USER hduser

# Pasta de trabalho
WORKDIR /home/hduser

# Cria a chave ssh
RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && chmod 0600 ~/.ssh/authorized_keys

# Usuário de trabalho
ENV HDFS_NAMENODE_USER=hduser
ENV HDFS_DATANODE_USER=hduser
ENV HDFS_SECONDARYNAMENODE_USER=hduser
ENV YARN_RESOURCEMANAGER_USER=hduser
ENV YARN_NODEMANAGER_USER=hduser

# Copia os binários do JDK
ADD ./binaries/jdk ./jdk

# Variáveis de ambiente JDK
ENV JAVA_HOME=/home/hduser/jdk
ENV PATH=$PATH:$JAVA_HOME:$JAVA_HOME/bin

# Copia os binários do Hadoop
ADD ./binaries/hadoop ./hadoop

# Variáveis de ambiente do Hadoop
ENV HADOOP_HOME=/home/hduser/hadoop
ENV HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
ENV LD_LIBRARY_PATH=$HADOOP_HOME/lib/native
ENV PATH=$PATH:$HADOOP_HOME:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$HADOOP_COMMON_LIB_NATIVE_DIR

# Pastas para os arquivos do NameNode
RUN mkdir /home/hduser/hdfs
RUN mkdir /home/hduser/hdfs/namenode

# Variáveis de ambiente
RUN echo "export PATH=$PATH" >> ~/.bashrc
RUN echo "export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native" >> ~/.bashrc
RUN echo "export LD_LIBRARY_PATH=$HADOOP_HOME/lib/native" >> ~/.bashrc

# Copia os arquivos de configuração do Hadoop
ADD ./config-files/hadoop-env.sh $HADOOP_HOME/etc/hadoop/
ADD ./config-files/core-site.xml $HADOOP_HOME/etc/hadoop/
ADD ./config-files/hdfs-site.xml $HADOOP_HOME/etc/hadoop/
ADD ./config-files/workers $HADOOP_HOME/etc/hadoop/

# Copia os arquivos de configuração da inicialização do container
ADD ./config-files/entrypoint-startup.sh /home/hduser/entrypoint-startup.sh

# Muda o usuário
USER root

# Ajuste dos privilégios
RUN sudo chown -R hduser:hduser /home/hduser/jdk
RUN sudo chown -R hduser:hduser /home/hduser/hadoop
RUN sudo chown -R hduser:hduser /home/hduser/entrypoint-startup.sh
RUN sudo chmod +x /home/hduser/entrypoint-startup.sh

# adjust/clean format shell script file
RUN sudo sed -i -e 's/\r$//' /home/hduser/entrypoint-startup.sh

# Muda o usuário
USER hduser

ENTRYPOINT ["/home/hduser/entrypoint-startup.sh"]

# Portas que poderão ser usadas
#EXPOSE 50070 50075 50010 50020 50090 8020 9000 9864 9870 8030 8031 8032 8033 8040 8042 22
EXPOSE 22 8020 9870 50030
