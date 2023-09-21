# REMOVE
# from pathlib import Path
import sys
import pandas as pd
import logging

sys.path.append('/opt/airflow/dags/scripts/')

from utils.utils import load_model
from models.lfm import LFMModel

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# REMOVE
# df = pd.read_parquet(r"airflow/dags/scripts/data\preprocessed_data\interactions.parquet", engine='pyarrow')
def train_lfm(data_path: str=None) -> None:
    """
    trains model for a given data with interactions
    :data_path: str, path to parquet with interactions
    """
    if data_path is None:
        logging.warning('Local data path is not set... Using default path')
        data = pd.read_parquet(r"airflow/dags/scripts/data\preprocessed_data\interactions.parquet", engine='pyarrow')
    else:
        logging.info(f'Reading data from local path: {data_path}')
        data = pd.read_parquet(data_path, engine='pyarrow')

    logging.info('Started training LightFM model...')
    lfm = LFMModel(is_infer=False) # train mode
    lfm.fit(
        data,
        user_col='user_id',
        item_col='item_id'
    )
    logging.info('Finished training LightFM model!')


# REMOVE
# p = r"C:\Users\qwerty\Documents\GitHub\recSysSoA\data\preprocessed_data\interactions_local_train.parquet"
# train_lfm(p)

# REMOVE
# data_for_train_ranker = prepare_data_for_train()
# print(data_for_train_ranker.head())



def train_ranker():
    """
    executes training pipeline for 2nd level model
    all params are stored in configs
    """

    X_train, X_test, y_train, y_test = prepare_data_for_train()
    ranker = Ranker(is_infer = False) # train mode
    ranker.fit(X_train, y_train, X_test, y_test)
    logging.info('Finished training Ranker model!')
#
# if __name__ == '__main__':
#     Fire(
#     {
#         'train_lfm': train_lfm,
#         'train_cbm': train_ranker
#         }
#     )