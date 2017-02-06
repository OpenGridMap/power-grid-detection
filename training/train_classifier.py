import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns

from skimage import io
from skimage.util import view_as_windows
from keras.utils import np_utils
from keras.optimizers import SGD
from keras.callbacks import CSVLogger, ModelCheckpoint
from keras.layers import Dense
from PIL import Image, ImageDraw

sys.path.append('/home/tanuj/Workspace/power-grid-detection')

# %matplotlib inline
# Image.MAX_IMAGE_PIXELS = None

import config

from utils.model.helpers import get_model_from_json
from utils.img.helpers import sliding_window
from utils.dataset.helpers import get_image_collection
from utils.img.collection import ImageCollection
from utils.dataset.data_generator import DataGenerator

lr = 0.01
batch_size = 32
batch_size=256
n_epochs=500
input_shape=(140, 140, 1)
name = 'cnn_140_1_thr_dil_ero_lr_%f_conv_freeze' % lr

model = get_model_from_json('cnn_140_1_thr_dil_ero_lr_0.100000_final.json')
model.load_weights('/home/tanuj/Workspace/power-grid-detection/training/cnn_140_1_thr_dil_ero_lr_0.100000_training_weights_best.hdf5')
# model

for layer in model.layers:
    print(layer)
    if not isinstance(layer, Dense):
        layer.trainable = False

model.summary()

optimizer = SGD(lr=lr)

print('compiling model...')
model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
print('done.')

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
                              verbose=1,
                              callbacks=[csv_logger, best_model_checkpointer])
print('done.')

print('Evaluating model...')
score = model.evaluate_generator(test_data_gen, val_samples=test_data_gen.n_samples)
print('done.')

print('Test score:', score[0])
print('Test accuracy:', score[1])
