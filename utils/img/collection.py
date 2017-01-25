import numpy as np

from skimage import io
from skimage.util import img_as_float
from sklearn.utils import shuffle


class ImageCollection(io.ImageCollection):
    def __init__(self, load_pattern, conserve_memory=True):
        super(ImageCollection, self).__init__(load_pattern, conserve_memory, ImageCollection.load_func)
        self._files = shuffle(self._files, random_state=17)

    def concatenate(self):
        x = super(ImageCollection, self).concatenate()
        y = map(ImageCollection.is_tower, self.files)
        return x, y

    @staticmethod
    def load_func(f):
        img = io.imread(f)
        img = img_as_float(img).astype(np.float32)
        return img

    @staticmethod
    def is_tower(path):
        if 'positive' in path:
            return 1
        # elif 'negative' in path:
        else:
            return 0
