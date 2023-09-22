import os
import dill
import numpy as np
import pandas as pd

def save_csv_to_path(add_path, data):
    path = os.getcwd()
    path_to_save = os.path.abspath(os.path.join(path, os.pardir)) + add_path
    data.to_csv(path_to_save)


def read_parquet(file_folder, file_name):
    """
    ADD
    """
    parent_directory = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
    path = f"{parent_directory}{file_folder}{file_name}"

    data = pd.read_parquet(path)
    return data


def rm_parquet(file_folder, file_name):
    """
    ADD
    """
    parent_directory = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
    path = f"{parent_directory}{file_folder}{file_name}"

    os.remove(path)


def save_parquet(file_folder, file_name, data):
    """
    ADD
    """
    parent_directory = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
    path = f"{parent_directory}{file_folder}{file_name}"

    data.to_parquet(path)



def save_model(model: object, file_name: str, file_folder='\\'):
    parent_directory = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
    path = f"{parent_directory}{file_folder}{file_name}"

    with open(f"{path}", "wb") as obj_path:
        dill.dump(model, obj_path)


def load_model(file_name, file_folder='\\'):
    parent_directory = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
    path = f"{parent_directory}{file_folder}{file_name}"

    with open(path, "rb") as obj_file:
        obj = dill.load(obj_file)
    return obj


# copy_files_to_path(
#     src_file_folder=settings.DATA_FOLDERS.ARTEFACTS_DATA_FOLDER,
#     dst_file_folder=settings.DATA_FOLDERS.PREPROCESSED_DATA_FOLDER,
#     file_name=file
# )



def generate_lightfm_recs_mapper(
    model: object,
    item_ids: list,
    known_items: dict,
    user_features: list,
    item_features: list,
    N: int,
    user_mapping: dict,
    item_inv_mapping: dict,
    num_threads: int = 4,
):
    def _recs_mapper(user):
        user_id = user_mapping[user]
        recs = model.predict(
            user_id,
            item_ids,
            user_features=user_features,
            item_features=item_features,
            num_threads=num_threads,
        )

        additional_N = len(known_items[user_id]) if user_id in known_items else 0
        total_N = N + additional_N
        top_cols = np.argpartition(recs, -np.arange(total_N))[-total_N:][::-1]

        final_recs = [item_inv_mapping[item] for item in top_cols]
        if additional_N > 0:
            filter_items = known_items[user_id]
            final_recs = [item for item in final_recs if item not in filter_items]
        return final_recs[:N]

    return _recs_mapper
