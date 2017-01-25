import pandas as pd

import config

from utils.img.collection import ImageCollection


class DataIter:
    def __init__(self, dataset_file=None, batch_size=32):
        if dataset_file is None:
            dataset_file = config.train_data_file

        self.dataset = pd.read_csv(dataset_file)
        self.batch_size = batch_size

        self.ic = ImageCollection(self.dataset['filepath'].values.tolist())
        self.n_batches = 1. * len(self.ic) / batch_size

        if self.n_batches % 1 is not 0:
            self.n_batches = int(self.n_batches) + 1

    def __iter__(self):
        for batch_no in range(self.n_batches):
            x, y = self.ic[batch_no * self.batch_size: (batch_no + 1) * self.batch_size].concatenate()
            yield x, y, batch_no

    def __len__(self):
        return self.n_batches

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
