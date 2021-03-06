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




print "7) Top 5 cities with the most avg arrival delays in minutes:"
arrivalDelayFlights = df_air_time.filter( (df_air_time.DEST.isNotNull()) & (df_air_time.ARR_DELAY.isNotNull()))
arrivalDelayFlightsgrpOrigin = arrivalDelayFlights.groupby('DEST').agg(avg(col("ARR_DELAY")).alias('avg')).orderBy('avg', ascending=False).limit(5)
df_airports=df_airports.filter(df_airports.city.isNotNull())
arrivalDelayFlightsgrpOriginjoined = arrivalDelayFlightsgrpOrigin.join(df_airports, arrivalDelayFlightsgrpOrigin.DEST == df_airports.iata)
print arrivalDelayFlightsgrpOriginjoined.select('city', 'avg').collect()










print("--- %s seconds ---" % (time.time() - start_time))