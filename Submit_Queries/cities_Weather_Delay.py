from pyspark import SparkContext
from pyspark.sql import Row
from pyspark.sql import functions as F
from pyspark import SQLContext
from pyspark.sql.functions import *
from pyspark.sql.functions import col, avg, max
from pyspark.sql.functions import udf
import sys
import time


# SQL context. can also be replaced with SparkContext but we get RDD instaed of dataframes
sc = SparkContext()
sqlContext = SQLContext(sc)

start_time = time.time()
#DF creation for all the airtime csv file
df_air_time = sqlContext.read.format(source="com.databricks.spark.csv").options(header='true', inferschema='true').load(sys.argv[1])

#DF creation for airport
df_airports = sqlContext.read.format(source="com.databricks.spark.csv").options(header='true', inferschema='true').load(sys.argv[2])

#DF creation for carrier
df_carrier = sqlContext.read.format(source="com.databricks.spark.csv").options(header='true', inferschema='true').load(sys.argv[3])
# print count




print "2) Cities having Weather delay"
 
 
AirportsWeatherflightdelay = df_air_time.filter((df_air_time.SECURITY_DELAY > 100))
 
print "Airports having Weather delay"
statesNASdelay = AirportsWeatherflightdelay.groupby('ORIGIN_AIRPORT_ID').count().orderBy('count', ascending=False).limit(5)
top20outflightsgrpjoined = statesNASdelay.join(df_airports, statesNASdelay.ORIGIN_AIRPORT_ID == df_airports.iata)
print top20outflightsgrpjoined.select('City').show()

print("--- %s seconds ---" % (time.time() - start_time))

