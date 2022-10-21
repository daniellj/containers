#!/usr/bin/env python
# coding: utf-8

# ### O.S. process

# In[1]:


import warnings
warnings.filterwarnings('ignore')

from os import environ

get_ipython().system('host=$(hostname)')
get_ipython().system("ip=$(ifconfig | grep 'inet ' | grep -v '127.0.0.1' | cut -c 7-17)")
get_ipython().system('echo "hostname: $(hostname)"')

# create path if not exists
#!mkdir -p ~/notebooks/data/

# download if not exists
#!wget -nc https://files.grouplens.org/datasets/movielens/ml-25m.zip -P ~/notebooks/data/

# unzip if not exists
#!unzip -n ~/notebooks/data/ml-25m.zip -d ~/notebooks/data/

#!ls -las /home/admin/notebooks/data/ml-25m

# check environment variables: JAVA_HOME
get_ipython().system('export JAVA_HOME=/opt/jdk')
environ["JAVA_HOME"] = "/opt/jdk"
get_ipython().system('echo "- JAVA_HOME:$JAVA_HOME"')

# check environment variables: PYSPARK_SUBMIT_ARGS
get_ipython().system('export PYSPARK_SUBMIT_ARGS=\'--packages io.delta:delta-core_2.12:2.1.0 --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" pyspark-shell\'')
environ["PYSPARK_SUBMIT_ARGS"]='--packages io.delta:delta-core_2.12:2.1.0 --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" pyspark-shell'
get_ipython().system('echo "- PYSPARK_SUBMIT_ARGS:$PYSPARK_SUBMIT_ARGS"')

# check environment variables: PATH
get_ipython().system('export PATH=$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/jdk:/opt/jdk/bin')
environ["PATH"] = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/jdk:/opt/jdk/bin"
get_ipython().system('echo "- PATH:$PATH"')

get_ipython().system('pip freeze')

# check java version
get_ipython().system('java -version')


# ### Function to reduce memory usage in Pandas DataFrame

# In[2]:


import numpy as np

def reduce_mem_usage(df):
    """ iterate through all the columns of a dataframe and modify the data type
        to reduce memory usage.
    """
    start_mem = df.memory_usage().sum() / 1024**2
    print('Memory usage of dataframe is {:.2f} MB'.format(start_mem))
    
    for col in df.columns:
        col_type = df[col].dtype
        
        if col_type != object:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)  
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
        else:
            df[col] = df[col].astype('category')

    end_mem = df.memory_usage().sum() / 1024**2
    print('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
    print('Decreased by {:.1f}%\n'.format(100 * (start_mem - end_mem) / start_mem))
    
    return df


# ### Connect from Apache Spark Cluster - without Delta Lake

# In[ ]:


#from os import environ
#environ["SPARK_HOME"] = '/opt/apache-spark'
#environ["PATH"] = '$PATH:/opt/jdk:/opt/jdk/bin:/opt/apache-spark:/opt/apache-spark/bin:/opt/apache-spark/sbin'

from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, DataFrameReader

#If you need to stop SparkContext (sc) or SparkSession
if 's_session' in locals():
    s_session.stop()
if 's_context' in locals():
    s_context.stop()

conf = SparkConf()

conf.setAppName("app_data_lake") \
.setMaster("spark://spark-master:7077") \
.setSparkHome("/opt/apache-spark")

s_context = SparkContext(conf=conf).getOrCreate()
s_session = SparkSession(sparkContext=s_context)
#builder = s_session.builder


# ### Read .CSV from SFTP and load into a Pandas DataFrame

# In[ ]:


import pysftp
from pandas import read_csv as pandas_read_csv
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType

# SFTP config connection
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
environ["FTP_HOST"] = 'sftp-01' # sftp-01 = 172.19.0.15
environ["FTP_PORT"] = '2222'
environ["FTP_USER"] = 'admin'
environ["FTP_PASS"] = 'admin'

# CSV schema
schema_doc = {
                "tags.csv": StructType([StructField("userId", IntegerType(), True),
                                     StructField("movieId", IntegerType(), True),
                                     StructField("tag", StringType(), True),
                                     StructField("timestamp", IntegerType(), True)]),
                "ratings.csv": StructType([StructField("userId", IntegerType(), True),
                                     StructField("movieId", IntegerType(), True),
                                     StructField("rating", FloatType(), True),
                                     StructField("timestamp", IntegerType(), True)])
                }

chunksize=500000
sftp_file="tags.csv" # 1.093.000 lines
#sftp_file="ratings.csv" # 25.000.000 lines

# open SFTP connection
with pysftp.Connection(environ["FTP_HOST"], port = int(environ["FTP_PORT"]), username = environ["FTP_USER"], password = environ["FTP_PASS"], cnopts=cnopts) as connection:
    print("Connection succesfully established…\n")
    # open the file
    with connection.open(remote_file = f"/data/{sftp_file}", mode='r') as file:

        i = 1
        for reader in pandas_read_csv(file, sep=',', chunksize=chunksize):
            chnk = "0 until " + str(chunksize) if i==1 else str(((chunksize * i) - chunksize) + 1) + " until " + str(chunksize * i)
            print(f"Chunksize block = line {chnk}")
            reader=reduce_mem_usage(df=reader)
            if i == 1:
                data = s_session.createDataFrame(data=reader, schema=schema_doc.get(sftp_file, sftp_file.split('.')[0]))
            else:
                new_data = s_session.createDataFrame(data=reader, schema=schema_doc.get(sftp_file, sftp_file.split('.')[0]))
                data = data.union(new_data)
                del new_data
            i = i + 1

connection.close()


# ### Resume of data

# In[ ]:


print( "- sparkSession: ", data.sparkSession, '\n' )
print("- Object: ", type(data), "\n")
print( "- schema: ", data.schema, '\n' )
print( "- printSchema: ", data.printSchema(), '\n' )
print( "- isStreaming: ", data.isStreaming, '\n' )
print( "- columns: ", data.columns, '\n' )
print( "- dtypes: ", data.dtypes, '\n' )
print( "- head: ", data.head(10), '\n' )
print( "- show: ", data.show(10), '\n' )
print( "- isEmpty: ", data.isEmpty(), '\n' )
print("- cache", data.cache(), '\n' ) # Persists the DataFrame with the default storage level (MEMORY_AND_DISK)
print( "- persist: ", data.persist(), '\n' ) # Sets the storage level to persist the contents of the DataFrame across operations after the first time it is computed.
print( "- storageLevel: ", data.storageLevel, '\n' )
print( "- count: ", data.count(), '\n' )
if sftp_file=="ratings.csv":
    print( "- correlation between rating and timestamp: ", data.corr("rating", "timestamp"), '\n' )
    print( "- covariance between rating and timestamp: ", data.cov("rating", "timestamp"), '\n' ) # Calculate the sample covariance for the given columns, specified by their names, as a double value
    print( "- descriptive statistics: ", data.describe(["userId", "movieId", "rating", "timestamp"]).show(), '\n' )
#print( "- summary: ", data.summary(), '\n' ) # Computes specified statistics for numeric and string columns


# ### Write DataFrame in HDFS

# In[ ]:


data.write.csv("hdfs://hdpmaster:9000/users/hduser/teste1.csv", header=True, mode="ignore")
data.write.parquet("hdfs://hdpmaster:9000/users/hduser/teste1.parquet", mode="ignore")


# ### Read data from HDFS

# In[ ]:


df_load_csv = s_session.read.csv("hdfs://hdpmaster:9000/users/hduser/teste1.csv", header='true', inferSchema='true')
df_load_parquet = s_session.read.parquet("hdfs://hdpmaster:9000/users/hduser/teste1.parquet")


# In[ ]:


print("CSV FILE:", "\n")
print( "- sparkSession: ", df_load_csv.sparkSession, '\n' )
print("- Object: ", type(df_load_csv), "\n")
print( "- schema: ", df_load_csv.schema, '\n' )
print( "- printSchema: ", df_load_csv.printSchema(), '\n' )
print( "- isStreaming: ", df_load_csv.isStreaming, '\n' )
print( "- columns: ", df_load_csv.columns, '\n' )
print( "- dtypes: ", df_load_csv.dtypes, '\n' )
print( "- head: ", df_load_csv.head(10), '\n' )
print( "- show: ", df_load_csv.show(10), '\n' )
print("##########################################################")
print("PARQUET FILE:", "\n")
print( "- sparkSession: ", df_load_parquet.sparkSession, '\n' )
print("- Object: ", type(df_load_parquet), "\n")
print( "- schema: ", df_load_parquet.schema, '\n' )
print( "- printSchema: ", df_load_parquet.printSchema(), '\n' )
print( "- isStreaming: ", df_load_parquet.isStreaming, '\n' )
print( "- columns: ", df_load_parquet.columns, '\n' )
print( "- dtypes: ", df_load_parquet.dtypes, '\n' )
print( "- head: ", df_load_parquet.head(10), '\n' )
print( "- show: ", df_load_parquet.show(10), '\n' )


# ### Create a temporary table

# In[ ]:


s_session.sql("CREATE TEMPORARY VIEW teste USING parquet OPTIONS (path \"hdfs://hdpmaster:9000/users/hduser/teste1.parquet\")")


# In[ ]:


s_session.sql("select * from teste limit 10").show(truncate=False)


# ### Connect from Apache Spark Cluster - with Delta Lake Session

# In[3]:


from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession

#If you need to stop SparkContext (sc) or SparkSession
if 's_session' in locals():
    s_session.stop()
if 's_context' in locals():
    s_context.stop()

#If you need to stop SparkContext (sc) or SparkSession
if 's_session_dl' in locals():
    s_session_dl.stop()
if 's_context_dl' in locals():
    s_context_dl.stop()

conf = SparkConf()

conf.setAppName("app_delta_lake") \
.setMaster("spark://spark-master:7077")
#.setSparkHome("/opt/apache-spark")
#.set("spark.jars.packages", "io.delta:delta-core_2.12:2.1.0")
#.set("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
#.set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \

s_context_dl = SparkContext(conf=conf).getOrCreate()
s_session_dl = SparkSession(sparkContext=s_context_dl)
builder = s_session_dl.builder \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")


from delta import configure_spark_with_delta_pip, DeltaTable

#my_packages = ["io.delta:delta-core_2.12:2.1.0"]
#s_session_delta = configure_spark_with_delta_pip(spark_session_builder=builder, extra_packages=my_packages).getOrCreate()

s_session_delta = configure_spark_with_delta_pip(spark_session_builder=builder).getOrCreate()


# In[4]:


from sys import version as sys_version

print('jupyter-hub python version:', sys_version)
print('context pyspark version:', s_context_dl.version)
print('context java spark version:', s_context_dl._jsc.version())
print(f'context hadoop version = {s_context_dl._jvm.org.apache.hadoop.util.VersionInfo.getVersion()}')


# ### Read .CSV from SFTP and load into a Pandas DataFrame - with Delta Lake Session

# In[5]:


import pysftp
from pandas import read_csv as pandas_read_csv
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, TimestampType
from pyspark.sql.functions import current_timestamp, date_format

# SFTP config connection
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
environ["FTP_HOST"] = 'sftp-01' # sftp-01 = 172.19.0.15
environ["FTP_PORT"] = '2222'
environ["FTP_USER"] = 'admin'
environ["FTP_PASS"] = 'admin'

# CSV schema
schema_doc = {
                "tags.csv": StructType([StructField("userId", IntegerType(), True),
                                     StructField("movieId", IntegerType(), True),
                                     StructField("tag", StringType(), True),
                                     StructField("timestamp", IntegerType(), True)]),
                "ratings.csv": StructType([StructField("userId", IntegerType(), True),
                                     StructField("movieId", IntegerType(), True),
                                     StructField("rating", FloatType(), True),
                                     StructField("timestamp", IntegerType(), True)])
                }

chunksize=500000
sftp_file="tags.csv" # 1.093.000 lines
#sftp_file="ratings.csv" # 25.000.000 lines

# open SFTP connection
with pysftp.Connection(environ["FTP_HOST"], port = int(environ["FTP_PORT"]), username = environ["FTP_USER"], password = environ["FTP_PASS"], cnopts=cnopts) as connection:
    print("Connection succesfully established…\n")
    # open the file
    with connection.open(remote_file = f"/data/{sftp_file}", mode='r') as file:

        i = 1
        for reader in pandas_read_csv(file, sep=',', chunksize=chunksize):
            chnk = "0 until " + str(chunksize) if i==1 else str(((chunksize * i) - chunksize) + 1) + " until " + str(chunksize * i)
            print(f"Chunksize block = line {chnk}")
            reader=reduce_mem_usage(df=reader)
            if i == 1:
                data_dl = s_session_delta.createDataFrame(data=reader, schema=schema_doc.get(sftp_file, sftp_file.split('.')[0]))
            else:
                new_data_dl = s_session_delta.createDataFrame(data=reader, schema=schema_doc.get(sftp_file, sftp_file.split('.')[0]))
                data_dl = data_dl.union(new_data_dl)
                del new_data_dl
            i = i + 1

connection.close()


# In[6]:


data_dl = data_dl.withColumn("created_datetime", current_timestamp())


# In[7]:


data_dl.show(10)


# In[8]:


print( "- count: ", data_dl.count())


# ### Create tables WITHOUT the metastore - Delta Lake

# In[43]:


s_session_delta.sql("CREATE SCHEMA IF NOT EXISTS bronze LOCATION 'hdfs://hdpmaster:9000/deltalake/bronze';")
s_session_delta.sql("CREATE SCHEMA IF NOT EXISTS silver LOCATION 'hdfs://hdpmaster:9000/deltalake/silver';")
s_session_delta.sql("CREATE SCHEMA IF NOT EXISTS gold LOCATION 'hdfs://hdpmaster:9000/deltalake/gold';")


# In[ ]:


s_session_delta.sql("""
CREATE TABLE IF NOT EXISTS bronze.tags (
      userId INT,
      movieId INT,
      tag STRING,
      timestamp INT
    ) USING DELTA
      LOCATION 'hdfs://hdpmaster:9000/deltalake/bronze/tags'
      COMMENT 'Table to store movie tags.';
    """)

#data_dl.createOrReplaceTempView("bronze.tags")

s_session_delta.sql("""
CREATE TABLE IF NOT EXISTS bronze.ratings (
      userId INT,
      movieId INT,
      rating FLOAT,
      timestamp INT
    ) USING DELTA
      LOCATION 'hdfs://hdpmaster:9000/deltalake/bronze/ratings'
      COMMENT 'Table to store movie ratings.';
    """)

#data_dl.createOrReplaceTempView("bronze.ratings")


# In[44]:


s_session_delta.sql("SHOW DATABASES;").show()


# In[45]:


s_session_delta.sql("SHOW SCHEMAS;").show()


# In[46]:


s_session_delta.sql("""DESCRIBE SCHEMA EXTENDED default""").head(20)


# In[47]:


s_session_delta.sql("""DESCRIBE SCHEMA EXTENDED bronze""").head(20)


# In[25]:


s_session_delta.sql("SHOW TABLES IN default;").show()


# In[32]:


s_session_delta.sql("SHOW TABLES IN bronze;").show()


# In[41]:


s_session_delta.sql("SHOW TABLE EXTENDED IN bronze like 'tags'").head(20)


# ### Create tables WITH the metastore - Delta Lake

# In[61]:


s_session_delta.sql("CREATE SCHEMA IF NOT EXISTS bronze LOCATION 'hdfs://hdpmaster:9000/deltalake/bronze';")
s_session_delta.sql("CREATE SCHEMA IF NOT EXISTS silver LOCATION 'hdfs://hdpmaster:9000/deltalake/silver';")
s_session_delta.sql("CREATE SCHEMA IF NOT EXISTS gold LOCATION 'hdfs://hdpmaster:9000/deltalake/gold';")


# In[62]:


s_session_delta.sql("""DESCRIBE SCHEMA EXTENDED bronze""").head(20)


# In[49]:


s_session_delta.sql("""DESCRIBE SCHEMA EXTENDED silver""").head(20)


# In[63]:


s_session_delta.sql("""DESCRIBE SCHEMA EXTENDED gold""").head(20)


# In[64]:


# https://learn.microsoft.com/en-us/azure/databricks/delta/table-properties
s_session_delta.conf.set("delta.autoOptimize.autoCompact", "true")
s_session_delta.conf.set("delta.autoOptimize.optimizeWrite", "true")


# In[65]:


# Create "bronze.tags" table in the metastore
DeltaTable.createIfNotExists(sparkSession=s_session_delta) \
  .tableName("bronze.tags") \
  .addColumn("userId", dataType=IntegerType(), nullable=True) \
  .addColumn("movieId", dataType=IntegerType(), nullable=True) \
  .addColumn("tag", dataType=StringType(), nullable=True, comment = "Movie genre.") \
  .addColumn("timestamp", dataType=IntegerType(), nullable=True) \
  .addColumn("created_datetime", dataType=TimestampType(), nullable=False) \
  .addColumn("created_date_year", dataType=IntegerType(), nullable=False, generatedAlwaysAs="YEAR(created_datetime)") \
  .addColumn("created_date_month", dataType=IntegerType(), nullable=False, generatedAlwaysAs="MONTH(created_datetime)") \
  .addColumn("created_date_day", dataType=IntegerType(), nullable=False, generatedAlwaysAs="DAY(created_datetime)") \
  .addColumn("modified_datetime", dataType=TimestampType(), nullable=True) \
  .comment("Table to store the genre for each movie.") \
  .property("description", "Table to store the genre for each movie.") \
  .location("hdfs://hdpmaster:9000/deltalake/bronze/tags") \
  .partitionedBy("created_date_year", "created_date_month") \
  .execute()


# In[66]:


# Create "bronze.ratings" table in the metastore
DeltaTable.createIfNotExists(sparkSession=s_session_delta) \
  .tableName("bronze.ratings") \
  .addColumn("userId", dataType=IntegerType(), nullable=True) \
  .addColumn("movieId", dataType=IntegerType(), nullable=True) \
  .addColumn("tag", dataType=StringType(), nullable=True, comment = "Movie genre.") \
  .addColumn("timestamp", dataType=IntegerType(), nullable=True) \
  .addColumn("created_datetime", dataType=TimestampType(), nullable=False) \
  .addColumn("created_date_year", dataType=IntegerType(), nullable=False, generatedAlwaysAs="YEAR(created_datetime)") \
  .addColumn("created_date_month", dataType=IntegerType(), nullable=False, generatedAlwaysAs="MONTH(created_datetime)") \
  .addColumn("created_date_day", dataType=IntegerType(), nullable=False, generatedAlwaysAs="DAY(created_datetime)") \
  .addColumn("modified_datetime", dataType=TimestampType(), nullable=True) \
  .comment("Movies classification ratings into a time series.") \
  .property("description", "Movies classification ratings into a time series.") \
  .location("hdfs://hdpmaster:9000/deltalake/bronze/ratings") \
  .partitionedBy("created_date_year", "created_date_month") \
  .execute()


# ### Write data in table - Delta Lake

# In[67]:


s_session_delta.sql("USE SCHEMA bronze;")
#ata_dl.write.format("delta").mode("append").save("hdfs://hdpmaster:9000/deltalake/bronze.tags")
data_dl.write.format("delta").mode("append").saveAsTable(name='bronze.tags')

# mode = append, overwrite, error, errorifexists, ignore


# ### Read data in table - Delta Lake

# In[83]:


s_session_delta.sql("SELECT * FROM bronze.tags ORDER BY userId LIMIT 15;").show(15)


# In[69]:


s_session_delta.sql("SELECT COUNT(*) FROM bronze.tags;").show()


# ### EXPLAIN statement is used to provide logical/physical plans

# In[17]:


s_session_delta.sql("EXPLAIN EXTENDED SELECT * FROM bronze.tags ORDER BY userId LIMIT 150;").head(200)


# In[18]:


s_session_delta.sql("EXPLAIN CODEGEN SELECT * FROM bronze.tags ORDER BY userId LIMIT 150;").head(200)


# In[19]:


s_session_delta.sql("EXPLAIN COST SELECT * FROM bronze.tags ORDER BY userId LIMIT 150;").head(200)


# In[20]:


s_session_delta.sql("EXPLAIN FORMATTED SELECT * FROM bronze.tags ORDER BY userId LIMIT 150;").head(200)


# ### Get information about Delta objects

# In[70]:


deltaTable_tags_by_path = DeltaTable.forPath(sparkSession=s_session_delta, path="hdfs://hdpmaster:9000/deltalake/bronze/tags")
deltaTable_tags_by_path.detail().head(10)


# In[71]:


s_session_delta.sql("DESCRIBE DETAIL 'hdfs://hdpmaster:9000/deltalake/bronze/tags'").head(10)


# In[72]:


deltaTable_tags_by_path.history().head(10)


# In[75]:


s_session_delta.sql("DESCRIBE HISTORY 'hdfs://hdpmaster:9000/deltalake/bronze/tags' LIMIT 10").head(10)


# In[76]:


deltaTable_tags_by_tablename = DeltaTable.forName(sparkSession=s_session_delta,tableOrViewName='bronze.tags')
deltaTable_tags_by_tablename.detail().head(10)


# In[77]:


s_session_delta.sql("DESCRIBE DETAIL bronze.tags").head(10)


# In[27]:


deltaTable_tags_by_tablename.history().head(10)


# In[78]:


s_session_delta.sql("DESCRIBE HISTORY bronze.tags").head(10)


# In[79]:


s_session_delta.sql("SHOW COLUMNS IN  bronze.tags").head(10)


# In[80]:


s_session_delta.sql("DESCRIBE TABLE bronze.tags").head(10)


# In[81]:


s_session_delta.sql("DESCRIBE TABLE EXTENDED bronze.tags").head(10)


# ### Optimize table

# In[82]:


deltaTable_tags_by_tablename.optimize().executeCompaction()


# In[41]:


#s_session_delta.sql("DROP TABLE IF EXISTS bronze.tags").head(10)

