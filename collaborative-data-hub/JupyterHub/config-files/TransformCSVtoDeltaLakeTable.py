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
get_ipython().system('echo "JAVA_HOME:$JAVA_HOME"')

# check environment variables: PATH
get_ipython().system('export PATH=$PATH:/opt/jdk:/opt/jdk/bin')
environ["PATH"] = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/jdk:/opt/jdk/bin"
get_ipython().system('echo "PATH:$PATH"')

get_ipython().system('pip freeze')

# check java version
get_ipython().system('java -version')


# ### Connect from Apache Spark Cluster

# In[2]:


#from os import environ
#environ["SPARK_HOME"] = '/opt/apache-spark'
#environ["PATH"] = '$PATH:/opt/jdk:/opt/jdk/bin:/opt/apache-spark:/opt/apache-spark/bin:/opt/apache-spark/sbin'

from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, DataFrameReader
from delta import *

#If you need to stop SparkContext (sc) or SparkSession
if 's_session' in locals():
    s_session.stop()
if 's_context' in locals():
    s_context.stop()

conf = SparkConf()

conf.setAppName("app1") \
.setMaster("spark://spark-master:7077") \
.setSparkHome("/opt/apache-spark")
#.set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
#.set("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
#.set("spark.jars.packages", "io.delta:delta-core_2.12:2.1.0")

s_context = SparkContext(conf=conf).getOrCreate()
s_session = SparkSession(sparkContext=s_context)
builder = s_session.builder
#.config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
#.config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

#my_packages = ["io.delta:delta-core_2.12:2.1.0"]
#s_session_delta = configure_spark_with_delta_pip(spark_session_builder=builder, extra_packages=my_packages).getOrCreate()

#s_session_delta = configure_spark_with_delta_pip(spark_session_builder=builder).getOrCreate()


# In[ ]:





# In[3]:


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


# ### Read .CSV from SFTP and load into a Pandas DataFrame

# In[5]:


environ["FTP_HOST"] = 'sftp-01' # sftp-01 = 172.19.0.15
environ["FTP_PORT"] = '2222'
environ["FTP_USER"] = 'admin'
environ["FTP_PASS"] = 'admin'

import pysftp
from pandas import read_csv as pandas_read_csv
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

#dfreader = DataFrameReader(spark = s_session)


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
#sftp_file="tags.csv"
sftp_file="ratings.csv"

with pysftp.Connection(environ["FTP_HOST"], port = int(environ["FTP_PORT"]), username = environ["FTP_USER"], password = environ["FTP_PASS"], cnopts=cnopts) as connection:
    print("Connection succesfully established…\n")
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
                #data.append(other=new_data)
                data = data.union(new_data)
                del new_data
            i = i + 1
            #data = dfreader.csv(path=file.readlines(), sep =',')

connection.close()


# In[11]:


#data.show(10)

data


# ### Convert Pandas to PySpark (Spark) DataFrame

# In[ ]:


#Create PySpark DataFrame from Pandas

from pyspark.sql.types import StructType, StructField, LongType, StringType

schema = StructType(
                    [
                        StructField("movieId", LongType(), True, metadata = {'description': 'The movie unique identifier.'}),
                        StructField("title", StringType(), True, metadata = {'description': 'The movie title.'}),
                        StructField("genres", StringType(), True, metadata = {'description': 'The movie genre.'})
                    ]
                    )

sparkDF=spark.createDataFrame(data = data)
sparkDF.printSchema()


# In[ ]:


schema.json()


# In[ ]:


sparkDF.show(15)


# ### Transform a Delta Lake

# In[ ]:


sparkDF.write.format("delta").save("/tmp/movies")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




