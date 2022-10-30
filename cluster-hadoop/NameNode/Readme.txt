# Preparação do NameNode

1- Faça o download do Apache Hadoop e do JDK 8, coloque na pasta "binarios", descompacte os arquivos e renomeie as pastas.

2- Abra o terminal ou prompt de comando, navegue até a pasta do NameNode e execute a instrução abaixo para criar a imagem:

docker build . --file=Dockerfile -t namenode:hadoop_cluster

# Documentação do docker build:
https://docs.docker.com/engine/reference/commandline/build/

3- Precisaremos de uma rede. Verifique se há a rede "dfs_net" disponível, senão crie.

# verificar redes disponíveis
docker network ls

# criar a rede
docker network create -d bridge dfs_net --subnet=172.19.0.0/16

4- Crie e inicialize o container com a instrução abaixo:

docker run -it -d --net dfs_net --ip 172.19.0.10 --hostname hdpmaster --add-host=zookeeper_worker_01:172.19.0.2 --add-host=zookeeper_worker_02:172.19.0.3 --add-host=zookeeper_worker_03:172.19.0.4 --add-host=kafka:172.19.0.5 --add-host=postgresql-db:172.19.0.6 --add-host=pgadmin:172.19.0.7 --add-host=flume_stream:172.19.0.8 --add-host=nifi:172.19.0.9 --add-host=datanode1:172.19.0.11 --add-host=datanode2:172.19.0.12 -p 9870:9870 -p 50030:50030 -p 8020:8020 --name namenode namenode:hadoop_cluster /bin/bash

# Documentação do doccker run:
https://docs.docker.com/engine/reference/commandline/run/

5- Acesse o container usando qualquer terminar do seu S.O. e execute as instruções abaixo:
5.1 - para acessar o(s) container(s) recém criado(s):
docker container exec -it namenode /bin/bash

# Para o serviço do hadoop:
hdfs --daemon stop namenode

# Formate o NameNode (SOMENTE NA PRIMEIRA EXECUÇÃO)
hdfs namenode -format

# Inicializar o serviço do hadoop
hdfs --daemon start namenode

# verifica estado do processo
jps

# cria estrutura de pastas
hdfs dfs -mkdir /users

hdfs dfs -mkdir /users/hduser/
hdfs dfs -mkdir /users/hduser/files/
hdfs dfs -mkdir /users/hduser/files/sandbox/

# ajusta as permissões
hdfs dfs -chown -R hduser:supergroup /
hdfs dfs -chmod -R 755 /

hdfs dfs -chown -R hduser:supergroup /users/hduser/
#hdfs dfs -chmod -R 750 /users/hduser/
hdfs dfs -chmod -R 755 /users/hduser/

# verifica se estrutura foi criada
hdfs dfs -ls /users
hdfs dfs -ls /users/hduser

# enviando um arquivo para o hadoop para testar a replicação (antes é necessário ter o cluster inicializado!)
mkdir /home/hduser/data
cd /home/hduser/data
wget https://files.grouplens.org/datasets/movielens/ml-25m.zip
hdfs dfs -put /home/hduser/data/ml-25m.zip /users/hduser/files/sandbox/
hdfs dfs -ls /users/hduser/files/sandbox
rm -rf /home/hduser/data/ml-25m.zip

# Acesse o painel de gestão pelo navegador
127.0.0.1:9870