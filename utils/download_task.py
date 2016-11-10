import os

import requests


class DownloadTask(object):
    def __init__(self, url, file_path):
        self.url = url
        self.file_path = file_path

    def __call__(self):
        if os.path.isfile(self.file_path):
            # print('Already Exists : %s' % self.file_path.split('/')[-1])
            return

        req = requests.get(url=self.url, stream=True)

        if req.status_code is 200:
            with open(self.file_path, 'wb') as f:
                for chunk in req.iter_content(1024):
                    f.write(chunk)
            print("Success : %s " % self.file_path)
        else:
            print(req.status_code, req.content)
