import os
import traceback

from PIL import Image

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
        im_src = Image.open(self.src_file)
        basename = os.path.splitext(os.path.basename(self.src_file))[0]
        
        try:
            self.crop_annotated_regions(im_src, basename)
            self.crop_positive_samples(im_src, basename)
            self.crop_negative_samples(im_src, basename)
        except Exception as e:
            traceback.print_exc()
            raise e

    def crop_annotated_regions(self, im_src, basename):
        i = 0

        for annotation in annotations_iter(self.annotations):
            path = self.get_path(basename, i)
            i += 1

            crop_annotated_region(im_src, annotation, path)

    def crop_positive_samples(self, im_src, basename):
        for annotation in annotations_iter(self.annotations):
            crop_positive_samples(im_src, annotation, '%s_%d' % (basename, self.task_no))
            crop_positive_samples(im_src, annotation, '%s_%d' % (basename, self.task_no), window_res=(128, 128))
            crop_positive_samples(im_src, annotation, '%s_%d' % (basename, self.task_no), window_res=(256, 256))

    def crop_negative_samples(self, im_src, basename):
        basename = '%s_%d' % (basename, self.task_no)
        crop_negative_samples(im_src, self.annotations, basename, 30)
        crop_negative_samples(im_src, self.annotations, basename, 30, window_res=(128, 128))
        crop_negative_samples(im_src, self.annotations, basename, 30, window_res=(256, 256))

    def get_path(self, basename, i):
        filename = '%s_%d_%d.jpg' % (basename, i, self.task_no)
        path = os.path.join(self.dest_dir, filename)
        return path
