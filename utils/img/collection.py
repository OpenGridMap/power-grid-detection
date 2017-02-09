import numpy as np

from skimage import io
from skimage.util import img_as_float
from skimage.transform import resize
from skimage.feature import canny, hog
from sklearn.utils import shuffle
from keras.utils import np_utils


class ImageCollection(io.ImageCollection):
    def __init__(self, load_pattern, conserve_memory=True, **load_func_kwargs):
        super(ImageCollection, self).__init__(load_pattern, conserve_memory, ImageCollection.load_func,
                                              **load_func_kwargs)
        self._files = shuffle(self._files, random_state=17)

    def concatenate(self):
        x = super(ImageCollection, self).concatenate()
        y = map(ImageCollection.is_tower, self.files)
        return x, np_utils.to_categorical(y)

    @staticmethod
    def load_func(f, as_grey=False, **kwargs):
        img = io.imread(f, as_grey=as_grey)
        img = img_as_float(img).astype(np.float32)

        # edges = canny(img, sigma=0.80, low_threshold=0.3, high_threshold=0.2)

        # fd = hog(img, orientations=9, pixels_per_cell=(12, 12), cells_per_block=(4, 4))
        # hog_shape = np.sqrt(fd.shape[0]).astype(int)
        # fd = resize(fd.reshape(hog_shape, hog_shape), (img.shape[0], img.shape[1]))

        # img = np.dstack((img, edges, fd))
        # img = edges.reshape((edges.shape[0], edges.shape[1], 1))

        if len(img.shape) == 2:
            img = img.reshape((img.shape[0], img.shape[1], 1))

        return img

    @staticmethod
    def is_tower(path):
        if 'positive' in path:
            return 1
        # elif 'negative' in path:
        else:
            return 0

# if __name__ == '__main__':
#     images = ImageCollection('/home/tanuj/Workspace/power-grid-detection/data/cache/google-maps/3x3_tiles/*.jpg')
