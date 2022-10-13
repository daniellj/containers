### Get data + S.O. process

# create path if not exists
!mkdir -p ~/notebooks/data/

# download if not exists
!wget -nc https://files.grouplens.org/datasets/movielens/ml-25m.zip -P ~/notebooks/data/

# unzip if not exists
!unzip -n ~/notebooks/data/ml-25m.zip -d ~/notebooks/data/

# check environment variables: JAVA_HOME
!export JAVA_HOME=/opt/jdk
!echo $JAVA_HOME

# check environment variables: PATH
!export PATH=$PATH:/opt/jdk:/opt/jdk/bin
!echo $PATH

# check java version
!java -version

### Connect a Apache Spark Cluster

from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .master("spark://spark-master:7077") \
    .appName("ToDeltaLake") \
    .getOrCreate()

### Read a .CSV
df = spark.read.option("header", "true").csv.(~/notebooks/data/ml-25m/ratings.csv)
df.show(10)

### Transform a Delta Lake