import csv
import numpy as np

from keras.callbacks import CSVLogger
from collections import OrderedDict, Iterable


class Logger(CSVLogger):
    def __init__(self, filename, separator=',', append=False):
        super(Logger, self).__init__(filename, separator, append)

    def on_batch_end(self, batch, logs={}):
        def handle_value(k):
            is_zero_dim_ndarray = isinstance(k, np.ndarray) and k.ndim == 0
            if isinstance(k, Iterable) and not is_zero_dim_ndarray:
                return '"[%s]"' % (', '.join(map(lambda x: str(x), k)))
            else:
                return k

        if not self.writer:
            self.keys = sorted(logs.keys())
            self.writer = csv.DictWriter(self.csv_file, fieldnames=['batch'] + self.keys)
            self.writer.writeheader()

        row_dict = OrderedDict({'batch': batch})
        row_dict.update((key, handle_value(logs[key])) for key in self.keys)
        self.writer.writerow(row_dict)
        self.csv_file.flush()

    def on_epoch_end(self, epoch, logs={}):
        return
