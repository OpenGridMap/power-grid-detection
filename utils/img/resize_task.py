import os
import shutil

from PIL import Image

import config

class ResizeTask:
    def __init__(self, src_file, dataset_dir, sample_type, resolutions):
        self.src_file = src_file
        self.dataset_dir = dataset_dir
        self.sample_type = sample_type
        self.resolutions = resolutions

    def __call__(self):
        if os.path.exists(self.src_file):
            im = Image.open(self.src_file)

            for res in self.resolutions:
                file_path = os.path.join(self.dataset_dir, str(res), self.sample_type, os.path.basename(self.src_file))

                if im.size[0] is res:
                    shutil.copy2(self.src_file, file_path)
                    continue

                im_resized = im.resize((res, res))
                im_resized.save(file_path, 'JPEG')
