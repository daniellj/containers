FROM ubuntu:latest

# Updates e instalações
RUN \
  apt-get update && apt-get install -y \
  openssh-server \
  python3 \
  rsync \
  sudo \
  arp-scan \
  net-tools \
  iputils-ping \
  vim \
  && apt-get clean

# Cria usuário para a instalação do Hadoop
RUN useradd -m nifi && echo "nifi:supergroup" | chpasswd && adduser nifi sudo && echo "nifi ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && cd /usr/bin/ && sudo ln -s python3 python

# Copia o arquivo de configuração do ssh
ADD ./config-files/ssh_config /etc/ssh/ssh_config

# Muda o usuário
USER nifi

# Cria a chave ssh
#RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && chmod 0600 ~/.ssh/authorized_keys

# Copia os binários do JDK
ADD ./binaries/jdk /opt/jdk

# Variáveis de ambiente JDK
ENV JAVA_HOME=/opt/jdk
ENV PATH=$PATH:$JAVA_HOME:$JAVA_HOME/bin

# Copia os binários do apache-nifi
ADD ./binaries/apache-nifi /opt/apache-nifi

# Remove arquivos de configuração do Nifi
RUN sudo rm -rf /opt/apache-nifi/bin/nifi-env.sh

# Copia os arquivos de configuração do apache-nifi
ADD ./config-files/nifi-env.sh /opt/apache-nifi/bin

# Copia os arquivos de configuração do cluster hadoop
RUN sudo mkdir /opt/hadoop
RUN sudo mkdir /opt/hadoop/conf
ADD ./config-files/core-site.xml /opt/hadoop/conf
ADD ./config-files/hdfs-site.xml /opt/hadoop/conf

# ~/.bashrc
RUN echo "export JAVA_HOME=/opt/jdk" >> ~/.bashrc
RUN echo "export PATH=$PATH:$JAVA_HOME:$JAVA_HOME/bin" >> ~/.bashrc

# Copia os arquivos de configuração da inicialização do container
ADD ./config-files/entrypoint-startup.sh /home/nifi/entrypoint-startup.sh
ADD ./config-files/start-nifi.sh /home/nifi/start-nifi.sh

# Muda o usuário
USER root

# Ajuste dos privilégios
RUN sudo chown -R nifi:nifi /opt/jdk
RUN sudo chown -R nifi:nifi /opt/apache-nifi
RUN sudo chown -R nifi:nifi /opt/hadoop
RUN sudo chown -R nifi:nifi /home/nifi/entrypoint-startup.sh
RUN sudo chown -R nifi:nifi /home/nifi/start-nifi.sh
RUN sudo chmod +x /home/nifi/entrypoint-startup.sh
RUN sudo chmod +x /home/nifi/start-nifi.sh

# adjust/clean format shell script file
RUN sudo sed -i -e 's/\r$//' /opt/apache-nifi/bin/nifi-env.sh
RUN sudo sed -i -e 's/\r$//' /opt/hadoop/conf/core-site.xml
RUN sudo sed -i -e 's/\r$//' /opt/hadoop/conf/hdfs-site.xml
RUN sudo sed -i -e 's/\r$//' /home/nifi/entrypoint-startup.sh
RUN sudo sed -i -e 's/\r$//' /home/nifi/start-nifi.sh

# adjust /opt/apache-nifi/conf/nifi.properties
RUN sudo sed -i -e 's/nifi.web.https.host=127.0.0.1/nifi.web.https.host=0.0.0.0/g' /opt/apache-nifi/conf/nifi.properties
RUN sudo sed -i -e 's/nifi.web.https.port=8443/nifi.web.https.port=59595/g' /opt/apache-nifi/conf/nifi.properties

# Muda o usuário
USER nifi

# Pasta de trabalho
WORKDIR /home/nifi

ENTRYPOINT ["/home/nifi/entrypoint-startup.sh"]
EXPOSE 59595