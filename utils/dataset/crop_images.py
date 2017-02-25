import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

import config

from utils.dataset.annotations import load_annotations, count_annotated_images
from utils.img.tasks import CropTask
from utils.tasks.handler import TasksHandler


def get_crop_tasks(nodes, dest_dir, negative_samples_per_image):
    for node in nodes:
        annotations = node['annotations']

        # if len(annotations) > 0:
        #     yield CropTask(node['filename'], annotations, dest_dir, negative_samples_per_image)

        yield CropTask(node['filename'], annotations, dest_dir, negative_samples_per_image)


def crop_annotated_images(annotations_file, dest_dir, negative_samples_per_image, ipython_notebook=False):
    nodes = load_annotations(annotations_file)
    n = len(nodes)
    tasks = get_crop_tasks(nodes, dest_dir, negative_samples_per_image)
    TasksHandler.map(tasks=tasks, n_tasks=n, ipython_notebook=ipython_notebook)
    print('Finished cropping images')


if __name__ == '__main__':
    try:
        # crop_annotated_images(config.current_annotations_file, config.positive_samples_dir, 8)
        crop_annotated_images(config.final_annotations_file, os.path.join(config.dataset_dir, 'corrected', '19'), 8)
    except Exception as e:
        print(e)
        raise e
