import pandas as pd
import datetime as dt
import logging
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
import os

def split_train_test(data_path) -> None:
    logging.info(f"Loading data for split...")

    interactions = pd.read_parquet(data_path)
    # set dates params for filter
    MAX_DATE = pd.to_datetime(interactions['timestamp_event_time'].max())
    MIN_DATE = pd.to_datetime(interactions['timestamp_event_time'].min())
    TEST_INTERVAL_DAYS = 7


    TEST_MAX_DATE = MAX_DATE - dt.timedelta(days=TEST_INTERVAL_DAYS)
    logging.info(f"test max date = {TEST_MAX_DATE}")


    global_train = interactions.loc[pd.to_datetime(interactions['timestamp_event_time']) < TEST_MAX_DATE]
    global_test = interactions.loc[pd.to_datetime(interactions['timestamp_event_time']) >= TEST_MAX_DATE]
    logging.info(f"Global test shape = {global_test.shape}")


    local_train_thresh = pd.to_datetime(global_train['timestamp_event_time'].quantile(q=.7, interpolation='nearest'))

    local_train = global_train[pd.to_datetime(global_train['timestamp_event_time']) < local_train_thresh]
    local_test = global_train[pd.to_datetime(global_train['timestamp_event_time']) >= local_train_thresh]

    local_test = local_test.loc[local_test['user_id'].isin(local_train['user_id'].unique())]
    logging.info(f"Localt test shape = {global_test.shape}")

    logging.info("Saving splitted data...")

    try:
        os.remove(data_path + r"\interactions_local_train.parquet")
        os.remove(data_path + r"\interactions_local_test.parquet")
        os.remove(data_path + r"\interactions_global_test.parquet")
    except OSError:
        local_train.to_parquet(data_path + r"\interactions_local_train.parquet")
        local_test.to_parquet(data_path + r"\interactions_local_test.parquet")
        global_test.to_parquet(data_path + r"\interactions_global_test.parquet")

    logging.info("Split is performed!")





