from pathlib import Path
import sys

# sys.path.append(str(Path(__file__).parent))
from airflow.dags.scripts.data_prep.data_preprocessing import \
    load_csv_from_path \
    ,rename_columns \
    ,sampling \
    ,remove_brackets \
    ,drop_nan_values \
    ,check_data_types \
    ,remove_reg_event \
    ,add_session_feature

interactions = load_csv_from_path()

interactions = rename_columns(interactions)
interactions = sampling(interactions)
interactions = remove_brackets(interactions)
interactions = drop_nan_values(interactions)
interactions = check_data_types(interactions)
interactions = remove_reg_event(interactions)
interactions = add_session_feature(interactions)


# path = r"C:\Users\qwerty\Documents\GitHub\recSysSoA\data\preprocessed_data\interactions.parquet"
path = f"{Path(__file__).parent}\data\preprocessed_data\interactions.parquet"
interactions.repartition(1).write.format("parquet").mode("overwrite").save(path)