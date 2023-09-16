#
# def preparation():
#
#     import logging
#     # import pathlib
#     #
#     logger = logging.getLogger("Airflow")
#     from pathlib import Path
#     import sys
#
#     sys.path.append(str(Path(__file__).parent.parent.parent))
#
#     from data_prep.data_preprocessing import \
#         load_csv_from_path
#     # \
#     #     , rename_columns \
#     #     , sampling \
#     #     , remove_brackets \
#     #     , drop_nan_values \
#     #     , check_data_types \
#     #     , remove_reg_event \
#     #     , add_session_feature
#
#     logger.info('Reading the data...')
#     #
#     # interactions = load_csv_from_path()
#     # logger.info(f'First rows of initial dataset: {interactions.head(5)}')
#     #
#     #
#     # logger.info('Perform the preprocessing and feature generation...')
#     #
#     # interactions = rename_columns(interactions)
#     # interactions = sampling(interactions)
#     # interactions = remove_brackets(interactions)
#     # interactions = drop_nan_values(interactions)
#     # interactions = check_data_types(interactions)
#     # interactions = remove_reg_event(interactions)
#     # interactions = add_session_feature(interactions)
#     # logger.info(f'First rows of preprocessed dataset: {interactions.head(5)}')
#     #
#     # logger.info('Saving the preprocessed data...')
#     #
#     # path = r"C:\Users\qwerty\Documents\GitHub\recSysSoA\data\preprocessed_data\interactions.parquet"
#     # interactions.repartition(1).write.format("parquet").mode("overwrite").save(path)
#     #
#     # logging.info('Preprocessed data saved!')
#
#
# # C:\Users\qwerty\Documents\GitHub\recSysSoA\airflow\dags\pipeline.py
#
#
#
#
#
