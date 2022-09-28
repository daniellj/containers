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

docker run -it -d --net dfs_net --hostname kafka -p 9092:9092 -p 9093:9093 -p 9094:9094 --name apache_kafka apache_kafka:hadoop_cluster /bin/bash

# Documentação do doccker run:
https://docs.docker.com/engine/reference/commandline/run/

5 - para acessar o container recém criado:
docker container exec -it apache_kafka /bin/bash

6 - Laboratório simples com o kafka
# deletar um tópico
/opt/apache-kafka/bin/kafka-topics.sh --delete --topic topic01 --bootstrap-server kafka:9092

# Criando um tópico no Apache Kafka
/opt/apache-kafka/bin/kafka-topics.sh --create --topic topic01 --bootstrap-server kafka:9092 --replication-factor 3 --partitions 1
/opt/apache-kafka/bin/kafka-topics.sh --create --topic topic03 --bootstrap-server kafka:9093 --replication-factor 3 --partitions 3

# Listando os tópicos no Apache Kafka do broker 0 (rodando na porta 9092)
/opt/apache-kafka/bin/kafka-topics.sh --list --bootstrap-server kafka:9092

# Verificando informações do topic01 (particionamento, fator de replicação, Isnk = ordem de persistência das mensagens em disco)
# do broker 0 (rodando na porta 9092)
/opt/apache-kafka/bin/kafka-topics.sh --describe --topic topic01 --bootstrap-server kafka:9092
/opt/apache-kafka/bin/kafka-topics.sh --describe --topic topic03 --bootstrap-server kafka:9092

# Produzindo mensagens para o tópico no Apache Kafka
/opt/apache-kafka/bin/kafka-console-producer.sh --broker-list kafka:9092 --topic topic01

# após abrir o console, digite o conteúdo das mensagens e ao final de cada mensagem, clicar enter.

# Consumindo mensagens do tópico no Apache Kafka
/opt/apache-kafka/bin/kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic topic01 --from-beginning

# verificando os logs do Apache Kafka
tail -f -n3000 /opt/apache-kafka/logs/server.log