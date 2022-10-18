FROM ubuntu:latest

# Prerequisites
RUN \
  apt-get update && apt-get install -y \
  python3 \
  pip \
  python3-venv \
  npm \
  nodejs \
  sudo \
  arp-scan \
  net-tools \
  iputils-ping \
  unzip \
  vim \
  && apt-get clean

# Cria usuário para a instalação
RUN useradd -m jupyterhub && echo "jupyterhub:supergroup" | chpasswd && adduser jupyterhub sudo && echo "jupyterhub ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && cd /usr/bin/ && sudo ln -s python3 python

# Create "admin" for jupyterhub
RUN useradd -m admin
RUN echo "admin:admin" | chpasswd
RUN mkdir /home/admin/notebooks
RUN sudo chown -R admin:admin /home/admin
RUN sudo chmod 770 -R /home/admin/notebooks

######## JDK instalation ########
# Copia os binários do JDK
ADD ./binaries/jdk /opt/jdk
RUN chown -R jupyterhub:root /opt/jdk
RUN chmod -R 775 /opt/jdk
#################################

# Muda o usuário
USER admin

# ~/.bashrc admin user
RUN export JAVA_HOME=/opt/jdk
RUN export PATH=$PATH:$JAVA_HOME:/opt/jdk/:/opt/jdk/bin
RUN echo "export JAVA_HOME=/opt/jdk" >> ~/.bashrc
RUN echo "export PATH=$PATH:/opt/jdk:/opt/jdk/bin" >> ~/.bashrc


# Muda o usuário
USER root

# ~/.bashrc root user
RUN export JAVA_HOME=/opt/jdk
RUN export PATH=$PATH:$JAVA_HOME:/opt/jdk/:/opt/jdk/bin

# Paths
RUN cd /
RUN mkdir -p srv
RUN mkdir -p /srv/jupyterhub
RUN mkdir -p /etc/jupyterhub

# Install JupyterHub
RUN npm install -g configurable-http-proxy
RUN python -m venv /srv/jupyterhub
RUN /srv/jupyterhub/bin/python -m pip install jupyterhub
RUN /srv/jupyterhub/bin/python -m pip install notebook

# Configuration files
ADD ./config-files/jupyterhub_config.py /etc/jupyterhub/jupyterhub_config.py
ADD ./config-files/entrypoint-startup.sh /home/jupyterhub/entrypoint-startup.sh

# adjust/clean format shell script file
RUN sudo sed -i -e 's/\r$//' /etc/jupyterhub/jupyterhub_config.py
RUN sudo sed -i -e 's/\r$//' /home/jupyterhub/entrypoint-startup.sh

# Adjust Permissions
RUN sudo chown -R jupyterhub:jupyterhub /home/jupyterhub
RUN sudo chmod +x /home/jupyterhub/entrypoint-startup.sh
RUN sudo chown -R root:jupyterhub /etc/jupyterhub/
RUN sudo chown -R root:jupyterhub /srv

# give permission to access credentials
#RUN sudo groupadd shadow
#RUN sudo chgrp shadow /etc/shadow
#RUN sudo chmod g+r /etc/shadow
#RUN sudo usermod -aG shadow jupyterhub

# Variáveis de ambiente
ENV PATH=$PATH
ENV PATH=$PATH:$JAVA_HOME:/opt/jdk/bin:/opt/jdk/sbin

# install other python libraries
RUN /srv/jupyterhub/bin/python -m pip install pyspark pandas numpy matplotlib scikit-learn statsmodels seaborn bokeh scrapy pysftp

# Muda o usuário
USER jupyterhub

# ~/.bashrc jupyterhub user
RUN export JAVA_HOME=/opt/jdk
RUN export PATH=$PATH:$JAVA_HOME:/opt/jdk/:/opt/jdk/bin
RUN echo "export JAVA_HOME=/opt/jdk" >> ~/.bashrc
RUN echo "export PATH=$PATH:/opt/jdk:/opt/jdk/bin" >> ~/.bashrc

# Pasta de trabalho
WORKDIR /home/jupyterhub

ENTRYPOINT ["/home/jupyterhub/entrypoint-startup.sh"]

EXPOSE 5858