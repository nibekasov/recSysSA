import logging
from fire import Fire

from configs.config import settings
from utils.utils import read_parquet

from models.lfm import LFMModel
from models.ranker import Ranker
from data_prep.prepare_ranker_data import prepare_data_for_train, get_ranker_sample

def train_lfm(data_path: str = None) -> None:
    """
    trains model for a given data with interactions
    :data_path: str, path to parquet with interactions
    """
    logging.info(f'Reading data from path...')
    data = read_parquet(

        file_folder=settings.DATA_FOLDERS.SPLITTED_DATA_FOLDER,
        # file_name=settings.DATA_FILES_P.INTERACTIONS_FILE
        file_name=settings.DATA_SPLIT_P.INTERACTIONS_LOCAL_TRAIN
    )

    logging.info('Started training LightFM model...')
    lfm = LFMModel(is_infer=False)  # train mode
    lfm.fit(
        data,
        user_col=settings.FEATURES.USER_IDS,
        item_col=settings.FEATURES.ITEM_IDS
    )
    logging.info('Finished training LightFM model!')

# REMOVE AFTER TESTING
# p = r"C:\Users\qwerty\Documents\GitHub\recSysSoA\data\preprocessed_data\interactions_local_train.parquet"
# train_lfm(p)


# data_for_train_ranker = prepare_data_for_train()
# print(data_for_train_ranker.head())


def train_ranker():
    """
    executes training pipeline for 2nd level model
    all params are stored in configs
    """
    # test_preds = prepare_data_for_train()
    X_train, X_test, y_train, y_test = prepare_data_for_train()
    ranker = Ranker(is_infer=False)  # train mode
    ranker.fit(X_train, y_train, X_test, y_test)
    logging.info('Finished training Ranker model!')

# REMOVE AFTER TESTING
# test_preds = prepare_data_for_train()
# X_train, X_test, y_train, y_test = get_ranker_sample(test_preds)
# print(y_test.head())


# if __name__ == '__main__':
#     Fire(
#     {
#         'train_lfm': train_lfm,
        # 'train_cbm': train_ranker
        # }
    # )

# train_lfm()
# train_ranker()
