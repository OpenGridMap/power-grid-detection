import os
import sys

from keras.layers import Input, Dense, Reshape, Flatten
from keras.models import Model
from keras.optimizers import SGD
from keras.callbacks import CSVLogger, ModelCheckpoint

sys.path.append(os.path.join(os.getcwd(), os.pardir))

# from utils.dataset.helpers import load_dataset


def mlp_5(input_shape=(48, 48, 3)):
    input_img = Input(input_shape)
    # x = Reshape((input_shape[0] * input_shape[1] * input_shape[2], ))(input_img)

    x = Flatten()(input_img)

    x = Dense(4096, activation='sigmoid', name='D1')(x)
    x = Dense(4096, activation='sigmoid', name='D2')(x)
    x = Dense(2048, activation='sigmoid', name='D3')(x)
    x = Dense(2048, activation='sigmoid', name='D4')(x)
    x = Dense(2, activation='softmax', name='O')(x)

    model = Model(input_img, x)

    return model


def train(data, lr=0.001, batch_size=256, n_epochs=20, input_shape=(48, 48, 3)):
    print('loading model...')
    model = mlp_5(input_shape=input_shape)
    model.summary()

    optimizer = SGD(lr=lr)

    print('compiling model...')
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['binary_accuracy', 'binary_crossentropy'])

    (X_train, y_train), (X_validation, y_validation), (X_test, y_test) = data

    csv_logger = CSVLogger('mlp_5_a1_processed_training.log')
    # model_checkpointer = ModelCheckpoint(filepath="./mlp_5_a1_weights.hdf5", verbose=1, save_best_only=False)
    best_model_checkpointer = ModelCheckpoint(filepath="./mlp_5_a1_processed_weights_best.hdf5", verbose=1, save_best_only=True)

    history = model.fit(X_train, y_train, batch_size, n_epochs, validation_data=(X_validation, y_validation),
                        callbacks=[csv_logger, best_model_checkpointer], verbose=1)

    score = model.evaluate(X_test, y_test, verbose=True)

    print('Test score:', score[0])
    print('Test accuracy:', score[1])

    return history


# if __name__ == '__main__':
#     train(load_dataset(), n_epochs=500, batch_size=2048, input_shape=(128, 128, 1))
