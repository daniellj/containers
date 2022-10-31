CREATE SCHEMA IF NOT EXISTS bronze COMMENT 'Bronze tables have raw data ingested from various sources.' LOCATION 'hdfs://hdpmaster:9000/deltalake/bronze';
CREATE SCHEMA IF NOT EXISTS silver COMMENT 'Silver tables have a more refined view of the data.' LOCATION 'hdfs://hdpmaster:9000/deltalake/silver';
CREATE SCHEMA IF NOT EXISTS gold COMMENT 'Gold tables give business-level aggregates often used for dashboarding and reporting.' LOCATION 'hdfs://hdpmaster:9000/deltalake/gold';

SHOW SCHEMAS;

USE bronze;

CREATE EXTERNAL TABLE IF NOT EXISTS bronze.tags (
      userId INT,
      movieId INT,
      tag STRING,
      timestamp_event INT,
	  created_datetime TIMESTAMP,
	  created_date_year INT COMMENT 'The DEFAULT value must be = YEAR(created_datetime)',
	  created_date_month INT COMMENT 'The DEFAULT value must be = MONTH(created_datetime)',
	  created_date_day INT COMMENT 'The DEFAULT value must be = DAY(created_datetime)',
	  modified_datetime TIMESTAMP
    ) COMMENT 'Table to store the genre for each movie'
	  STORED BY 'io.delta.hive.DeltaStorageHandler'
	  LOCATION 'hdfs://hdpmaster:9000/deltalake/bronze/tags';

SELECT * from bronze.tags LIMIT 10;

CREATE EXTERNAL TABLE IF NOT EXISTS bronze.ratings (
      userId INT,
      movieId INT,
      rating FLOAT,
      timestamp_event INT,
	  created_datetime TIMESTAMP,
	  created_date_year INT COMMENT 'The DEFAULT value must be = YEAR(created_datetime)',
	  created_date_month INT COMMENT 'The DEFAULT value must be = MONTH(created_datetime)',
	  created_date_day INT COMMENT 'The DEFAULT value must be = DAY(created_datetime)',
	  modified_datetime TIMESTAMP
    ) COMMENT 'Movies classification ratings into a time series'
	  STORED BY 'io.delta.hive.DeltaStorageHandler'
	  LOCATION 'hdfs://hdpmaster:9000/deltalake/bronze/ratings';

SELECT * from bronze.ratings LIMIT 10;

SHOW TABLES;