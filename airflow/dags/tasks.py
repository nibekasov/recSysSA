from scripts.data_prep.prepare_split import split_train_test
from scripts.data_prep.train import train_lfm
import os

def SPLIT():
    data_path = f'{os.path.abspath(os.path.dirname(__file__))}/scripts/data/preprocessed_data/interactions.parquet'
    split_train_test(data_path)

def TRAIN():
    data_path = f'{os.path.abspath(os.path.dirname(__file__))}/scripts/data/preprocessed_data/interactions_local_train.parquet'
    train_lfm(data_path)

