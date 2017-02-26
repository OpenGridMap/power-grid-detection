import os

from keras.models import Model
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Input, Activation, Dropout, Flatten, Dense
from keras.regularizers import l1l2

import config


def cnn_regularized(input_shape=(48, 48, 3), activation_fn='relu', init='glorot_uniform', l1=0.01, l2=0.01, dropout=0.5,
                    weights=None):
    # input_img = Input(input_shape, tensor=theano.shared(np.zeros(input_shape, dtype=np.float32), borrow=True))
    input_img = Input(input_shape)

    # x = Convolution2D(128, 7, 7, activation='relu', border_mode='same')(input_img)
    x = Convolution2D(128, 7, 7, border_mode='same', init=init, W_regularizer=l1l2(l1, l2), b_regularizer=l1l2(l1, l2))(input_img)
    x = Activation(activation_fn)(x)
    x = MaxPooling2D(pool_size=(2, 2), border_mode='same')(x)
    # x = BatchNormalization()(x)

    # x = Convolution2D(64, 5, 5, activation='relu', border_mode='same')(x)
    x = Convolution2D(64, 5, 5, border_mode='same', init=init, W_regularizer=l1l2(l1, l2), b_regularizer=l1l2(l1, l2))(x)
    x = Activation(activation_fn)(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    # x = BatchNormalization()(x)

    # x = Convolution2D(64, 3, 3, activation='relu', border_mode='same')(x)
    x = Convolution2D(64, 3, 3, border_mode='same', init=init, W_regularizer=l1l2(l1, l2), b_regularizer=l1l2(l1, l2))(x)
    x = Activation(activation_fn)(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    # x = BatchNormalization()(x)
    #
    # x = Convolution2D(128, 3, 3, activation='relu')(x)
    # x = MaxPooling2D(pool_size=(2, 2))(x)
    # x = BatchNormalization()(x)
    #
    # x = Convolution2D(128, 3, 3, activation='relu')(x)
    # x = MaxPooling2D(pool_size=(2, 2))(x)
    # x = BatchNormalization()(x)

    # x = Convolution2D(192, 3, 3, activation='relu')(x)
    # x = MaxPooling2D(pool_size=(2, 2))(x)
    # x = BatchNormalization()(x)

    x = Flatten()(x)
    x = Dense(1024, activation='relu', init=init, W_regularizer=l1l2(l1, l2), b_regularizer=l1l2(l1, l2))(x)
    x = Dropout(dropout)(x)
    x = Dense(1024, activation='relu', init=init, W_regularizer=l1l2(l1, l2), b_regularizer=l1l2(l1, l2))(x)
    x = Dropout(dropout)(x)
    x = Dense(512, activation='relu', init=init, W_regularizer=l1l2(l1, l2), b_regularizer=l1l2(l1, l2))(x)
    x = Dense(2, activation='relu', init=init, W_regularizer=l1l2(l1, l2), b_regularizer=l1l2(l1, l2))(x)
    x = Activation('softmax')(x)

    model = Model(input_img, x)

    if weights is not None:
        model.load_weights(weights)

    return model


def cnn(input_shape=(48, 48, 3), activation_fn='relu', init='glorot_uniform', weights=None):
    # input_img = Input(input_shape, tensor=theano.shared(np.zeros(input_shape, dtype=np.float32), borrow=True))
    input_img = Input(input_shape)

    # x = Convolution2D(128, 7, 7, activation='relu', border_mode='same')(input_img)
    x = Convolution2D(128, 7, 7, border_mode='same', init=init)(input_img)
    x = Activation(activation_fn)(x)
    x = MaxPooling2D(pool_size=(2, 2), border_mode='same')(x)
    # x = BatchNormalization()(x)

    # x = Convolution2D(64, 5, 5, activation='relu', border_mode='same')(x)
    x = Convolution2D(64, 5, 5, border_mode='same', init=init)(x)
    x = Activation(activation_fn)(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    # x = BatchNormalization()(x)

    # x = Convolution2D(64, 3, 3, activation='relu', border_mode='same')(x)
    x = Convolution2D(64, 3, 3, border_mode='same', init=init)(x)
    x = Activation(activation_fn)(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    # x = BatchNormalization()(x)
    #
    # x = Convolution2D(128, 3, 3, activation='relu')(x)
    # x = MaxPooling2D(pool_size=(2, 2))(x)
    # x = BatchNormalization()(x)
    #
    # x = Convolution2D(128, 3, 3, activation='relu')(x)
    # x = MaxPooling2D(pool_size=(2, 2))(x)
    # x = BatchNormalization()(x)

    # x = Convolution2D(192, 3, 3, activation='relu')(x)
    # x = MaxPooling2D(pool_size=(2, 2))(x)
    # x = BatchNormalization()(x)

    x = Flatten()(x)
    x = Dense(1024, activation='relu', init=init)(x)
    x = Dense(1024, activation='relu', init=init)(x)
    x = Dense(512, activation='relu', init=init)(x)
    x = Dense(2, activation='relu', init=init)(x)
    x = Activation('softmax')(x)

    model = Model(input_img, x)

    if weights is not None:
        model.load_weights(weights)

    return model
