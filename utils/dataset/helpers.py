import os

import numpy as np

from sklearn.utils import shuffle
from sklearn.cross_validation import train_test_split
from skimage import io
from keras.utils.np_utils import to_categorical

import config


def get_image_collection(path):
    if os.path.exists(path):
        pattern = os.path.abspath(path) + os.sep + '/*.jpg'
        return io.imread_collection(pattern, conserve_memory=False)

    raise Exception
#
#
# def create_dataset(test_data_size=0.15, validation_data_size=0.15, dataset_path=None, flatten=False):
#     print('Reading positive images...')
#     positive_images = get_image_collection(config.positive_samples_dir)
#     print('done.')
#     print('Reading negative images...')
#     negative_images = get_image_collection(config.negative_samples_dir)
#     print('done.\n')
#
#     print('Compiling images...')
#     X = []
#
#     for image in positive_images:
#         if flatten:
#             image.flatten()
#
#         X.append(image.tolist())
#
#     for image in negative_images:
#         if flatten:
#             image.flatten()
#
#         X.append(image.tolist())
#
#     print('Creating dataset...')
#     X = np.asarray(X)
#     y = np.zeros((X.shape[0],))
#
#     y[:len(positive_images)] = 1
#
#     # del positive_images, negative_images
#     # gc.collect()
#
#     print('Splitting dataset...')
#     X, y = shuffle(X, y, random_state=64453)
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_data_size + validation_data_size,
#                                                         random_state=457)
#     X_validation, X_test, y_validation, y_test = train_test_split(X_test, y_test, test_size=test_data_size / (
#         test_data_size + validation_data_size), random_state=193)
#
#     del X,
#     gc.collect()
#
#     data = (X_train, y_train), (X_validation, y_validation), (X_test, y_test)
#     print('done.\n')
#
#     print('Pickling data...')
#     if dataset_path is None:
#         dataset_path = config.dataset_file
#
#     with open(dataset_path, 'wb') as f:
#         cPickle.dump(data, f)
#     print('done.')
#
#
# def load_dataset_from_pickle(dataset_path=None):
#     nb_classes = 2
#     if dataset_path is None:
#         dataset_path = config.dataset_file
#
#     print('loading data from %s' % dataset_path)
#
#     with open(dataset_path, 'rb') as f:
#         data = cPickle.load(f)
#
#     (X_train, y_train), (X_validation, y_validation), (X_test, y_test) = data
#
#     X_train = X_train.astype('float32')
#     X_validation = X_validation.astype('float32')
#     X_test = X_test.astype('float32')
#     X_train /= 255.
#     X_validation /= 255.
#     X_test /= 255.
#
#     y_train = to_categorical(y_train, nb_classes)
#     y_validation = to_categorical(y_train, nb_classes)
#     y_test = to_categorical(y_test, nb_classes)
#
#     print(X_train.shape[0], 'training samples')
#     print(X_validation.shape[0], 'validation samples')
#     print(X_test.shape[0], 'test samples')
#
#     return (X_train, y_train), (X_validation, y_validation), (X_test, y_test)
#
#
# def load_dataset(test_data_size=0.15, validation_data_size=0.15, dataset_path=None, flatten=False):
#     nb_classes = 2
#     print('Reading positive images...')
#     positive_images = get_image_collection(config.positive_samples_dir)
#     print('%d samples' % len(positive_images))
#     print('done.')
#     print('Reading negative images...')
#     negative_images = get_image_collection(config.negative_samples_dir)
#     print('%d samples' % len(negative_images))
#     print('done.\n')
#
#     print('Compiling images...')
#     X = []
#
#     for image in positive_images:
#         if flatten:
#             image.flatten()
#
#         X.append(image.tolist())
#
#     for image in negative_images:
#         if flatten:
#             image.flatten()
#
#         X.append(image.tolist())
#
#     print('Creating dataset...')
#     X = np.asarray(X, dtype=np.float32)
#     if len(X.shape) == 3:
#         print('Reshaping X')
#         X = X.reshape((X.shape[0], X.shape[1], X.shape[2], 1))
#
#     y = np.zeros((X.shape[0],), dtype=np.int8)
#
#     X /= 255.
#     y[:len(positive_images)] = 1
#     y = to_categorical(y, nb_classes)
#
#     # del positive_images, negative_images
#     # gc.collect()
#
#     print('Splitting dataset...')
#     X, y = shuffle(X, y, random_state=64453)
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_data_size + validation_data_size,
#                                                         random_state=457)
#     X_validation, X_test, y_validation, y_test = train_test_split(X_test, y_test, test_size=test_data_size / (
#         test_data_size + validation_data_size), random_state=193)
#
#     # X_train = X_train.astype('float32')
#     # X_validation = X_validation.astype('float32')
#     # X_test = X_test.astype('float32')
#     # X_train /= 255.
#     # X_validation /= 255.
#     # X_test /= 255.
#
#     # y_train = to_categorical(y_train, nb_classes)
#     # y_validation = to_categorical(y_train, nb_classes)
#     # y_test = to_categorical(y_test, nb_classes)
#
#     print(X_train.shape[0], 'training samples')
#     print(X_validation.shape[0], 'validation samples')
#     print(X_test.shape[0], 'test samples')
#
#     return (X_train, y_train), (X_validation, y_validation), (X_test, y_test)
