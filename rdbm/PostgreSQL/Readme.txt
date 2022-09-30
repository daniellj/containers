1 - Precisaremos de uma rede. Verifique as redes disponíveis e então crie uma com as instruções abaixo:

docker network ls
docker network create -d bridge dfs_net

3 - Usar a imagem pronta do postgre

docker pull postgres
docker run --net dfs_net --hostname postgresql-db --name postgresql -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=1234 -p 5432:5432 postgres -d /bin/bash

4 - Instalar o pgadmin
docker pull dpage/pgadmin4:latest
docker run -it -d --net dfs_net --hostname pgadmin --name pgadmin -p 6500:80 -e 'PGADMIN_DEFAULT_EMAIL=seu_email@dominio.com' -e 'PGADMIN_DEFAULT_PASSWORD=1234' -e 'PGADMIN_LISTEN_PORT=80' -d dpage/pgadmin4 /bin/bash

5 - Após, acessar no navegador de internet o seguinte endereço:

URL: 127.0.0.1:6500
Login: seu_email@dominio.com
Password: 1244

6 - Criação de objetos de banco de dados
-- create database objects
DO $$ 
DECLARE
   database_name VARCHAR(50) := 'datawarehouse';
BEGIN 
   IF EXISTS (SELECT FROM pg_database WHERE datname = database_name) THEN
      RAISE NOTICE 'Database % already exists', database_name;
   ELSE
      PERFORM dblink_exec('dbname=' || current_database(), concat('CREATE DATABASE ', database_name));
   END IF;
END $$;

CREATE SCHEMA IF NOT EXISTS dw AUTHORIZATION admin;

CREATE TABLE IF NOT EXISTS dw.sales(
   Id INT GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY NOT NULL,
   Product       CHAR(250)    NOT NULL,
   Price		 NUMERIC (18, 2),
   DateEvent 	 TIMESTAMP WITH TIME ZONE,
   CreatedDate 	 TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dw.control_data_flow(
   Id INT NOT NULL,
   schema_name       CHAR(250)    NOT NULL,
   table_name        CHAR(250)    NOT NULL,
   modifieddate TIMESTAMP WITH TIME ZONE NULL,
   CreatedDate 	 TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE FUNCTION update_modifieddate_on_dw_control_data_flow()
RETURNS TRIGGER AS $$
BEGIN
    NEW.modifieddate = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_ModifiedDate
    BEFORE UPDATE
    ON
        dw.control_data_flow
    FOR EACH ROW
EXECUTE PROCEDURE update_modifieddate_on_dw_control_data_flow();

-- insert loop
CREATE OR REPLACE FUNCTION random_between(low INT ,high INT) 
   RETURNS INT AS
$$
BEGIN
   RETURN floor(random()* (high-low + 1) + low);
END;
$$ language 'plpgsql' STRICT;


CREATE OR REPLACE FUNCTION random_pick(qty_elements INT)
  RETURNS CHAR(250) AS
$$
BEGIN
   RETURN ('{Bathing suit,Bathrobe,Belt,Beret,Boots,Bracelet,Brassiere,Briefcase,Cap,Coat,Dress,Earrings,Girdle,Glasses,Gloves,Hat,Jacket,Jeans,Mittens,Necklace,Nightgown,Overcoat,Panties,Pants,Pantyhose,Purse,Raincoat,Sandals,Scarf,Shirt,Shoes,Shorts,Skirt,Sneakers,Socks,Suit,Sweater,T-shirt,Tie,Umbrella,Underwear,Uniform,Wallet,Watch}'::text[])[ceil(random()*qty_elements)];
END
$$ LANGUAGE 'plpgsql' VOLATILE;

7 - Inserir alguns registros
do $$
declare
    id INTEGER :=1;
	max_id INTEGER :=1000;
begin
    WHILE id < max_id LOOP
    INSERT INTO dw.sales(Product, Price, DateEvent) VALUES(
														 random_pick(44)
														,random_between(20,200)::NUMERIC(18, 2)
														,(NOW()::TIMESTAMP-(ROUND(random_between(10,8760))||' HOURS')::INTERVAL)::TIMESTAMP
														);
				id := id+1;
    END LOOP;
END; $$;

insert into dw.control_data_flow (Id, schema_name, table_name) values (0, 'dw', 'sales');

-- check data
SELECT * FROM dw.sales order by id desc limit 1000;

select * from dw.control_data_flow WHERE schema_name = 'dw' and table_name = 'sales' ORDER BY Id DESC LIMIT 1;