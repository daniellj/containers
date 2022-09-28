1- Abra o terminal ou prompt de comando, navegue até a pasta do PosgreSQL e execute a instrução abaixo para criar a imagem:

docker build . --file=Dockerfile -t postgresql:hadoop_cluster

# Documentação do docker build:
https://docs.docker.com/engine/reference/commandline/build/

3- Precisaremos de uma rede. Verifique as redes disponíveis e então crie uma com as instruções abaixo:

docker network ls
docker network create -d bridge dfs_net

4- Crie e inicialize o container com a instrução abaixo:

docker run -it -d --net dfs_net --hostname postgresql-db -p 5432:5432 --name postgresql postgresql:hadoop_cluster /bin/bash

# Documentação do doccker run:
https://docs.docker.com/engine/reference/commandline/run/

5 - para acessar o container recém criado:
docker container exec -it postgresql /bin/bash

6 - Ajuste de configurações + lab
sudo -u postgres psql

# change de password
\password

# create database objects
CREATE DATABASE datawarehouse;

\l

# connect on datawarehouse database
\c datawarehouse;

# create databae objects
CREATE TABLE sales(
   Id INT GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY NOT NULL,
   Product       CHAR(250)    NOT NULL,
   Price		 NUMERIC (18, 2),
   DateEvent 	 TIMESTAMP WITH TIME ZONE,
   CreatedDate 	 TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

# insert loop
do $$
declare
    id INTEGER :=1;
	max_id INTEGER :=1000;
begin
    WHILE id < max_id LOOP
    INSERT INTO sales(Product, Price, DateEvent) VALUES( randomValueFromList(ARRAY['Bathing suit,'Bathrobe,'Belt,'Beret,'Boots,'Bracelet','Brassiere','Briefcase','Cap','Coat','Dress','Earrings','Girdle','Glasses','Gloves','Hat','Jacket','Jeans','Mittens','Necklace','Nightgown','Overcoat','Panties','Pants','Pantyhose','Purse','Raincoat','Sandals','Scarf','Shirt','Shoes','Shorts','Skirt','Sneakers','Socks','Suit','Sweater','T-shirt','Tie','Umbrella','Underwear','Uniform','Wallet','Watch'])
														,randomNumber(20,200)::NUMERIC(18, 2)
														,(NOW::TIMESTAMP-(ROUND(randomNumber(1,365))||' DAYS')::INTERVAL)::TIMESTAMP
														);
				id := id+1;
    END LOOP;
END; $$;

# check data
SELECT * FROM sales;

# quit
\q