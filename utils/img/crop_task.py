import os
import traceback
import numpy as np

from PIL import Image
from skimage import io
from skimage import img_as_ubyte
from skimage.color import rgb2gray
from skimage.filters import gaussian, sobel
from skimage.morphology import dilation, square

from utils.dataset.annotations import annotations_iter
from utils.img.helpers import crop_annotated_region, crop_positive_samples, crop_negative_samples


class CropTask(object):
    def __init__(self, src_file, annotations, dest_dir, task_no=None, **kwargs):
        self.src_file = src_file
        self.annotations = annotations
        self.dest_dir = dest_dir
        self.task_no = task_no

        if not os.path.exists(self.dest_dir):
            os.makedirs(self.dest_dir)

    def __call__(self, **kwargs):
        basename = os.path.splitext(os.path.basename(self.src_file))[0]

        # tmp_file = os.path.join('/home/tanuj/tmp/tmp', os.path.basename(self.src_file))
        # im_src = io.imread(self.src_file, as_grey=True)

        try:
            # self.pre_process_img(tmp_file)
            # im_src = Image.open(tmp_file)
            im_src = Image.open(self.src_file)
            self.crop_annotated_regions(im_src, basename)
            # self.crop_positive_samples(im_src, basename)
            self.crop_negative_samples(im_src, basename)
        except Exception as e:
            traceback.print_exc()
            raise e
        finally:
            return

    def pre_process_img(self, path):
        img = io.imread(self.src_file, as_grey=True)
        # img = np.array(img)
        # img = rgb2gray(img)
        # img = img_as_ubyte(img)
        img = gaussian(img, sigma=0.5)
        img = sobel(img)
        img = dilation(img, square(1))
        io.imsave(os.path.abspath(path), img)
        # return Image.fromarray(img, mode='L')

    def crop_annotated_regions(self, im_src, basename):
        i = 0

        for annotation in annotations_iter(self.annotations):
            path = self.get_path(basename, i)
            i += 1

            crop_annotated_region(im_src, annotation, path)

    def crop_positive_samples(self, im_src, basename):
        for annotation in annotations_iter(self.annotations):
            crop_positive_samples(im_src, annotation, '%s_%d' % (basename, self.task_no), window_res=(180, 180))
            # crop_positive_samples(im_src, annotation, '%s_%d' % (basename, self.task_no))
            # crop_positive_samples(im_src, annotation, '%s_%d' % (basename, self.task_no), window_res=(128, 128))
            # crop_positive_samples(im_src, annotation, '%s_%d' % (basename, self.task_no), window_res=(256, 256))

    def crop_negative_samples(self, im_src, basename):
        basename = '%s_%d' % (basename, self.task_no)
        crop_negative_samples(im_src, self.annotations, basename, 3, window_res=(180, 180))
        # crop_negative_samples(im_src, self.annotations, basename, 30)
        # crop_negative_samples(im_src, self.annotations, basename, 30, window_res=(128, 128))
        # crop_negative_samples(im_src, self.annotations, basename, 30, window_res=(256, 256))

    def get_path(self, basename, i):
        filename = '%s_%d_%d.jpg' % (basename, i, self.task_no)
        path = os.path.join(self.dest_dir, filename)
        return path
