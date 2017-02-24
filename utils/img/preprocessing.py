import numpy as np

from skimage import color
from skimage.transform import resize
from skimage.feature import canny, hog
from skimage.morphology import dilation, erosion, diamond


def edges_hog_gray(img):
    img = color.rgb2gray(img)

    edges = canny(img, sigma=0.80, low_threshold=0.3, high_threshold=0.2)
    fd = hog(img, orientations=9, pixels_per_cell=(12, 12), cells_per_block=(4, 4))
    hog_shape = np.sqrt(fd.shape[0]).astype(int)
    fd = resize(fd.reshape(hog_shape, hog_shape), (img.shape[0], img.shape[1]))

    img = np.dstack((img, edges, fd))

    return img


def edges_dil_ero(img):
    r_threshold = 90
    g_threshold = 90
    b_threshold = 90

    img[img[:, :, 0] < r_threshold] = 0
    img[img[:, :, 1] < g_threshold] = 0
    img[img[:, :, 2] < b_threshold] = 0

    img = color.rgb2gray(img)
    img = dilation(img, diamond(1))
    img = erosion(img, diamond(1))

    return img
