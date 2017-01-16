import os
import sys

from keras.optimizers import SGD
from keras.callbacks import CSVLogger, ModelCheckpoint

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from utils.dataset.helpers import load_dataset
from models.vgg_simplified_10 import VGG10


def train(data, lr=0.001, batch_size=256, n_epochs=20, input_shape=(48, 48, 3)):
    print('loading model...')
    model = VGG10(input_shape=input_shape)
    model.summary()

    optimizer = SGD(lr=lr)

    print('compiling model...')
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['binary_accuracy', 'binary_crossentropy'])

    (X_train, y_train), (X_validation, y_validation), (X_test, y_test) = data

    csv_logger = CSVLogger('vgg_10_a1_training.log')
    # model_checkpointer = ModelCheckpoint(filepath="./vgg_10_a1_weights.hdf5", verbose=1, save_best_only=False)
    best_model_checkpointer = ModelCheckpoint(filepath="./vgg_10_a1_weights_best.hdf5", verbose=1, save_best_only=True)

    history = model.fit(X_train, y_train, batch_size, n_epochs, validation_data=(X_validation, y_validation),
              callbacks=[csv_logger, best_model_checkpointer], verbose=1)

    score = model.evaluate(X_test, y_test, verbose=True)

    print('Test score:', score[0])
    print('Test accuracy:', score[1])

    return history


# if __name__ == '__main__':
#     train(load_dataset())
