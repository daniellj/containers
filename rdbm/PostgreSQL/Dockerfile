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
  postgresql \
  libcppdb-postgresql0 \
  odbc-postgresql \
  && apt-get clean

RUN dpkg --status postgresql

# Cria usuário para a instalação do Hadoop
RUN useradd -m postgresql && echo "postgresql:supergroup" | chpasswd && adduser postgresql sudo && echo "postgresql ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && cd /usr/bin/ && sudo ln -s python3 python

# Copia o arquivo de configuração do ssh
ADD ./config-files/ssh_config /etc/ssh/ssh_config

# Muda o usuário
USER postgresql

# Cria a chave ssh
#RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && chmod 0600 ~/.ssh/authorized_keys

# Copia os arquivos de configuração da inicialização do container
ADD ./config-files/entrypoint-startup.sh /home/postgresql/entrypoint-startup.sh

# Muda o usuário
USER root

# adjust/clean format shell script file
RUN sudo sed -i -e 's/\r$//' /home/postgresql/entrypoint-startup.sh

# Ajuste dos privilégios
RUN sudo chown -R postgresql:postgresql /home/postgresql/entrypoint-startup.sh
RUN sudo chmod +x /home/postgresql/entrypoint-startup.sh

# Muda o usuário
USER postgresql

ENTRYPOINT ["/home/postgresql/entrypoint-startup.sh"]

EXPOSE 5432