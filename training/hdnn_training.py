from __future__ import print_function

import os
import sys
import numpy as np

from keras.optimizers import SGD
from keras.callbacks import CSVLogger, ModelCheckpoint

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

import config

from utils.dataset.data_generator import DataGenerator
from models.hdnn import hdnn
from models.cnn3_with_normalization import cnn_w_normalization
from models.mlp_5 import mlp_5


def train(data=None, lr=0.001, batch_size=256, n_epochs=50, input_shape=(48, 48, 3)):
    print('loading model...')
    model = hdnn(input_shape=input_shape)
    # model = cnn_w_normalization(input_shape=input_shape)
    # model = mlp_5(input_shape=input_shape)
    model.summary()

    optimizer = SGD(lr=lr)

    print('compiling model...')
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
    print('done.')

    name = 'cnn_140_1_thr_dil_ero'
    csv_logger = CSVLogger('%s_training.log' % name)
    best_model_checkpointer = ModelCheckpoint(filepath=("./%s_training_weights_best.hdf5" % name), verbose=1,
                                              save_best_only=True)

    print('Initializing data generators...')
    train_data_gen = DataGenerator(dataset_file=config.train_data_file, batch_size=batch_size)
    validation_data_gen = DataGenerator(dataset_file=config.validation_data_file, batch_size=batch_size)
    test_data_gen = DataGenerator(dataset_file=config.test_data_file, batch_size=batch_size)
    print('done.')

    print('Fitting model...')
    history = model.fit_generator(train_data_gen,
                                  nb_epoch=n_epochs,
                                  samples_per_epoch=train_data_gen.n_batches * batch_size,
                                  validation_data=validation_data_gen,
                                  nb_val_samples=validation_data_gen.n_samples,
                                  callbacks=[csv_logger, best_model_checkpointer],
                                  verbose=1)
    print('done.')

    print('Evaluating model...')
    score = model.evaluate_generator(test_data_gen, val_samples=test_data_gen.n_samples)
    print('done.')

    print('Test score:', score[0])
    print('Test accuracy:', score[1])

    return history

    # return model, res


if __name__ == '__main__':
    # train(load_dataset(), n_epochs=500, batch_size=84, input_shape=(180, 180, 3))
    # train(None, n_epochs=500, batch_size=256, input_shape=(180, 180, 3))
    # train(None, n_epochs=500, batch_size=16, input_shape=(140, 140, 3))
    train(None, n_epochs=500, batch_size=48, input_shape=(140, 140, 1))
