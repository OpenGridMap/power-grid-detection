from __future__ import print_function
import os
import numpy as np
import skimage
import skimage.io as io

from skimage.io.collection import ImageCollection

import config


# from utils.dataset.helpers import load_dataset_from_pickle, get_image_collection
# from keras.applications import VGG16

# def info(x, y):
#     print(x.shape)
#     print(y.shape)
#     print('{0:.2f} GB\n'.format((x.nbytes + y.nbytes) / (1024.0 ** 3)))
#
#
# def test_load_data():
#     (X_train, y_train), (X_validation, y_validation), (X_test, y_test) = load_dataset_from_pickle()
#     print('Training data')
#     info(X_train, y_train)
#     print('Validation data')
#     info(X_validation, y_validation)
#     print('Test data')
#     info(X_test, y_test)


# if __name__ == '__main__':
#     test_load_data()
# images = get_image_collection(config.positive_samples_dir)
#
# print(images[0].shape)

def get_image_collection(path):
    if os.path.exists(path):
        print(path)
        pattern = os.path.abspath(path) + os.sep + '*.jpg'
        return io.imread_collection(pattern, conserve_memory=False)

    raise Exception


def get_images(path):
    pattern = os.path.abspath(path) + os.sep + '*.jpg'
    return ImageCollection(pattern, load_func=imread_convert)


def imread_convert(f, **kwargs):
    return io.imread(f).astype(np.float32)


if __name__ == '__main__':
    # images = get_image_collection(config.positive_samples_dir)

    # print(images)
    ims = get_images(config.positive_samples_dir)

    print(skimage.__version__)

    # print(ims[0:5].concatenate().shape)
    print(ims[0:5])
