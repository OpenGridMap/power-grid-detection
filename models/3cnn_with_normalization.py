import os
import sys

from keras.layers import Input, Convolution2D, MaxPooling2D, BatchNormalization, Flatten, Dense
from keras.models import Model
from keras.optimizers import SGD
from keras.callbacks import CSVLogger, ModelCheckpoint

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from utils.dataset.helpers import load_dataset


def cnn_w_normalization(input_shape=(48, 48, 3)):
    input_img = Input(input_shape)

    x = Convolution2D(64, 4, 4, activation='relu')(input_img)
    x = MaxPooling2D(pool_size=(1, 1))(x)
    x = BatchNormalization()(x)

    x = Convolution2D(256, 3, 3, activation='relu')(input_img)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    x = BatchNormalization()(x)

    # x = Convolution2D(256, 3, 3, activation='relu')(input_img)
    # x = MaxPooling2D(pool_size=(2, 2))(x)
    # x = BatchNormalization()(x)

    x = Flatten()(x)
    x = Dense(1024, activation='relu')(x)
    x = Dense(1024, activation='relu')(x)
    x = Dense(512, activation='relu')(x)
    x = Dense(2, activation='relu')(x)

    model = Model(input_img, x)

    return model


def train(data, lr=0.001, batch_size=256, n_epochs=20, input_shape=(48, 48, 3)):
    print('loading model...')
    model = cnn_w_normalization(input_shape=input_shape)
    model.summary()

    optimizer = SGD(lr=lr)

    print('compiling model...')
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['binary_accuracy', 'binary_crossentropy'])

    (X_train, y_train), (X_validation, y_validation), (X_test, y_test) = data

    csv_logger = CSVLogger('3ccn_w_n_a1_1o_training.log')
    # model_checkpointer = ModelCheckpoint(filepath="./mlp_5_a1_weights.hdf5", verbose=1, save_best_only=False)
    best_model_checkpointer = ModelCheckpoint(filepath="./3ccn_w_n_a1_1o_weights_best.hdf5", verbose=0, save_best_only=True)

    history = model.fit(X_train, y_train, batch_size, n_epochs, validation_data=(X_validation, y_validation),
                        callbacks=[csv_logger, best_model_checkpointer], verbose=1)

    score = model.evaluate(X_test, y_test, verbose=True)

    print('Test score:', score[0])
    print('Test accuracy:', score[1])

    return history


if __name__ == '__main__':
    train(load_dataset(), n_epochs=500, batch_size=128)
