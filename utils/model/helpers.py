import os
import config

from keras.models import model_from_json


def get_model_from_json(fname, path=None):
    if path is None:
        path = config.results_dir

    with open(os.path.join(path, fname), "rb") as json_file:
        model_json = json_file.read()

    return model_from_json(model_json)
