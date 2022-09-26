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
RUN useradd -m flume && echo "flume:supergroup" | chpasswd && adduser flume sudo && echo "flume ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && cd /usr/bin/ && sudo ln -s python3 python

# Copia o arquivo de configuração do ssh
ADD ./config-files/ssh_config /etc/ssh/ssh_config

# Muda o usuário
USER flume

# Cria a chave ssh
#RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && chmod 0600 ~/.ssh/authorized_keys

# Copia os binários do JDK
ADD ./binaries/jdk /opt/jdk

# Variáveis de ambiente JDK
ENV JAVA_HOME=/opt/jdk
ENV PATH=$PATH:$JAVA_HOME:$JAVA_HOME/bin

# Copia os binários do apache-flume
ADD ./binaries/apache-flume /opt/apache-flume

# Copia os arquivos de configuração do apache-flume
ADD ./config-files/flume-env.sh /opt/apache-flume/conf/
ADD ./config-files/twitter.conf /opt/apache-flume/conf/

# Copia bibliotecas do Hadoop para o Apache Flume
ADD ./binaries/hadoop-lib /opt/apache-flume/lib

# Variáveis de ambiente do apache-flume
ENV FLUME_HOME=/opt/apache-flume
#ENV FLUME_CLASSPATH=/opt/apache-flume/lib
#ENV PATH=$PATH:$FLUME_HOME:$FLUME_HOME/bin:$FLUME_CLASSPATH
ENV PATH=$PATH:$FLUME_HOME:$FLUME_HOME/bin

# ~/.bashrc
RUN echo "export JAVA_HOME=/opt/jdk" >> ~/.bashrc
RUN echo "export FLUME_HOME=/opt/apache-flume" >> ~/.bashrc
#RUN echo "export FLUME_CLASSPATH=/opt/apache-flume/lib" >> ~/.bashrc
#RUN echo "export PATH=$PATH:$JAVA_HOME:$JAVA_HOME/bin:$FLUME_HOME:$FLUME_HOME/bin:$FLUME_CLASSPATH" >> ~/.bashrc
RUN echo "export PATH=$PATH:$JAVA_HOME:$JAVA_HOME/bin:$FLUME_HOME:$FLUME_HOME/bin" >> ~/.bashrc

# Copia os arquivos de configuração da inicialização do container
ADD ./config-files/twitter_agent.sh /home/flume/twitter_agent.sh
ADD ./config-files/entrypoint-startup.sh /home/flume/entrypoint-startup.sh

# Muda o usuário
USER root

# Ajuste dos privilégios
RUN sudo chown -R flume:flume /opt/jdk
RUN sudo chown -R flume:flume /opt/apache-flume
RUN sudo chown -R flume:flume /home/flume/twitter_agent.sh
RUN sudo chown -R flume:flume /home/flume/entrypoint-startup.sh
RUN sudo chmod +x /home/flume/twitter_agent.sh
RUN sudo chmod +x /home/flume/entrypoint-startup.sh

# adjust/clean format shell script file
RUN sudo sed -i -e 's/\r$//' /opt/apache-flume/conf/flume-env.sh
RUN sudo sed -i -e 's/\r$//' /opt/apache-flume/conf/twitter.conf
RUN sudo sed -i -e 's/\r$//' /home/flume/twitter_agent.sh
RUN sudo sed -i -e 's/\r$//' /home/flume/entrypoint-startup.sh

# Muda o usuário
USER flume

# Pasta de trabalho
WORKDIR /home/flume

ENTRYPOINT ["/home/flume/entrypoint-startup.sh"]