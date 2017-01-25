import os
import sys
import numpy as np

from keras.layers import Input, Convolution2D, MaxPooling2D, BatchNormalization, Flatten, Dense, Activation
from keras.models import Model
from keras.optimizers import SGD
from keras.callbacks import CSVLogger, ModelCheckpoint
from keras.preprocessing.image import ImageDataGenerator

import theano

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

import config

# from utils.dataset.helpers import load_dataset
from utils.dataset.data_iter import DataIter


def cnn_w_normalization(input_shape=(48, 48, 3)):
    # input_img = Input(input_shape, tensor=theano.shared(np.zeros(input_shape, dtype=np.float32), borrow=True))
    input_img = Input(input_shape)

    x = Convolution2D(128, 3, 3, activation='relu')(input_img)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    # x = BatchNormalization()(x)

    x = Convolution2D(256, 3, 3, activation='relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    # x = BatchNormalization()(x)

    x = Convolution2D(256, 3, 3, activation='relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    x = BatchNormalization()(x)

    x = Flatten()(x)
    x = Dense(1024, activation='sigmoid')(x)
    x = Dense(1024, activation='sigmoid')(x)
    x = Dense(512, activation='sigmoid')(x)
    x = Dense(2, activation='sigmoid')(x)
    x = Activation('softmax')(x)

    model = Model(input_img, x)

    return model


def train(data=None, lr=0.001, batch_size=256, n_epochs=20, input_shape=(48, 48, 3)):
    print('loading model...')
    model = cnn_w_normalization(input_shape=input_shape)
    model.summary()

    optimizer = SGD(lr=lr)

    print('compiling model...')
    model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    print('done.')

    # (X_train, y_train), (X_validation, y_validation), (X_test, y_test) = data

    csv_logger = CSVLogger('3cnn_180_training.log')
    # model_checkpointer = ModelCheckpoint(filepath="./mlp_5_a1_weights.hdf5", verbose=1, save_best_only=False)
    best_model_checkpointer = ModelCheckpoint(filepath="./3cnn_180_training_weights_best.hdf5", verbose=1, save_best_only=True)

    # history = model.fit(X_train, y_train, batch_size, n_epochs, validation_data=(X_validation, y_validation),
    #                     callbacks=[csv_logger, best_model_checkpointer], verbose=1)

    data_iter = DataIter(batch_size=batch_size)

    for epoch in range(n_epochs):
        print(epoch)
        for x, y, n in data_iter:
            print('Batch no : ', n)
            model.train_on_batch(x, y)

    # score = model.evaluate(X_test, y_test, verbose=True)

    # print('Test score:', score[0])
    # print('Test accuracy:', score[1])

    # return history


if __name__ == '__main__':
    # train(load_dataset(), n_epochs=500, batch_size=84, input_shape=(180, 180, 3))
    train(None, n_epochs=500, batch_size=32, input_shape=(180, 180, 3))
