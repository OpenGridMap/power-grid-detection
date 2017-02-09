import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

import config

from utils.tasks.handler import TasksHandler
from utils.img.tasks import CropTask
from utils.dataset.annotations import count_annotated_images, load_annotations_nodes


def get_crop_tasks(annotations_file, dest_dir):
    nodes = load_annotations_nodes(annotations_file)
    i = 0

    for node in nodes:
        annotations = node['annotations']

        if len(annotations) > 0:
            i += 1
            yield CropTask(node['filename'], annotations, dest_dir, i)


def crop_annotated_images(annotations_file, dest_dir, ipython_notebook=False):
    n = count_annotated_images(annotations_file)
    tasks = get_crop_tasks(annotations_file, dest_dir)
    TasksHandler.map(tasks=tasks, n_tasks=n, ipython_notebook=ipython_notebook)
    print('Finished cropping images')


if __name__ == '__main__':
    try:
        crop_annotated_images(config.current_annotations_file, config.positive_samples_dir)
    except Exception as e:
        print(e)
        raise e
