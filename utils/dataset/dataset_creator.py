import os

from skimage import io
from glob import iglob
import matplotlib.pyplot as plt
import numpy as np

import config

# io.use_plugin('matplotlib')

pathname = os.path.join(config.positive_samples_dir, '256')

i = 0

images = []
targets = []

for im in iglob(os.path.abspath(pathname) + '/*.jpg'):
    img = io.imread(im)
    img = img.reshape((img.shape[0] * img.shape[1] * img.shape[2],))
    images.append(img)
    targets.append(1)

images = np.array(images)

print(images.shape)
