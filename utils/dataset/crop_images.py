import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

import config

from utils.tasks.handler import TasksHandler
from utils.img.crop_task import CropTask
from utils.dataset.annotations import count_annotated_images, load_annotations_nodes


def get_crop_tasks(annotations_file, dest_dir):
    nodes = load_annotations_nodes(annotations_file)
    i = 0

    # tasks = []

    for node in nodes:
        annotations = node['annotations']

        if len(annotations) > 2:
            i += 1
            yield CropTask(node['filename'], annotations, dest_dir, i)
            # task = CropTask(node['filename'], annotations, dest_dir, i)
            # tasks.append(task)

    # return tasks


def crop_annotated_images(annotations_file, dest_dir, ipython_notebook=False):
    tasks = get_crop_tasks(annotations_file, dest_dir)
    # n = len(tasks)
    n = count_annotated_images(annotations_file)
    TasksHandler.map(tasks=tasks, n_tasks=n, ipython_notebook=ipython_notebook)
    print('Finished cropping images')


if __name__ == '__main__':
    crop_annotated_images(config.current_annotations_file, config.cropped_images_dir)
