from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent))

from data_prep.prepare_split import split_train_test

path = f"{Path(__file__).parent}\data\preprocessed_data"
split_train_test(path)
