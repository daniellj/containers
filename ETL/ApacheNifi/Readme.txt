1- Baixe e descompacte o arquivo zip disponível ao final do capítulo.

2- Faça o download do Apache Hadoop e do JDK 8, coloque na pasta "binarios", descompacte os arquivos e renomeie as pastas. O procedimento é mostrado nas aulas.

3- Abra o terminal ou prompt de comando, navegue até a pasta do NameNode e execute a instrução abaixo para criar a imagem:

docker build . --file=Dockerfile -t apache_nifi:hadoop_cluster

# Documentação do docker build:
https://docs.docker.com/engine/reference/commandline/build/

3- Precisaremos de uma rede. Verifique as redes disponíveis e então crie uma com as instruções abaixo:

docker network ls
docker network create -d bridge dfs_net

4- Crie e inicialize o container com a instrução abaixo:

docker run -it -d --net dfs_net --hostname nifi -p 59595:59595 --name apache_nifi apache_nifi:hadoop_cluster /bin/bash

ou usar a imagem pronta:

docker run --name nifi -p 59595:59595 -d -e SINGLE_USER_CREDENTIALS_USERNAME=admin -e SINGLE_USER_CREDENTIALS_PASSWORD=rHkWR1gDNW3R9hgbeRsT3OM3Ue0zwGtQqcFKJD2EXWE -e NIFI_WEB_HTTPS_PORT='59595' apache/nifi:latest

# Documentação do doccker run:
https://docs.docker.com/engine/reference/commandline/run/

5 - Acesse o container usando a CLI no Docker Desktop e execute as instruções abaixo:
5.1 - para acessar o(s) container(s) recém criado(s):
docker container exec -it nifi /bin/bash

6 - Caso necessite inicializar o agente do Apache Nifi, rodar o comando abaixo:
/opt/apache-nifi/bin/nifi.sh start

# Verificar se serviço subiu
/opt/apache-nifi/bin/nifi.sh status

# verifica se a porta está listening
netstat -vant|grep LISTEN|grep 59595

# verifica os logs
tail -f -n 300 /opt/apache-nifi/logs/nifi-app.log

7 - set user and password
/opt/apache-nifi/bin/nifi.sh set-single-user-credentials admin rHkWR1gDNW3R9hgbeRsT3OM3Ue0zwGtQqcFKJD2EXWE

8 - Para acessar a interface do Nifi:
https://127.0.0.1:59595/nifi

Username = 349e74a3-d8ac-4582-887d-0f2a62008c8e
Password = KIt9FBQoY37roRs/dsQLyvBhGdcIlLc/

9 - Configurar um processor consumindo o protocolo MQTT com o broker http://www.hivemq.com/demos/websocket-client/ para inserir no hdfs
Conecte-se no cluster hadoop e faça os comandos abaixo:

#hdfs dfs -copyToLocal "/path/file_name" "OS_destination_path"
hdfs dfs -copyToLocal /users/nifi/files/iot/c1c82561-636e-4386-9b1f-93ee59a603ae /home/hduser/data
vim /home/hduser/data/c1c82561-636e-4386-9b1f-93ee59a603ae
