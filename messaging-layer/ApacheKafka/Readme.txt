1- Baixe e descompacte o arquivo zip disponível ao final do capítulo.

2- Faça o download do Apache Hadoop e do JDK 8, coloque na pasta "binarios", descompacte os arquivos e renomeie as pastas. O procedimento é mostrado nas aulas.

3- Abra o terminal ou prompt de comando, navegue até a pasta do NameNode e execute a instrução abaixo para criar a imagem:

docker build . --file=Dockerfile -t apache_kafka:hadoop_cluster

# Documentação do docker build:
https://docs.docker.com/engine/reference/commandline/build/

3- Precisaremos de uma rede. Verifique as redes disponíveis e então crie uma com as instruções abaixo:

docker network ls
docker network create -d bridge dfs_net

4- Crie e inicialize o container com a instrução abaixo:

docker run -it -d --net dfs_net --ip 172.19.0.5 --hostname kafka --add-host=zookeeper_worker_01:172.19.0.2 --add-host=zookeeper_worker_02:172.19.0.3 --add-host=zookeeper_worker_03:172.19.0.4 --add-host=postgresql-db:172.19.0.6 --add-host=pgadmin:172.19.0.7 --add-host=flume_stream:172.19.0.8 --add-host=nifi:172.19.0.9 --add-host=hdpmaster:172.19.0.10 --add-host=datanode1:172.19.0.11 --add-host=datanode2:172.19.0.12 -p 19092:19092 -p 19093:19093 -p 19094:19094 --name apache_kafka apache_kafka:hadoop_cluster /bin/bash

# Documentação do doccker run:
https://docs.docker.com/engine/reference/commandline/run/

5 - para acessar o container recém criado:
docker container exec -it apache_kafka /bin/bash

6 - Laboratório simples com o kafka
# deletar um tópico
/opt/apache-kafka/bin/kafka-topics.sh --delete --topic topic01 --bootstrap-server kafka:9092,kafka:9093,kafka:9094

# Criando um tópico no Apache Kafka
/opt/apache-kafka/bin/kafka-topics.sh --create --topic topic01 --bootstrap-server kafka:9092,kafka:9093,kafka:9094 --replication-factor 3 --partitions 1
/opt/apache-kafka/bin/kafka-topics.sh --create --topic topic03 --bootstrap-server kafka:9092,kafka:9093,kafka:9094 --replication-factor 3 --partitions 3

# Listando os tópicos no Apache Kafka do broker 0 (rodando na porta 9092)
/opt/apache-kafka/bin/kafka-topics.sh --list --bootstrap-server kafka:9092,kafka:9093,kafka:9094

# Verificando informações do topic01 (particionamento, fator de replicação, Isnk = ordem de persistência das mensagens em disco)
# do broker 0 (rodando na porta 19092)
/opt/apache-kafka/bin/kafka-topics.sh --describe --topic topic01 --bootstrap-server kafka:9092,kafka:9093,kafka:9094

# Produzindo mensagens para o tópico no Apache Kafka
/opt/apache-kafka/bin/kafka-console-producer.sh --broker-list kafka:9092,kafka:9093,kafka:9094 --topic topic01

# após abrir o console, digite o conteúdo das mensagens e ao final de cada mensagem, clicar enter.

# Consumindo mensagens do tópico no Apache Kafka
/opt/apache-kafka/bin/kafka-console-consumer.sh --bootstrap-server kafka:9092,kafka:9093,kafka:9094 --topic topic01 --from-beginning

# verificando os logs do Apache Kafka
tail -f -n3000 /opt/apache-kafka/logs/server.log




