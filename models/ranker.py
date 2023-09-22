# import logging
# from typing import Dict, List
# import dill
# import catboost as cb
# import pandas as pd
#
# from configs.config import settings
#
#
# class Ranker:
#     def __init__(self, is_infer=True):
#         if is_infer:
#             logging.info("loading ranker model")
#             self.ranker = cb.CatBoostClassifier().load_model(
#                 fname=settings.CBM_TRAIN_PARAMS.MODEL_PATH
#             )
#             logging.info("LOADED")
#
#         else:
#             pass
#
#     @staticmethod
#     def fit(
#         X_train: pd.DataFrame,
#         y_train: pd.DataFrame,
#         X_test: pd.DataFrame = None,
#         y_test: pd.DataFrame = None,
#     ) -> None:
#         """
#         trains catboost clf model
#         :X_train:
#         :y_train:
#         :X_test:
#         :y_test:
#         :ranker_params
#         """
#
#         logging.info(f"Initialization of ranker model...")
#         cbm_classifier = cb.CatBoostClassifier(
#             loss_function=settings.CBM_TRAIN_PARAMS.LOSS_FUNCTION,
#             iterations=settings.CBM_TRAIN_PARAMS.ITERATIONS,
#             learning_rate=settings.CBM_TRAIN_PARAMS.LEARNING_RATE,
#             depth=settings.CBM_TRAIN_PARAMS.DEPTH,
#             random_state=settings.CBM_TRAIN_PARAMS.RANDOM_STATE,
#             verbose=settings.CBM_TRAIN_PARAMS.VERBOSE,
#         )
#
#         logging.info("Started fitting the model...")
#         cbm_classifier.fit(
#             X_train,
#             y_train,
#             eval_set=(X_test, y_test),
#             early_stopping_rounds=100,  # to avoid overfitting
#             cat_features=settings.RANKER_PREPROCESS_FEATURES.CATEGORICAL_COLS,
#         )
#
#         cbm_classifier.save_model(settings.CBM_TRAIN_PARAMS.MODEL_PATH)
#         logging.info("Model saved!")
#
#     def infer(self, ranker_input: List) -> Dict[str, int]:
#         """
#         inference for the output from lfm model
#         :user_id:
#         :candidates: dict with ranks {"item_id": 1, ...}
#         """
#
#         logging.info("Making predictions...")
#         preds = self.ranker.predict_proba(ranker_input)[:, 1]
#
#         return preds
#
# # m = Ranker()
# # print(m.infer('180809344862945720015299585164694667846'))


import logging
from typing import Dict, List

import catboost as cb
import pandas as pd

from configs.config import settings


class Ranker:
    def __init__(self, is_infer=True):
        if is_infer:
            logging.info("loading ranker model")
            self.ranker = cb.CatBoostClassifier().load_model(
                fname=r"\\wsl$\Ubuntu\home\recSysSA-main\artefacts\catboost_clf.cbm"
            )
        else:
            pass

    @staticmethod
    def fit(
        X_train: pd.DataFrame,
        y_train: pd.DataFrame,
        X_test: pd.DataFrame = None,
        y_test: pd.DataFrame = None,
    ) -> None:
        """
        trains catboost clf model
        :X_train:
        :y_train:
        :X_test:
        :y_test:
        :ranker_params
        """

        logging.info(f"init ranker model")
        cbm_classifier = cb.CatBoostClassifier(
            loss_function=settings.CBM_TRAIN_PARAMS.LOSS_FUNCTION,
            iterations=settings.CBM_TRAIN_PARAMS.ITERATIONS,
            learning_rate=settings.CBM_TRAIN_PARAMS.LEARNING_RATE,
            depth=settings.CBM_TRAIN_PARAMS.DEPTH,
            random_state=settings.CBM_TRAIN_PARAMS.RANDOM_STATE,
            verbose=settings.CBM_TRAIN_PARAMS.VERBOSE,
        )

        logging.info("started fitting the model")
        cbm_classifier.fit(
            X_train,
            y_train,
            eval_set=(X_test, y_test),
            early_stopping_rounds=100,  # to avoid overfitting,
            cat_features=settings.RANKER_PREPROCESS_FEATURES.CATEGORICAL_COLS,
        )

        logging.info('Trying to save model...')
        cbm_classifier.save_model(fname=r"\\wsl$\Ubuntu\home\recSysSA-main\artefacts\catboost_clf.cbm")
    # settings.CBM_TRAIN_PARAMS.MODEL_PATH
    def infer(self, ranker_input: List) -> Dict[str, int]:
        """
        inference for the output from lfm model
        :user_id:
        :candidates: dict with ranks {"item_id": 1, ...}
        """

        logging.info("making predictions...")
        preds = self.ranker.predict_proba(ranker_input)[:, 1]

        return preds


# m = Ranker()
# print(m.infer(['180809344862945720015299585164694667846']))

# print(parent_directory)