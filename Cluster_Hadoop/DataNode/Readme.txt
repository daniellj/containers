# Preparação dos DataNodes

1- Baixe e descompacte o arquivo zip disponível ao final do capítulo.

2- Faça o download do Apache Hadoop e do JDK 8, coloque na pasta "binarios", descompacte os arquivos e renomeie as pastas. O procedimento é mostrado nas aulas e é o mesmo usado no capítulo anterior.

3- Abra o terminal ou prompt de comando, navegue até a pasta do DataNode e execute a instrução abaixo para criar a imagem:

docker build . --file=Dockerfile -t datanode:hadoop_cluster

# Documentação do docker build:
https://docs.docker.com/engine/reference/commandline/build/

3- Precisaremos de uma rede. Verifique se a rede dfs_net criada no capítulo anterior está criada:

docker network ls

4- Crie e inicialize o container de cada datanode (criaremos 2) com cada instrução abaixo:

docker run -it -d --net dfs_net --hostname datanode1 --name datanode1 datanode:hadoop_cluster /bin/bash
docker run -it -d --net dfs_net --hostname datanode2 --name datanode2 datanode:hadoop_cluster /bin/bash

# Documentação do doccker run:
https://docs.docker.com/engine/reference/commandline/run/

5- Acesse CADA container usando a CLI no Docker Desktop e execute as instruções abaixo:
5.1 - para acessar o(s) container(s) recém criado(s):
docker container exec -it datanode1 /bin/bash
docker container exec -it datanode2 /bin/bash

# Copie a chave que está em /home/hduser/.ssh/authorized_keys no NameNode para o mesmo arquivo em cada datanode.
# no namenode, executar:
cat /home/hduser/.ssh/authorized_keys

# nos dois datanodes, executar os passos à seguir substituindo o conteúdo entre aspas duplas pela saída do comando anterior (cat /home/hduser/.ssh/authorized_keys):
echo "ssh-rsa XXXXXXXXXXXXXXXXXXXXXXXXXX" > /home/hduser/.ssh/authorized_keys

# conferir o conteúdo
cat /home/hduser/.ssh/authorized_keys

# reinicializa o serviço SSH
sudo service ssh restart

# Parar o serviço do hadoop:
hdfs --daemon stop datanode

# Formata DataNode
hdfs datanode -format

# Inicializar o serviço do hadoop:
hdfs --daemon start datanode

# Verifica status do cluster
jps

# Acesse o namenode e insira um arquivo no cluster