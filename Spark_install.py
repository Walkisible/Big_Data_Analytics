'''
Spark installation source code for google colab (.ipynb)

* Disclaimer: Spark is frequently update their version adn when the Spark is updated,
              some line cannot be executed.

              To fix this, change the Saprk version to the latest and try to run again

Tutorial: https://github.com/Walkisible/Big_Data_Analytics/blob/main/Spark_installation.ipynb
'''


# check for upgradable packages
!apt update

# install java
!apt-get install openjdk-11-jdk-headless -qq > /dev/null

!wget -q https://dlcdn.apache.org/spark/spark-3.4.0/spark-3.4.0-bin-hadoop3.tgz 

# unzip the spark file to the current folder
!tar -xf spark-3.4.0-bin-hadoop3.tgz

# to remove Spark.tgz file
!rm -rf spark-3.4.0-bin-hadoop3.tgz

# install findspark using pip
!pip install -q findspark
!pip install -q pyspark

# set your spark folder to your system path environment. 
import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64"
os.environ["SPARK_HOME"] = "/content/spark-3.4.0-bin-hadoop3"

# create SparkContext
from pyspark import SparkContext
import findspark

findspark.init()
sc = SparkContext.getOrCreate()
sc