import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

from utils.dataset.helpers import create_dataset


if __name__ == '__main__':
    create_dataset(0.15, 0.15)
