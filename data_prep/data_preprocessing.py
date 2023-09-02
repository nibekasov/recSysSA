import findspark
findspark.init()
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType, LongType, StringType, DateType, FloatType
from pyspark.sql.window import Window

import time
import logging

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

from utils.utils import save_csv_to_path

spark = SparkSession \
    .builder \
    .config("spark.eventLog.gcMetrics.oldGenerationGarbageCollectors", "G1 Concurrent GC") \
    .config("spark.eventLog.gcMetrics.oldGenerationGarbageCollectors", "G1 Old Generation").getOrCreate()
sc = spark.sparkContext


# add parameter of path!
path = r"C:\Users\qwerty\Documents\GitHub\recSysSA\data\initial_data\ab_data.csv"
df = spark.read.options(header=True).csv(path)
logging.info("Initial data is loaded")


def remove_brackets(data, columns_brackets: list = ['price', 'quantity', 'item_id']):
    """
    removes brackets in columns' values given in columns_brackets
    """
    for column in columns_brackets:
        data = data.withColumn(column, F.regexp_replace(column, '[\\[\\]]', '').alias(column))
    return data


# df.show(1)
# df.show(3)

logging.info("Start of data preprocessing...")
df = df.withColumnRenamed("ecom.price100", "price")\
       .withColumnRenamed("ecom.qty", "quantity")\
       .withColumnRenamed("ecom.nm", "item_id")


df = df.sample(fraction=0.001, seed=21)
df = df.dropna()

# # remove brackets
df = remove_brackets(df)

# # check data types and add some basic features of date
df = df.withColumn("id", F.monotonically_increasing_id())   \
  .withColumn("platform" , df["platform"].cast(StringType()))   \
  .withColumn("utc_event_date" , F.col("utc_event_date").cast(DateType()))   \
  .withColumn("user_id" , df["user_id"].cast(StringType()))   \
  .withColumn("event_type" , df["event_type"].cast(StringType()))   \
  .withColumn("price", df["price"].cast(IntegerType()))    \
  .withColumn("quantity", df["quantity"].cast(IntegerType())) \
  .withColumn("item_id", df["item_id"].cast(StringType())) \
  .withColumn("timestamp_event_time", F.to_timestamp("utc_event_time", 'yyyy-MM-dd HH:mm:ssXXX'))    \
  .withColumn("year", F.year(F.to_timestamp("utc_event_date", 'yyyy-MM-dd')))    \
  .withColumn("month", F.month(F.to_timestamp("utc_event_date", 'yyyy-MM-dd')))    \
  .withColumn("day", F.dayofmonth(F.to_timestamp("utc_event_date", 'yyyy-MM-dd')))    \
  .withColumn("hour", F.hour(F.to_timestamp("utc_event_time", 'yyyy-MM-dd HH:mm:ssXXX')))    \


# # remove useless regular expression
df = df.withColumn("event_type",
  F.when(df.event_type.startswith("ec."), F.regexp_replace("event_type", "ec.", "")) \
   .otherwise(df.event_type))

# # start_time = time.time()

logging.info("Addidng time feature...")

# # time of one session = 30 min
lead_diff = 60 * 30
w_userid_time = Window.partitionBy("user_id").orderBy("timestamp_event_time")
w_userid_sessionid = Window.partitionBy("user_id", "session_id")

# calculate previous event for each user
df = df.withColumn("lag_event_timestamp", F.lag("timestamp_event_time", 1).over(w_userid_time))

# calculate if this event first in session
df = df.withColumn("is_first_event",
                   F.when((df.lag_event_timestamp.isNull()) | (
                               (df.timestamp_event_time - df.lag_event_timestamp).cast(LongType()) > lead_diff), 1)
                   .otherwise(0))

df = df.withColumn("timestamp_first_event",
                   F.when((df.is_first_event == 1), df.timestamp_event_time)
                   .otherwise(''))

# the session_id is common for all events in one session for each user
df = df.withColumn("session_id",
                   F.when((df.is_first_event == 1), df.id)
                   .otherwise(F.lag("id", 1).over(w_userid_time)))

# duration of session is difference between first and last events in one session
df = df.withColumn("session_duration",
                   ((F.max("timestamp_event_time").over(w_userid_sessionid)) - (
                       F.min("timestamp_event_time").over(w_userid_sessionid))).cast('long'))

# print(f'--- {time.time() - start_time :.2f} sec ---')
# print('Creating pandas dataframe...')
# # logging.info("Creating pandas dataframe...")
# pdf = df.toPandas()
# pdf.head(5)



# logging.info("Saving preprocessed data...")
# df.write.option("header",True) \
#  .csv(r"C:\Users\qwerty\Documents\GitHub\recSysSA\data\preprocessed_data\interactions.csv")
# logging.info("Data saved...")
