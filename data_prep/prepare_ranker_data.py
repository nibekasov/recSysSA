import logging
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

from configs.config import settings
from utils.utils import (
    generate_lightfm_recs_mapper,
    load_model,
)


import logging
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def prepare_data_for_train():
    """
    function to prepare data to train catboost classifier.
    Basically, you have to wrap up code from full_recsys_pipeline.ipynb
    where we prepare data for classifier. In the end, it should work such
    that we trigger and use fit() method from ranker.py

        paths_config: dict, where key is path name and value is the path to data
    """
    # load model artefacts
    # model = load_model(settings.LFM_TRAIN_PARAMS.MODEL_PATH)
    model = load_model(r"C:\Users\qwerty\Documents\GitHub\recSysSoA\artefacts\lfm_model.dill")
    dataset = load_model(r"C:\Users\qwerty\Documents\GitHub\recSysSoA\artefacts\lfm_mapper.dill")
    # dataset = load_model(settings.LFM_TRAIN_PARAMS.MAPPER_PATH)

    # get users sample to predict candidates on
    # user_sample_path = settings.RANKER_DATA.USERS_SAMPLE
    # if "https" in user_sample_path:
    #     users_sample = read_parquet_from_gdrive(user_sample_path)
    # else:
    local_test = pd.read_parquet(r"C:\Users\qwerty\Documents\GitHub\recSysSoA\data\preprocessed_data\interactions_local_test.parquet")

    # pred candidates
    test_preds = pd.DataFrame({
        'user_id': local_test['user_id'].unique()})

    # preds = users_sample[["user_id"]].drop_duplicates().reset_index(drop=True)

    # init mapper with model
    item_ids = list(dataset.mapping()[2].values())
    item_inv_mapper = {v: k for k, v in dataset.mapping()[2].items()}
    mapper = generate_lightfm_recs_mapper(
        model,
        item_ids=item_ids,
        known_items=dict(),
        N=settings.LFM_PREDS_PARAMS.TOP_K,
        user_features=None,
        item_features=None,
        user_mapping=dataset.mapping()[0],
        item_inv_mapping=item_inv_mapper,
        num_threads=20,
    )
    test_preds['item_id'] = test_preds['user_id'].map(mapper)

    # define target & prepare ranker sample
    test_preds = test_preds.explode('item_id')

    logging.info(f"Shape of the preds: {test_preds.shape}")

    test_preds['rank'] = test_preds.groupby('user_id').cumcount() + 1
    logging.info(
        f"Number of unique candidates generated by the LFM: {test_preds.item_id.nunique()}"
    )

    # ------ ADDDDDD --------
    # train_data = get_ranker_sample(preds=test_preds, users_sample=users_sample)

    # return train_data
    return test_preds

def get_ranker_sample(test_preds: pd.DataFrame):
    """
    final step to use candidates generation and users interaction to define
    train data - join features, define target, split into train & test samples
    """
    # local_test = users_sample.copy(deep=True)
    local_test = pd.read_parquet(r"C:\Users\qwerty\Documents\GitHub\recSysSoA\data\preprocessed_data\interactions_local_test.parquet")

    # prepare train & test
    positive_preds = pd.merge(test_preds, local_test, how='inner', on=['user_id', 'item_id'])
    positive_preds['target'] = 1
    logging.info(f"Shape of the positive target preds: {positive_preds.shape}")

    negative_preds = pd.merge(local_test, test_preds, how='left', on=['user_id', 'item_id'])
    negative_preds = negative_preds.loc[negative_preds['event_type'] != 'purchase'].sample(frac=.05)
    negative_preds['target'] = 0
    logging.info(f"Shape of the negative target preds: {positive_preds.shape}")

    # random split to train ranker
    train_users, test_users = train_test_split(
        local_test['user_id'].unique(),
        test_size=.2,
        random_state=13
    )

    cbm_train_set = shuffle(
        pd.concat(
            [positive_preds.loc[positive_preds['user_id'].isin(train_users)],
             negative_preds.loc[negative_preds['user_id'].isin(train_users)]]
        )
    )

    cbm_test_set = shuffle(
        pd.concat(
            [
                positive_preds.loc[positive_preds["user_id"].isin(test_users)],
                negative_preds.loc[negative_preds["user_id"].isin(test_users)],
            ]
        )
    )

    # users_data = read_parquet_from_gdrive(settings.RANKER_DATA.USERS_DATA_PATH)
    # items_data = read_parquet_from_gdrive(settings.RANKER_DATA.MOVIES_DATA_PATH)

    # join user features
    # cbm_train_set = pd.merge(
    #     cbm_train_set,
    #     users_data[["user_id"] + settings.USER_FEATURES],
    #     how="left",
    #     on=["user_id"],
    # )
    # cbm_test_set = pd.merge(
    #     cbm_test_set,
    #     users_data[["user_id"] + settings.USER_FEATURES],
    #     how="left",
    #     on=["user_id"],
    # )
    # # join item features
    # cbm_train_set = pd.merge(
    #     cbm_train_set,
    #     items_data[["item_id"] + settings.ITEM_FEATURES],
    #     how="left",
    #     on=["item_id"],
    # )
    # cbm_test_set = pd.merge(
    #     cbm_test_set,
    #     items_data[["item_id"] + settings.ITEM_FEATURES],
    #     how="left",
    #     on=["item_id"],
    # )

    # final steps
    ID_COLS = ['user_id', 'item_id']
    TARGET = ['target']
    CATEGORICAL_COLS = ['platform', 'event_type']
    DROP_COLS = ['utc_event_time', 'utc_event_date', 'id', 'year', 'month', 'day',
                 'timestamp_event_time', 'lag_event_timestamp', 'is_first_event', 'timestamp_first_event', 'session_id',
                 'session_duration']

    drop_cols = (
        ID_COLS +
        DROP_COLS +
        TARGET
    )
    X_train, y_train = (
        cbm_train_set.drop(
            drop_cols,
            axis=1,
        ),
        cbm_train_set[TARGET],
    )

    X_test, y_test = (
        cbm_test_set.drop(
            drop_cols,
            axis=1,
        ),
        cbm_test_set[TARGET],
    )
    logging.info(f"X_train.shape, X_test.shape {X_train.shape, X_test.shape}")

    # no time dependent feature -- we can leave it with mode
    X_train = X_train.fillna(X_train.mode().iloc[0])
    X_test = X_test.fillna(X_test.mode().iloc[0])

    return X_train, X_test, y_train, y_test


test_preds = prepare_data_for_train()
print(test_preds.head(5))
X_train, X_test, y_train, y_test = get_ranker_sample(test_preds)
print(X_train.head())


# def get_items_features(item_ids: List[int], item_cols: List[str]) -> Dict[int, Any]:
#     """
#     function to get items features from our available data
#     that we used in training (for all candidates)
#         :item_ids:  item ids to filter by
#         :item_cols: feature cols we need for inference
#
#     EXAMPLE OUTPUT
#     {
#     9169: {
#     'content_type': 'film',
#     'release_year': 2020,
#     'for_kids': None,
#     'age_rating': 16
#         },
#
#     10440: {
#     'content_type': 'series',
#     'release_year': 2021,
#     'for_kids': None,
#     'age_rating': 18
#         }
#     }
#
#     """
#     item_features = read_parquet_from_gdrive(
#         "https://drive.google.com/file/d/1XGLUhHpwr0NxU7T4vYNRyaqwSK5HU3N4/view?usp=share_link"
#     )
#     item_features = item_features.set_index("item_id")
#     item_features = item_features.to_dict("index")
#
#     collect all items
    # output = {}
    # for id in item_ids:
    #     output[id] = {k: v for k, v in item_features.get(id).items() if k in item_cols}
    #
    # return output
#
#
# def get_user_features(user_id: int, user_cols: List[str]) -> Dict[str, Any]:
#     """
#     function to get user features from our available data
#     that we used in training
#         :user_id: user id to filter by
#         :user_cols: feature cols we need for inference
#
#     EXAMPLE OUTPUT
#     {
#         'age': None,
#         'income': None,
#         'sex': None,
#         'kids_flg': None
#     }
#     """
#     users = read_parquet_from_gdrive(
#         "https://drive.google.com/file/d/1MCTl6hlhFYer1BTwjzIBfdBZdDS_mK8e/view?usp=share_link"
#     )
#     users = users.set_index("user_id")
#     users_dict = users.to_dict("index")
#     return {k: v for k, v in users_dict.get(user_id).items() if k in user_cols}
#
#
# def prepare_ranker_input(
#     candidates: Dict[int, int],
#     item_features: Dict[int, Any],
#     user_features: Dict[int, Any],
#     ranker_features_order,
# ):
#     ranker_input = []
#     for k in item_features.keys():
#         item_features[k].update(user_features)
#         item_features[k]["rank"] = candidates[k]
#         item_features[k] = {
#             feature: item_features[k][feature] for feature in ranker_features_order
#         }
#         ranker_input.append(list(item_features[k].values()))
#
#     return ranker_input
#



