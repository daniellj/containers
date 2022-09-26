# Preparação do NameNode

1- Baixe e descompacte o arquivo zip disponível ao final do capítulo.

2- Faça o download do Apache Hadoop e do JDK 8, coloque na pasta "binarios", descompacte os arquivos e renomeie as pastas. O procedimento é mostrado nas aulas.

3- Abra o terminal ou prompt de comando, navegue até a pasta do NameNode e execute a instrução abaixo para criar a imagem:

docker build . --file=Dockerfile -t namenode:hadoop_cluster

# Documentação do docker build:
https://docs.docker.com/engine/reference/commandline/build/

3- Precisaremos de uma rede. Verifique as redes disponíveis e então crie uma com as instruções abaixo:

docker network ls
docker network create -d bridge dfs_net

4- Crie e inicialize o container com a instrução abaixo:

docker run -it -d --net dfs_net --hostname hdpmaster -p 9870:9870 -p 50030:50030 -p 8020:8020 -p 22:22 --name namenode namenode:hadoop_cluster /bin/bash

# Documentação do doccker run:
https://docs.docker.com/engine/reference/commandline/run/

5- Acesse o container usando a CLI no Docker Desktop e execute as instruções abaixo:
5.1 - para acessar o(s) container(s) recém criado(s):
docker container exec -it hdpmaster /bin/bash

# Para o serviço do hadoop:
hdfs --daemon stop namenode

# Formate o NameNode (SOMENTE NA PRIMEIRA EXECUÇÃO)
hdfs namenode -format

# Inicializar o serviço do hadoop
hdfs --daemon start namenode

# verifica estado do processo
jps

# cria o usuario de serviço
sudo useradd nifi

# cria estrutura de pastas
hdfs dfs -mkdir /users

hdfs dfs -mkdir /users/hduser/
hdfs dfs -mkdir /users/hduser/files/
hdfs dfs -mkdir /users/hduser/files/sandbox/

hdfs dfs -mkdir /users/nifi/
hdfs dfs -mkdir /users/nifi/files
hdfs dfs -mkdir /users/nifi/files/iot
hdfs dfs -mkdir /users/nifi/files/streaming
hdfs dfs -mkdir /users/nifi/files/sandbox

# ajusta as permissões
hdfs dfs -chown -R hduser:supergroup /
hdfs dfs -chmod -R 755 /

hdfs dfs -chown -R hduser:supergroup /users/hduser/
#hdfs dfs -chmod -R 750 /users/hduser/
hdfs dfs -chmod -R 755 /users/hduser/
hdfs dfs -chown -R nifi:supergroup /users/nifi/
#hdfs dfs -chmod -R 770 /users/nifi/
hdfs dfs -chmod -R 775 /users/nifi/

# verifica se estrutura foi criada
hdfs dfs -ls /users
hdfs dfs -ls /users/hduser
hdfs dfs -ls /users/nifi

# enviando um arquivo para o hadoop para testar a replicação (antes é necessário ter o cluster inicializado!)
mkdir /home/hduser/data
cd /home/hduser/data
wget https://files.grouplens.org/datasets/movielens/ml-25m.zip
hdfs dfs -put /home/hduser/data/ml-25m.zip /users/hduser/files/sandbox/
hdfs dfs -ls /users/hduser/files/sandbox
rm -rf /home/hduser/data/ml-25m.zip

# Acesse o painel de gestão pelo navegador
127.0.0.1:9870