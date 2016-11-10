import os

from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.optimizers import SGD

import config

training_data_dir = os.path.join(config.dataset_dir, 'raw', '256')

n_train_samples = 30000
n_epochs = 50
img_width, img_height = 256, 256

datagen = ImageDataGenerator()
train_generator = datagen.flow_from_directory(
        training_data_dir,
        target_size=(img_width, img_height),
        batch_size=8,
        class_mode='binary')

model = Sequential()
model.add(Convolution2D(32, 3, 3, input_shape=(3, img_width, img_height)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(500, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(500, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))


sgd = SGD(lr=0.1, momentum=0.001)

model.compile(loss='binary_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])

model.fit_generator(
        train_generator,
        samples_per_epoch=n_train_samples,
        nb_epoch=n_epochs)