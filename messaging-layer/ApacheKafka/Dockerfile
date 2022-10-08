FROM ubuntu:latest

# Updates e instalações
RUN \
  apt-get update && apt-get install -y \
  openssh-server \
  python3 \
  pip \
  rsync \
  sudo \
  arp-scan \
  net-tools \
  iputils-ping \
  vim \
  && apt-get clean

# Cria usuário para a instalação do Hadoop
RUN useradd -m kafka && echo "kafka:supergroup" | chpasswd && adduser kafka sudo && echo "kafka ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && cd /usr/bin/ && sudo ln -s python3 python

# Copia o arquivo de configuração do ssh
ADD ./config-files/ssh_config /etc/ssh/ssh_config

# Muda o usuário
USER kafka

# Cria a chave ssh
#RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && chmod 0600 ~/.ssh/authorized_keys

# Copia os binários do JDK
ADD ./binaries/jdk /opt/jdk

# Variáveis de ambiente JDK
ENV JAVA_HOME=/opt/jdk
ENV KAFKA_OPTS="-Djava.security.auth.login.config=/opt/apache-kafka/config/kafka_server_jaas.conf"
ENV PATH=$PATH:$JAVA_HOME:$JAVA_HOME/bin:$KAFKA_OPTS

# Copia os binários do apache-kafka
ADD ./binaries/apache-kafka /opt/apache-kafka

# deleta o(s) arquivo(s) configuração do apache-kafka se existir(em)
RUN sudo rm -rf /opt/apache-kafka/config/config.properties
RUN sudo rm -rf /opt/apache-kafka/config/app_producer_01.conf
RUN sudo rm -rf /opt/apache-kafka/config/kafka_server_jaas.conf
RUN sudo rm -rf /opt/apache-kafka/config/consumer.properties
RUN sudo rm -rf /opt/apache-kafka/config/kafka_client_jaas.conf
RUN sudo rm -rf /opt/apache-kafka/config/producer.properties
RUN sudo rm -rf /opt/apache-kafka/config/server-00.properties
RUN sudo rm -rf /opt/apache-kafka/config/server-01.properties
RUN sudo rm -rf /opt/apache-kafka/config/server-02.properties
RUN sudo rm -rf /etc/init.d/kafka-broker-00
RUN sudo rm -rf /etc/init.d/kafka-broker-01
RUN sudo rm -rf /etc/init.d/kafka-broker-02
RUN sudo rm -rf /home/kafka/app

# Copia os arquivos de configuração do apache-kafka
ADD ./config-files/config.properties /opt/apache-kafka/config/config.properties
ADD ./config-files/app_producer_01.conf /opt/apache-kafka/config/app_producer_01.conf
ADD ./config-files/kafka_server_jaas.conf /opt/apache-kafka/config/kafka_server_jaas.conf
ADD ./config-files//consumer.properties /opt/apache-kafka/config/consumer.properties
ADD ./config-files/kafka_client_jaas.conf /opt/apache-kafka/config/kafka_client_jaas.conf
ADD ./config-files/producer.properties /opt/apache-kafka/config/producer.properties
ADD ./config-files/server-00.properties /opt/apache-kafka/config/server-00.properties
ADD ./config-files/server-01.properties /opt/apache-kafka/config/server-01.properties
ADD ./config-files/server-02.properties /opt/apache-kafka/config/server-02.properties
ADD ./config-files/kafka-broker-00 /etc/init.d/kafka-broker-00
ADD ./config-files/kafka-broker-01 /etc/init.d/kafka-broker-01
ADD ./config-files/kafka-broker-02 /etc/init.d/kafka-broker-02
ADD ./config-files/app /home/kafka/app

# Variáveis de ambiente do apache-kafka
ENV KAFKA_HOME=/opt/apache-kafka
ENV PATH=$PATH:$KAFKA_HOME:$KAFKA_HOME/bin

# ~/.bashrc
RUN echo "export JAVA_HOME=/opt/jdk" >> ~/.bashrc
RUN echo "export KAFKA_HOME=/opt/apache-kafka" >> ~/.bashrc
RUN echo "export KAFKA_OPTS="-Djava.security.auth.login.config=/opt/apache-kafka/config/kafka_server_jaas.conf""
RUN echo "export PATH=$PATH:$JAVA_HOME:$JAVA_HOME/bin:$KAFKA_HOME:$KAFKA_HOME/bin:$KAFKA_OPTS" >> ~/.bashrc

# Copia os arquivos de configuração da inicialização do container
ADD ./config-files/entrypoint-startup.sh /home/kafka/entrypoint-startup.sh

# Muda o usuário
USER root

# cria a pasta dos dados persistido do apache kafka
RUN mkdir /data
RUN mkdir /data/kafka-logs-boker-00
RUN mkdir /data/kafka-logs-boker-01
RUN mkdir /data/kafka-logs-boker-02

# adjust/clean format shell script file
RUN sudo sed -i -e 's/\r$//' /opt/apache-kafka/config/config.properties
RUN sudo sed -i -e 's/\r$//' /home/kafka/entrypoint-startup.sh
RUN sudo sed -i -e 's/\r$//' /opt/apache-kafka/config/app_producer_01.conf
RUN sudo sed -i -e 's/\r$//' /opt/apache-kafka/config/kafka_server_jaas.conf
RUN sudo sed -i -e 's/\r$//' /opt/apache-kafka/config/consumer.properties
RUN sudo sed -i -e 's/\r$//' /opt/apache-kafka/config/kafka_client_jaas.conf
RUN sudo sed -i -e 's/\r$//' /opt/apache-kafka/config/producer.properties
RUN sudo sed -i -e 's/\r$//' /opt/apache-kafka/config/server-00.properties
RUN sudo sed -i -e 's/\r$//' /opt/apache-kafka/config/server-01.properties
RUN sudo sed -i -e 's/\r$//' /opt/apache-kafka/config/server-02.properties
RUN sudo sed -i -e 's/\r$//' /etc/init.d/kafka-broker-00
RUN sudo sed -i -e 's/\r$//' /etc/init.d/kafka-broker-01
RUN sudo sed -i -e 's/\r$//' /etc/init.d/kafka-broker-02
RUN sudo sed -i -e 's/\r$//' /home/kafka/app/kafkaconsumer.py
RUN sudo sed -i -e 's/\r$//' /home/kafka/app/kafkaproducer.py
RUN sudo sed -i -e 's/\r$//' /home/kafka/app/requirements.txt

# install python requirements
RUN sudo pip install -r /home/kafka/app/requirements.txt

# Ajuste dos privilégios
RUN sudo chown -R kafka:kafka /data
RUN sudo chmod 0755 -R /data

RUN sudo chown -R kafka:kafka /home/kafka
RUN sudo chown -R kafka:kafka /opt/jdk
RUN sudo chown -R kafka:kafka /opt/apache-kafka
RUN sudo chown -R kafka:kafka /home/kafka/entrypoint-startup.sh
RUN sudo chmod +x /home/kafka/entrypoint-startup.sh
RUN sudo chown root:root /etc/init.d/kafka-broker-00
RUN sudo chown root:root /etc/init.d/kafka-broker-01
RUN sudo chown root:root /etc/init.d/kafka-broker-02
RUN sudo chmod 0755 /etc/init.d/kafka-broker-00
RUN sudo chmod 0755 /etc/init.d/kafka-broker-01
RUN sudo chmod 0755 /etc/init.d/kafka-broker-02
RUN sudo update-rc.d kafka-broker-00 defaults
RUN sudo update-rc.d kafka-broker-01 defaults
RUN sudo update-rc.d kafka-broker-02 defaults

# Muda o usuário
USER kafka

# Add the cron job (need cron app installed)
#RUN crontab -l | { cat; echo "@reboot nohup /opt/apache-kafka/bin/kafka-server-start.sh /opt/apache-kafka/config/server-00.properties &>/dev/null &"; } | crontab -
#RUN crontab -l | { cat; echo "@reboot nohup /opt/apache-kafka/bin/kafka-server-start.sh /opt/apache-kafka/config/server-01.properties &>/dev/null &"; } | crontab -
#RUN crontab -l | { cat; echo "@reboot nohup /opt/apache-kafka/bin/kafka-server-start.sh /opt/apache-kafka/config/server-02.properties &>/dev/null &"; } | crontab -

# Pasta de trabalho
WORKDIR /home/kafka

ENTRYPOINT ["/home/kafka/entrypoint-startup.sh"]

EXPOSE 19092 19093 19094