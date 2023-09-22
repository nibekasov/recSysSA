import pandas as pd
import datetime as dt
import logging

from configs.config import settings
from utils.utils import read_parquet, rm_parquet, save_parquet

def split_train_test() -> None:
    logging.info(f"Loading data for split...")

    interactions = read_parquet(
        file_folder=settings.DATA_FOLDERS.PREPROCESSED_DATA_FOLDER,
        file_name=settings.DATA_FILES_P.INTERACTIONS_FILE
    )

    # set dates params for filter
    max_date = pd.to_datetime(interactions['timestamp_event_time'].max())
    min_date = pd.to_datetime(interactions['timestamp_event_time'].min())
    test_interval_days = settings.SPLIT_PAR.TEST_INTERVAL_DAYS


    test_max_date = max_date - dt.timedelta(days=test_interval_days)
    logging.info(f"test max date = {test_max_date}")


    global_train = interactions.loc[pd.to_datetime(interactions['timestamp_event_time']) < test_max_date]
    global_test = interactions.loc[pd.to_datetime(interactions['timestamp_event_time']) >= test_max_date]
    logging.info(f"Global test shape = {global_test.shape}")


    local_train_thresh = pd.to_datetime(global_train['timestamp_event_time'].quantile(q=.7, interpolation='nearest'))

    local_train = global_train[pd.to_datetime(global_train['timestamp_event_time']) < local_train_thresh]
    local_test = global_train[pd.to_datetime(global_train['timestamp_event_time']) >= local_train_thresh]

    local_test = local_test.loc[local_test['user_id'].isin(local_train['user_id'].unique())]
    logging.info(f"Local test shape = {global_test.shape}")

    logging.info("Saving splitted data...")

    folder = settings.DATA_FOLDERS.SPLITTED_DATA_FOLDER
    try:
        rm_parquet(file_folder=folder, file_name=settings.DATA_SPLIT_P.INTERACTIONS_LOCAL_TEST)
        rm_parquet(file_folder=folder, file_name=settings.DATA_SPLIT_P.INTERACTIONS_LOCAL_TRAIN)
        rm_parquet(file_folder=folder, file_name=settings.DATA_SPLIT_P.INTERACTIONS_GLOBAL_TEST)
    except OSError:
        save_parquet(data=local_train, file_folder=folder, file_name=settings.DATA_SPLIT_P.INTERACTIONS_LOCAL_TRAIN)
        save_parquet(data=local_test, file_folder=folder, file_name=settings.DATA_SPLIT_P.INTERACTIONS_LOCAL_TEST)
        save_parquet(data=global_test, file_folder=folder, file_name=settings.DATA_SPLIT_P.INTERACTIONS_GLOBAL_TEST)

    logging.info("Split is performed!")




