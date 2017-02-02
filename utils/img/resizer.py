import os
from glob import glob

from utils.img.tasks import ResizeTask
from utils.tasks.handler import TasksHandler


class Resizer:
    def __init__(self, dataset_dir, positive_samples_dir, negative_samples_dir, resolutions, n_positive_samples=None,
                 n_negative_samples=None):
        self.dataset_dir = dataset_dir

        # self.positive_samples_dest_path = os.path.join()
        # self.negative_samples_dest_path = os.path.join()

        for res in resolutions:
            path = os.path.join(self.dataset_dir, str(res), 'positive')

            if not os.path.exists(path):
                os.makedirs(path)

            path = os.path.join(self.dataset_dir, str(res), 'negative')

            if not os.path.exists(path):
                os.makedirs(path)

        self.resolutions = resolutions

        self.positive_samples = glob(os.path.abspath(positive_samples_dir) + '/*.jpg')
        self.negative_samples = glob(os.path.abspath(negative_samples_dir) + '/*.jpg')

        if n_positive_samples is not None:
            self.positive_samples = self.positive_samples[:n_positive_samples]

        if n_negative_samples is not None:
            self.negative_samples = self.negative_samples[:n_negative_samples]

        self.tasks = [ResizeTask(sample, self.dataset_dir, 'positive', resolutions) for sample in self.positive_samples]
        self.tasks += [ResizeTask(sample, self.dataset_dir, 'negative', resolutions) for sample in
                       self.negative_samples]

    def resize(self):
        # print("No of images to resize : %d" % len(self.tasks))
        handler = TasksHandler(self.tasks)
        handler.wait_completion()
