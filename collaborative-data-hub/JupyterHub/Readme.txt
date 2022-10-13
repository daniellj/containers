1- Abra o terminal ou prompt de comando, navegue até a pasta do Dockerfile:

docker build . --file=Dockerfile -t jupyterhub:hadoop_cluster

# Documentação do docker build:
https://docs.docker.com/engine/reference/commandline/build/

2- Precisaremos de uma rede. Verifique as redes disponíveis e então crie uma com as instruções abaixo:

docker network ls
docker network create dfs_net --subnet=172.19.0.0/16

3- Crie e inicialize o container com a instrução abaixo:

# run the image
docker run -it -d --net dfs_net --ip 172.19.0.100 --hostname jupyter-hub --add-host=spark-master:172.19.0.250 --add-host=spark-node1:172.19.0.251 --add-host=spark-node2:172.19.0.252 --add-host=zookeeper_worker_01:172.19.0.2 --add-host=zookeeper_worker_02:172.19.0.3 --add-host=zookeeper_worker_03:172.19.0.4 --add-host=postgresql-db:172.19.0.6 --add-host=pgadmin:172.19.0.7 --add-host=flume_stream:172.19.0.8 --add-host=nifi:172.19.0.9 --add-host=hdpmaster:172.19.0.10 --add-host=datanode1:172.19.0.11 --add-host=datanode2:172.19.0.12 -p 5858:5858 --name jupyter-hub jupyterhub:hadoop_cluster /bin/bash

# Documentação do doccker run:
https://docs.docker.com/engine/reference/commandline/run/

4- para acessar o container recém criado:
docker container exec -it jupyter-hub /bin/bash

# verifica logs de execução master node
tail -f -n500 