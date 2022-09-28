1- Baixe e descompacte o arquivo zip disponível ao final do capítulo.

2- Faça o download do Apache Hadoop e do JDK 8, coloque na pasta "binarios", descompacte os arquivos e renomeie as pastas. O procedimento é mostrado nas aulas.

3- Abra o terminal ou prompt de comando, navegue até a pasta do NameNode e execute a instrução abaixo para criar a imagem:

docker build . --file=Dockerfile -t apache_flume:hadoop_cluster

# Documentação do docker build:
https://docs.docker.com/engine/reference/commandline/build/

3- Precisaremos de uma rede. Verifique as redes disponíveis e então crie uma com as instruções abaixo:

docker network ls
docker network create -d bridge dfs_net

4- Crie e inicialize o container com a instrução abaixo:

docker run -it -d --net dfs_net --hostname flume_stream --name apache_flume apache_flume:hadoop_cluster /bin/bash

# Documentação do doccker run:
https://docs.docker.com/engine/reference/commandline/run/

5 - Acesse o container usando a CLI no Docker Desktop e execute as instruções abaixo:
5.1 - para acessar o(s) container(s) recém criado(s):
docker container exec -it nifi /bin/bash

6 - Certifique-se que a estrututa de pastas /users/hduser/twitter_data/ exista no hdfs:

No namenode, execute o comando para verificar a estrutura de pastas:
hdfs dfs -ls /users/hduser/twitter_data/

Caso não exista, vá criando uma por uma, até chegar no nível de "twitter_data":
hdfs dfs -mkdir /users/hduser/twitter_data/

7 - Caso necessite inicializar o agente do Apache Flume, rodar o comando abaixo:
#sudo /opt/apache-flume/bin/flume-ng agent --conf /opt/apache-flume/conf/ -f /opt/apache-flume/conf/twitter.conf -Dflume.root.logger=DEBUG,console -n TwitterAgent

tail -f /home/flume/nohup.out -n 150