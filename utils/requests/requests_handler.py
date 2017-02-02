import os
import requests
import config


class RequestsHandler:
    def __init__(self):
        self.session = requests.Session()
        self.session.proxies = config.proxies

    def get(self, url, **kwargs):
        try:
            return self.session.get(url, **kwargs)
        except requests.ConnectTimeout as e:
            print(e)
        except requests.ConnectionError as e:
            print(e)
        except requests.HTTPError as e:
            print(e)

    def get_file(self, url, file_path):
        if os.path.isfile(file_path):
            # print('Already Exists : %s' % self.file_path.split('/')[-1])
            return

        req = self.get(url=url, stream=True)

        if req.status_code is 200:
            with open(file_path, 'wb') as f:
                for chunk in req.iter_content(1024):
                    f.write(chunk)

            return True
        else:
            print(req.status_code)
            # print(req.content)
            return False

    def __del__(self):
        self.session.close()

# if __name__ == '__main__':
#     r = RequestsHandler()
#     print(r.get("http://httpbin.org/ip").text)
