# Preparação do Apache Hive

1- Faça o download do Apache Hive e do JDK 8, coloque na pasta "binarios", descompacte os arquivos e renomeie as pastas.

2- Abra o terminal ou prompt de comando, navegue até a pasta do apache-hive e execute a instrução abaixo para criar a imagem:

docker build . --file=Dockerfile -t apache-hive:hadoop_cluster

# Documentação do docker build:
https://docs.docker.com/engine/reference/commandline/build/

3- Precisaremos de uma rede. Verifique se há a rede "dfs_net" disponível, senão crie.

# verificar redes disponíveis
docker network ls

# criar a rede
docker network create -d bridge dfs_net --subnet=172.19.0.0/16

4- Crie e inicialize o container com a instrução abaixo:

docker run -it -d --net dfs_net --ip 172.19.0.19 --hostname metastore-hive --add-host=zookeeper_worker_01:172.19.0.2 --add-host=zookeeper_worker_02:172.19.0.3 --add-host=zookeeper_worker_03:172.19.0.4 --add-host=kafka:172.19.0.5 --add-host=postgresql-db:172.19.0.6 --add-host=pgadmin:172.19.0.7 --add-host=flume_stream:172.19.0.8 --add-host=nifi:172.19.0.9 --add-host=datanode1:172.19.0.11 --add-host=datanode2:172.19.0.12 -p 3306:3306 -p 9083:9083 -p 10000:10000 -p 10001:10001 -p 10002:10002 --name metastore-hive apache-hive:hadoop_cluster /bin/bash

# Documentação do doccker run:
https://docs.docker.com/engine/reference/commandline/run/

5- Acesse o container usando qualquer terminar do seu S.O. e execute as instruções abaixo:
5.1 - para acessar o(s) container(s) recém criado(s):
docker container exec -it metastore-hive /bin/bash

6- Verificar serviços:
Hiserver:
tail -f -n300 /home/hive/hiveserver2.log

- Metastore:
tail -f -n300 /home/hive/metastore.log

6- Conectar na interface web do Apache Hive # 9083 -> metadata server | 10000 -> hiveserver2 TCP | 10001 -> hiveserver2 HTTP | 10002 -> hiveserver2 Web Interface
http://127.0.0.1:10002/
