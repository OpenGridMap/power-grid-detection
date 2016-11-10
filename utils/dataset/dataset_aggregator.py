import os
from glob import glob

from utils.img.resizer import Resizer

import config

positive_samples_src_dir = config.positive_samples_src_dir
negative_samples_src_dir = config.negative_samples_src_dir

positive_samples = glob(os.path.abspath(positive_samples_src_dir) + '/*.jpg')
negative_samples = glob(os.path.abspath(negative_samples_src_dir) + '/*.jpg')

print('No of positive samples : ', len(positive_samples))
print('No of begative samples : ', len(negative_samples))

dataset_dir = os.path.join(config.dataset_dir, 'raw')
# positive_samples_dir = config.positive_samples_dir
# negative_samples_dir = config.negative_samples_dir

# if not os.path.exists(positive_samples_dir):
#     os.makedirs(positive_samples_dir)
#
# if not os.path.exists(negative_samples_dir):
#     os.makedirs(negative_samples_dir)

resolutions = [256, 128, 64, 32, 16, 8]

resizer = Resizer(dataset_dir, positive_samples_src_dir, negative_samples_src_dir, resolutions,
                  n_positive_samples=15000, n_negative_samples=15000)

resizer.resize()
