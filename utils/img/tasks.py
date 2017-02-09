import os
import shutil
import traceback
import numpy as np

from PIL import Image
from skimage import io, color
from skimage.morphology import dilation, erosion, diamond

from utils.dataset.annotations import annotations_iter, get_osm_id_from_annotation
from utils.img.helpers import crop_annotated_region, crop_negative_samples, crop_positive_sample_windows, crop_negative_sample_windows


class CropTask(object):
    def __init__(self, src_file, annotations, dest_dir, negative_samples_per_image, task_no=None, **kwargs):
        self.src_file = src_file
        self.annotations = annotations
        self.dest_dir = dest_dir
        self.task_no = task_no
        self.negative_samples_per_annotation = negative_samples_per_image

        if not os.path.exists(self.dest_dir):
            os.makedirs(self.dest_dir)

    def __call__(self, **kwargs):
        basename = os.path.splitext(os.path.basename(self.src_file))[0]

        try:
            im_src = Image.open(self.src_file)
            self.crop_positive_sample(im_src, basename)
            self.crop_negative_samples(im_src, basename)
            # self.crop_positive_sample_windows(im_src, basename)
            # self.crop_negative_sample_windows(im_src, basename)
        except Exception as e:
            traceback.print_exc()
            raise e
        finally:
            return

    def crop_positive_sample(self, im_src, basename):
        for i, annotation in enumerate(annotations_iter(self.annotations)):
            path = os.path.join(self.dest_dir, 'positive', '%d.jpg' % get_osm_id_from_annotation(annotation))
            crop_annotated_region(im_src, annotation, path)

    def crop_negative_samples(self, im_src, basename):
        path = os.path.join(self.dest_dir, 'negative')
        crop_negative_samples(im_src, self.annotations, self.negative_samples_per_annotation, basename, path)

    def crop_positive_sample_windows(self, im_src, basename):
        for annotation in annotations_iter(self.annotations):
            crop_positive_sample_windows(im_src, annotation, '%s_%d' % (basename, self.task_no), window_res=(140, 140))
            # crop_positive_samples(im_src, annotation, '%s_%d' % (basename, self.task_no))
            # crop_positive_samples(im_src, annotation, '%s_%d' % (basename, self.task_no), window_res=(128, 128))
            # crop_positive_samples(im_src, annotation, '%s_%d' % (basename, self.task_no), window_res=(256, 256))

    def crop_negative_sample_windows(self, im_src, basename):
        basename = '%s_%d' % (basename, self.task_no)
        crop_negative_sample_windows(im_src, self.annotations, basename, 3, window_res=(140, 140))
        # crop_negative_samples(im_src, self.annotations, basename, 30)
        # crop_negative_samples(im_src, self.annotations, basename, 30, window_res=(128, 128))
        # crop_negative_samples(im_src, self.annotations, basename, 30, window_res=(256, 256))

    def get_negative_sample_windows_path(self, basename, i):
        filename = '%s_%d_%d.jpg' % (basename, i, self.task_no)
        path = os.path.join(self.dest_dir, filename)
        return path


class ResizeTask(object):
    def __init__(self, src_file, dataset_dir, sample_type, resolutions, **kwargs):
        self.src_file = src_file
        self.dataset_dir = dataset_dir
        self.sample_type = sample_type
        self.resolutions = resolutions

    def __call__(self, **kwargs):
        if os.path.exists(self.src_file):
            im = Image.open(self.src_file)

            for res in self.resolutions:
                file_path = os.path.join(self.dataset_dir, str(res), self.sample_type, os.path.basename(self.src_file))

                if im.size[0] is res:
                    shutil.copy2(self.src_file, file_path)
                    continue

                im_resized = im.resize((res, res))
                im_resized.save(file_path, 'JPEG')


class PreprocessTask(object):
    def __init__(self, src_file, dest_dir, **kwargs):
        self.src_file = src_file
        self.dest_file = os.path.join(dest_dir, os.path.basename(src_file))

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

    def __call__(self, **kwargs):
        img = io.imread(self.src_file)

        r_threshold = 90
        g_threshold = 90
        b_threshold = 90

        img[img[:, :, 0] < r_threshold] = 0
        img[img[:, :, 1] < g_threshold] = 0
        img[img[:, :, 2] < b_threshold] = 0

        img = color.rgb2gray(img)
        img = dilation(img, diamond(1))
        img = erosion(img, diamond(1))

        img = img.astype(np.float32)

        io.imsave(self.dest_file, img)


if __name__ == '__main__':
    # p = PreprocessTask('/home/tanuj/Workspace/power-grid-detection/data/19_cache/google-maps/3x3_tiles/244410425.jpg',
    #                    None)
    #
    # p()
    Image.MAX_IMAGE_PIXELS = None
    p = PreprocessTask('/home/tanuj/Workspace/power-grid-detection/dataset/test/3.jpg', '/home/tanuj/Workspace/power-grid-detection/dataset/test/processed')
    p()
