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
def create_spark_session() -> None:
    spark = SparkSession \
        .builder \
        .config("spark.eventLog.gcMetrics.oldGenerationGarbageCollectors", "G1 Concurrent GC") \
        .config("spark.eventLog.gcMetrics.oldGenerationGarbageCollectors", "G1 Old Generation") \
        .getOrCreate()
    sc = spark.sparkContext
    return spark

def load_csv_from_path():
    # add parameter of path!
    spark = create_spark_session()
    path = r"C:\Users\qwerty\Documents\GitHub\recSysSA\data\initial_data\ab_data.csv"
    data = spark.read.options(header=True).csv(path)
    # logging.info("Initial data is loaded")
    return data

# logging.info("Start of data preprocessing...")

def rename_columns(data):
    """
    ADD!
    """
    data = data.withColumnRenamed("ecom.price100", "price")\
           .withColumnRenamed("ecom.qty", "quantity")\
           .withColumnRenamed("ecom.nm", "item_id")
    return data

def sampling(data, fraction=0.001, seed=21):
    """
    ADD!
    """
    data = data.sample(fraction=fraction, seed=seed)
    return data


def remove_brackets(data, columns_brackets: list = ['price', 'quantity', 'item_id']):
    """
    removes brackets in columns' values given in columns_brackets
    """
    for column in columns_brackets:
        data = data.withColumn(column, F.regexp_replace(column, '[\\[\\]]', '').alias(column))
    return data

def drop_nan_values(data):
    """
    ADD!
    """
    data = data.dropna()
    return data


def check_data_types(data):
    """
    check data types and add some basic features of date
    """
    data = data.withColumn("id", F.monotonically_increasing_id()) \
        .withColumn("platform", data["platform"].cast(StringType())) \
        .withColumn("utc_event_date", F.col("utc_event_date").cast(DateType())) \
        .withColumn("user_id", data["user_id"].cast(StringType())) \
        .withColumn("event_type", data["event_type"].cast(StringType())) \
        .withColumn("price", data["price"].cast(IntegerType())) \
        .withColumn("quantity", data["quantity"].cast(IntegerType())) \
        .withColumn("item_id", data["item_id"].cast(StringType())) \
        .withColumn("timestamp_event_time", F.to_timestamp("utc_event_time", 'yyyy-MM-dd HH:mm:ssXXX')) \
        .withColumn("year", F.year(F.to_timestamp("utc_event_date", 'yyyy-MM-dd'))) \
        .withColumn("month", F.month(F.to_timestamp("utc_event_date", 'yyyy-MM-dd'))) \
        .withColumn("day", F.dayofmonth(F.to_timestamp("utc_event_date", 'yyyy-MM-dd'))) \
        .withColumn("hour", F.hour(F.to_timestamp("utc_event_time", 'yyyy-MM-dd HH:mm:ssXXX'))) \

    return data

def remove_reg_event(data):
    """
    remove useless regular expression
    """
    data = data.withColumn("event_type",
      F.when(data.event_type.startswith("ec."), F.regexp_replace("event_type", "ec.", "")) \
       .otherwise(data.event_type))
    return data


def add_session_feature(data, session_dur_min=30):
    """
    ADD!
    """
    lead_diff = session_dur_min * 60
    w_userid_time = Window.partitionBy("user_id").orderBy("timestamp_event_time")
    w_userid_sessionid = Window.partitionBy("user_id", "session_id")

    # calculate previous event for each user
    data = data.withColumn("lag_event_timestamp", F.lag("timestamp_event_time", 1).over(w_userid_time))

    # calculate if this event first in session
    data = data.withColumn("is_first_event",
                       F.when((data.lag_event_timestamp.isNull()) | (
                               (data.timestamp_event_time - data.lag_event_timestamp).cast(LongType()) > lead_diff), 1)
                       .otherwise(0))

    data = data.withColumn("timestamp_first_event",
                       F.when((data.is_first_event == 1), data.timestamp_event_time)
                       .otherwise(''))

    # the session_id is common for all events in one session for each user
    data = data.withColumn("session_id",
                       F.when((data.is_first_event == 1), data.id)
                       .otherwise(F.lag("id", 1).over(w_userid_time)))

    # duration of session is difference between first and last events in one session
    data = data.withColumn("session_duration",
                       ((F.max("timestamp_event_time").over(w_userid_sessionid)) - (
                           F.min("timestamp_event_time").over(w_userid_sessionid))).cast('long'))

    return data


# ---garbage---
#
# print("Saving preprocessed data...")
# df.write.option("header",True).mode("overwrite") \
#  .parquet(r"interactions.parquet")
# print("Data saved!")
# # df.write.parquet("output/proto.parquet")
#
# # print("Data saved!")
#
# path = r"C:\Users\qwerty\Documents\GitHub\recSysSoA\data_prep\interactions.csv"
# df_check = spark.read.options(header=True).csv(path)
# df_check.show(1)