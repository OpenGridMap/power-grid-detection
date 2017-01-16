import os

import utils.requests


class DownloadTask(object):
    def __init__(self, url, file_path):
        self.url = url
        self.file_path = file_path

    def __call__(self, requests_handler):
        return requests_handler.get_file(self.url, self.file_path)
