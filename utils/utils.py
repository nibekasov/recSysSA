import os

def save_csv_to_path(add_path, data):
    path = os.getcwd()
    path_to_save = os.path.abspath(os.path.join(path, os.pardir)) + add_path
    data.to_csv(path_to_save)