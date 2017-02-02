import os
import sys
import glob

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

import config

from utils.tasks.handler import TasksHandler
from utils.img.tasks import PreprocessTask


def get_samples(path):
    return glob.glob(path + '/*.jpg')


def get_prepocess_tasks():
    samples = get_samples(config.affixed_tiles_dir)

    for sample in samples:
        yield PreprocessTask(sample, config.preprocessed_tiles_dir)


def get_task_count():
    return len(get_samples(config.affixed_tiles_dir))


def preprocess_images():
    tasks = get_prepocess_tasks()
    n = get_task_count()

    print(n)

    TasksHandler.map(tasks, n, 32)
    print('Finished preprocessing images')


if __name__ == '__main__':
    preprocess_images()
