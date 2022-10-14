#!/usr/bin/env python
# coding: utf-8

# ### O.S. process

# In[1]:


from os import environ

# create path if not exists
get_ipython().system('mkdir -p ~/notebooks/data/')

# download if not exists
#!wget -nc https://files.grouplens.org/datasets/movielens/ml-25m.zip -P ~/notebooks/data/

# unzip if not exists
#!unzip -n ~/notebooks/data/ml-25m.zip -d ~/notebooks/data/

get_ipython().system('ls -las /home/admin/notebooks/data/ml-25m')

# check environment variables: JAVA_HOME
get_ipython().system('export JAVA_HOME=/opt/jdk')
environ["JAVA_HOME"] = "/opt/jdk"
get_ipython().system('echo $JAVA_HOME')

# check environment variables: PATH
get_ipython().system('export PATH=$PATH:/opt/jdk:/opt/jdk/bin')
environ["PATH"] = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/jdk:/opt/jdk/bin"
get_ipython().system('echo $PATH')

# check java version
get_ipython().system('java -version')


# ### Read .CSV from SFTP and load into a Pandas DataFrame

# In[2]:


environ["FTP_HOST"] = 'sftp-01' # sftp-01 = 172.19.0.15
environ["FTP_PORT"] = '2222'
environ["FTP_USER"] = 'admin'
environ["FTP_PASS"] = 'admin'

import pysftp
from pandas import read_csv as pandas_read_csv

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

with pysftp.Connection(environ["FTP_HOST"], port = int(environ["FTP_PORT"]), username = environ["FTP_USER"], password = environ["FTP_PASS"], cnopts=cnopts) as sftp:
    print("Connection succesfully established…")
    with sftp.open(remote_file = "/data/movies.csv", mode='r') as file:
        data = pandas_read_csv(file)


# ### Connect from Apache Spark Cluster

# In[ ]:


'''
from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .master("spark://spark-master:7077") \
    .appName("ToDeltaLake") \
    .getOrCreate()
'''
#environ["SPARK_HOME"] = '/opt/apache-spark'
#environ["PATH"] = '$PATH:/opt/jdk:/opt/jdk/bin:/opt/apache-spark:/opt/apache-spark/bin:/opt/apache-spark/sbin'

from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from os import environ
from delta import *

conf = (
    SparkConf()
    #.setAppName("app1") \
    #.setMaster("spark://spark-master:7077")
)

sc = SparkContext(conf=conf).getOrCreate()
spark = SparkSession(sc).builder \
        .appName("app1") \
        .master("spark://spark-master:7077") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .getOrCreate()

#.config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \


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




