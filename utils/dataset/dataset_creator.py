import os

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


def create_dataset():
    positive_images = images_in_dir(config.positive_samples_dir)
    negative_images = images_in_dir(config.negative_samples_dir)

    print('Positive samples :', len(positive_images))
    print('Negative samples :', len(negative_images))

    images = []

    for image in positive_images:
        images.append(dict(filepath=os.path.join(config.positive_samples_dir, image), tower=1))

    for image in negative_images:
        images.append(dict(filepath=os.path.join(config.negative_samples_dir, image), tower=0))

    # images = random.shuffle(images)

    images = shuffle(images, random_state=17)
    images = pd.DataFrame(images)

    print(images.columns)

    images.to_csv(config.data_file)

    train_images, test_images = train_test_split(images, test_size=0.3, random_state=453)
    validation_images, test_images = train_test_split(test_images, test_size=0.5, random_state=531)

    train_images.to_csv(config.train_data_file)
    validation_images.to_csv(config.validation_data_file)
    test_images.to_csv(config.test_data_file)

    print('Training samples : %d ' % train_images.shape[0])
    print('Validation samples : %d' % validation_images.shape[0])
    print('Test samples : %d' % test_images.shape[0])


if __name__ == '__main__':
    create_dataset()
