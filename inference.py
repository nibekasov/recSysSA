import logging
import numpy as np
import pandas as pd

from models.lfm import LFMModel
from models.ranker import Ranker
from configs.config import settings
from utils.utils import (
    read_parquet,
    # compute_metrics
)
# from data_prep.prepare_ranker_data import (
#     prepare_ranker_input
# )
def get_recommendations(user_id: str, top_k: int = 20):
    """
    function to get recommendation for a given user id
    """
    lfm_model = LFMModel()
#     ranker = Ranker()
    try:
        logging.info('Getting 1st level candidates...')
        candidates = lfm_model.infer(user_id=user_id, top_k=top_k)
        return candidates
    except KeyError:
        output = "<p>Please enter the User ID that is in Wildberries database, {} is irrelevant.</p>".format(user_id)
        return output


# user_id = '283725137902134437008251670019063891876'
# result = get_recommendations(user_id)
# print(result)

# users_data = pd.read_parquet(r"\\wsl$\Ubuntu\home\recSysSA-main\data\preprocessed_data\interactions_local_train.parquet")
# random_user_id = np.random.choice(users_data['user_id'].unique(), 1)[0]
# print(random_user_id)
