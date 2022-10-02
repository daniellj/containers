1- Baixe e descompacte o arquivo zip disponível ao final do capítulo.

2- Faça o download do Apache Hadoop e do JDK 8, coloque na pasta "binarios", descompacte os arquivos e renomeie as pastas. O procedimento é mostrado nas aulas.

3- Abra o terminal ou prompt de comando, navegue até a pasta do NameNode e execute a instrução abaixo para criar a imagem:

docker build . --file=DockerfileCluster1 -t apache_zookeeper_cluster1:hadoop_cluster
docker build . --file=DockerfileCluster2 -t apache_zookeeper_cluster2:hadoop_cluster
docker build . --file=DockerfileCluster3 -t apache_zookeeper_cluster3:hadoop_cluster

# Documentação do docker build:
https://docs.docker.com/engine/reference/commandline/build/

3- Precisaremos de uma rede. Verifique as redes disponíveis e então crie uma com as instruções abaixo:

docker network ls
docker network create -d bridge dfs_net

4- Crie e inicialize o container com a instrução abaixo:

docker run -it -d --net dfs_net --ip 172.19.0.2 --hostname zookeeper_worker_01 --add-host=zookeeper_worker_02:172.19.0.3 --add-host=zookeeper_worker_03:172.19.0.4 --add-host=kafka:172.19.0.5 --add-host=postgresql-db:172.19.0.6 --add-host=pgadmin:172.19.0.7 --add-host=flume_stream:172.19.0.8 --add-host=nifi:172.19.0.9 --add-host=hdpmaster:172.19.0.10 --add-host=datanode1:172.19.0.11 --add-host=datanode2:172.19.0.12 --name zookeeper_worker_01 apache_zookeeper_cluster1:hadoop_cluster /bin/bash

docker run -it -d --net dfs_net --ip 172.19.0.3 --hostname zookeeper_worker_02 --add-host=zookeeper_worker_01:172.19.0.2 --add-host=zookeeper_worker_03:172.19.0.4 --add-host=kafka:172.19.0.5 --add-host=postgresql-db:172.19.0.6 --add-host=pgadmin:172.19.0.7 --add-host=flume_stream:172.19.0.8 --add-host=nifi:172.19.0.9 --add-host=hdpmaster:172.19.0.10 --add-host=datanode1:172.19.0.11 --add-host=datanode2:172.19.0.12 --name zookeeper_worker_02 apache_zookeeper_cluster2:hadoop_cluster /bin/bash

docker run -it -d --net dfs_net --ip 172.19.0.4 --hostname zookeeper_worker_03 --add-host=zookeeper_worker_01:172.19.0.2 --add-host=zookeeper_worker_02:172.19.0.3 --add-host=kafka:172.19.0.5 --add-host=postgresql-db:172.19.0.6 --add-host=pgadmin:172.19.0.7 --add-host=flume_stream:172.19.0.8 --add-host=nifi:172.19.0.9 --add-host=hdpmaster:172.19.0.10 --add-host=datanode1:172.19.0.11 --add-host=datanode2:172.19.0.12 --name zookeeper_worker_03 apache_zookeeper_cluster3:hadoop_cluster /bin/bash

# Documentação do doccker run:
https://docs.docker.com/engine/reference/commandline/run/

5 - Acesse o container usando a CLI no Docker Desktop e execute as instruções abaixo:
5.1 - para acessar o(s) container(s) recém criado(s):
docker container exec -it zookeeper_worker_01 /bin/bash
docker container exec -it zookeeper_worker_02 /bin/bash
docker container exec -it zookeeper_worker_03 /bin/bash

6 - Em cada um dos nodos, avalie os logs de execução
worker_01:
tail -f -n300 /opt/apache-zookeeper/logs/zookeeper--server-zookeeper_worker_01.out
tail -f -n300 /opt/apache-zookeeper/logs/zookeeper_audit.log

worker_02:
tail -f -n300 /opt/apache-zookeeper/logs/zookeeper--server-zookeeper_worker_02.out
tail -f -n300 /opt/apache-zookeeper/logs/zookeeper_audit.log

worker_03:
tail -f -n300 /opt/apache-zookeeper/logs/zookeeper--server-zookeeper_worker_03.out
tail -f -n300 /opt/apache-zookeeper/logs/zookeeper_audit.log

7 - Testando a comunicação. Apartir do cliente dos nodos 2 ou 3, vamos acessar o nodo 1
/opt/apache-zookeeper/bin/zkCli.sh -server zookeeper_worker_01:2181

# criando um znode zk_znode_1 associand a string sample_data:
create /zk_znode_1 sample_data

# Listar os nodos criados
ls /

# buscar os dados associados ao zk_znode_1
get /zk_znode_1