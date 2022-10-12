2- Faça o download do Apache Hadoop e do JDK 8, coloque na pasta "binarios", descompacte os arquivos e renomeie as pastas. O procedimento é mostrado nas aulas.

3- Abra o terminal ou prompt de comando, navegue até a pasta do NameNode e execute a instrução abaixo para criar a imagem:

docker build . --file=DockerfileMaster -t spark_master:hadoop_cluster
docker build . --file=DockerfileWorkers -t spark_worker:hadoop_cluster

# Documentação do docker build:
https://docs.docker.com/engine/reference/commandline/build/

3- Precisaremos de uma rede. Verifique as redes disponíveis e então crie uma com as instruções abaixo:

docker network ls
docker network create dfs_net --subnet=172.19.0.0/16

4- Crie e inicialize o container com a instrução abaixo:

# run master node
docker run -it -d --net dfs_net --ip 172.19.0.250 --hostname spark-master --add-host=spark-node1:172.19.0.251 --add-host=spark-node2:172.19.0.252 --add-host=zookeeper_worker_01:172.19.0.2 --add-host=zookeeper_worker_02:172.19.0.3 --add-host=zookeeper_worker_03:172.19.0.4 --add-host=postgresql-db:172.19.0.6 --add-host=pgadmin:172.19.0.7 --add-host=flume_stream:172.19.0.8 --add-host=nifi:172.19.0.9 --add-host=hdpmaster:172.19.0.10 --add-host=datanode1:172.19.0.11 --add-host=datanode2:172.19.0.12 -p 4040:4040 -p 8080:8080 -p 7077:7077 --name spark-master spark_master:hadoop_cluster /bin/bash

docker run -it -d --net dfs_net --ip 172.19.0.251 --hostname spark-node1 --add-host=spark-master:172.19.0.250 --add-host=spark-node2:172.19.0.252 --add-host=zookeeper_worker_01:172.19.0.2 --add-host=zookeeper_worker_02:172.19.0.3 --add-host=zookeeper_worker_03:172.19.0.4 --add-host=postgresql-db:172.19.0.6 --add-host=pgadmin:172.19.0.7 --add-host=flume_stream:172.19.0.8 --add-host=nifi:172.19.0.9 --add-host=hdpmaster:172.19.0.10 --add-host=datanode1:172.19.0.11 --add-host=datanode2:172.19.0.12 --name spark-node1 spark_worker:hadoop_cluster /bin/bash

docker run -it -d --net dfs_net --ip 172.19.0.252 --hostname spark-node2 --add-host=spark-master:172.19.0.250 --add-host=spark-node1:172.19.0.251 --add-host=zookeeper_worker_01:172.19.0.2 --add-host=zookeeper_worker_02:172.19.0.3 --add-host=zookeeper_worker_03:172.19.0.4 --add-host=postgresql-db:172.19.0.6 --add-host=pgadmin:172.19.0.7 --add-host=flume_stream:172.19.0.8 --add-host=nifi:172.19.0.9 --add-host=hdpmaster:172.19.0.10 --add-host=datanode1:172.19.0.11 --add-host=datanode2:172.19.0.12 --name spark-node2 spark_worker:hadoop_cluster /bin/bash

# Documentação do doccker run:
https://docs.docker.com/engine/reference/commandline/run/

5 - para acessar o container recém criado:

# master node
docker container exec -it spark-master /bin/bash

# verifica logs de execução master node
tail -f -n500 /opt/apache-spark/logs/spark--org.apache.spark.deploy.master.Master-1-spark-master.out

# worker 1 node
docker container exec -it spark-node1 /bin/bash

# verifica logs de execução worker node 1
tail -f -n500 /opt/apache-spark/logs/spark-spark-org.apache.spark.deploy.worker.Worker-1-spark-node1.out

# worker 2 node
docker container exec -it spark-node2 /bin/bash

# verifica logs de execução worker node 1
tail -f -n500 /opt/apache-spark/logs/spark-spark-org.apache.spark.deploy.worker.Worker-1-spark-node2.out