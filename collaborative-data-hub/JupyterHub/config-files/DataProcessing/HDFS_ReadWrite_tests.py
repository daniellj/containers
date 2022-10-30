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

# In[4]:


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

# In[5]:


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
.setMaster("spark://spark-master:7077")
#.setSparkHome("/opt/apache-spark")

s_context = SparkContext(conf=conf).getOrCreate()
s_session = SparkSession(sparkContext=s_context)
#builder = s_session.builder


# ### Read .CSV from SFTP and load into a Pandas DataFrame

# In[6]:


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

# In[7]:


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
print( "- summary: ", data.summary().show(), '\n' ) # Computes specified statistics for numeric and string columns


# ### Write DataFrame in HDFS

# In[8]:


data.write.csv("hdfs://hdpmaster:9000/users/hduser/teste1.csv", header=True, mode="ignore")
data.write.parquet("hdfs://hdpmaster:9000/users/hduser/teste1.parquet", mode="ignore")


# ### Read data from HDFS

# In[9]:


df_load_csv = s_session.read.csv("hdfs://hdpmaster:9000/users/hduser/teste1.csv", header='true', inferSchema='true')
df_load_parquet = s_session.read.parquet("hdfs://hdpmaster:9000/users/hduser/teste1.parquet")


# In[10]:


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

# In[11]:


s_session.sql("CREATE TEMPORARY VIEW teste USING parquet OPTIONS (path \"hdfs://hdpmaster:9000/users/hduser/teste1.parquet\")")


# In[12]:


s_session.sql("select * from teste limit 10").show(truncate=False)

