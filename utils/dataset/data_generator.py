import os
import pandas as pd

import config

from utils.img.collection import ImageCollection


def get_path(f):
    return os.path.join(config.project_dir, f)


class DataGenerator:
    def __init__(self, dataset_file=None, batch_size=32, as_grey=False, preprocessing=False):
        if dataset_file is None:
            dataset_file = config.data_file

        self.dataset = pd.read_csv(dataset_file)
        self.batch_size = batch_size

        files = self.dataset['filepath'].values.tolist()
        # files = map(get_path, files)

        self.ic = ImageCollection(files, as_grey=as_grey, preprocessing=preprocessing)
        self.n_samples = len(self.ic)
        # self.n_batches = 1. * self.n_samples / batch_size
        self.n_batches = int(self.n_samples / batch_size)

        # if self.n_batches % 1 is not 0:
        #     self.n_batches = int(self.n_batches) + 1

        self.batch_no = 0

    def __iter__(self):
        for batch_no in range(self.n_batches):
            x, y = self.ic[batch_no * self.batch_size: (batch_no + 1) * self.batch_size].concatenate()
            # print(x.shape)
            # print(y.shape)
            yield x, y

    def next(self):
        if self.batch_no == self.n_batches:
            self.reset()

        x, y = self.ic[self.batch_no * self.batch_size: (self.batch_no + 1) * self.batch_size].concatenate()

        self.batch_no += 1

        # print(x.shape)
        # print(y.shape)

        # print('Batch %d/%d' % (self.batch_no, self.n_batches))

        return x, y

    def __len__(self):
        return self.n_batches

    def reset(self):
        self.batch_no = 0

#
# if __name__ == '__main__':
#     di = DataIter(batch_size=500)
#
#     i = 0
#     for x, y in di:
#         # plt.plot(y)
#         # plt.show()
#         print(x)
#         print(y)
#         i += 1
#         if i > 2:
#             break
#
#     print('-------------------')
#     i = 0
#     for x, y in di:
#         # plt.plot(y)
#         # plt.show()
#         # print(x.shape)
#         print(y)
#         i += 1
#         if i > 2:
#             break
