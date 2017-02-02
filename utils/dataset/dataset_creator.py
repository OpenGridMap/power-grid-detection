import os
import functools

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from skimage import io
from skimage import util
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from glob import glob1

import config


def images_in_dir(path):
    return glob1(path, '*.jpg')


def get_sample_from_image(image, image_dir, is_tower):
    return dict(filepath=os.path.join(image_dir, image), tower=is_tower)


def get_samples_from_dir(image_dir, is_tower, n_samples):
    images = images_in_dir(image_dir)

    if n_samples is not None and isinstance(n_samples, int):
        images = images[:n_samples]

    images = map(functools.partial(get_sample_from_image, image_dir=image_dir, is_tower=is_tower), images)

    return images


def create_dataset(n_positive_images=None, n_negative_images=None, test_set_size=0.15, validation_set_size=0.15):
    # images = []

    positive_images = get_samples_from_dir(config.positive_samples_dir, 1, n_positive_images)

    print('Positive samples : %d' % len(positive_images))

    negative_images = get_samples_from_dir(config.negative_samples_dir, 0, n_negative_images)
    print('Negative samples : %d' % len(negative_images))

    images = positive_images + negative_images

    images = shuffle(images, random_state=17)
    images = pd.DataFrame(images)

    train_images, test_images = train_test_split(images, test_size=test_set_size + validation_set_size,
                                                 random_state=453)
    validation_images, test_images = train_test_split(test_images,
                                                      test_size=test_set_size / (test_set_size + validation_set_size),
                                                      random_state=531)

    images.to_csv(config.data_file)
    train_images.to_csv(config.train_data_file)
    validation_images.to_csv(config.validation_data_file)
    test_images.to_csv(config.test_data_file)

    print('Training samples : %d ' % train_images.shape[0])
    print('Validation samples : %d' % validation_images.shape[0])
    print('Test samples : %d' % test_images.shape[0])


if __name__ == '__main__':
    create_dataset(n_positive_images=5000, n_negative_images=10000)
