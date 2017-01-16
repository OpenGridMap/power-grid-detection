import requests
from requests import get
from requests.adapters import HTTPAdapter

import config
import os

from utils.geo.coordinate import Coordinate
from utils.requests.requests_handler import RequestsHandler

import socket

class DigitalGlobeMapScraper(object):
    BASE_URL = "https://api.mapbox.com"
    STATIC_IMAGE_URL = BASE_URL + "/v4/%s/%f,%f,%i/%ix%i%s?access_token=%s"
    FORMAT = {
        '1x': '.png',
        '2x': '@2x.png',
        'png32': '.png32',
        'png64': '.png64',
        'png128': '.png128',
        'png256': '.png256',
        'jpg70': '.jpg70',
        'jpg80': '.jpg80',
        'jpg90': '.jpg90'
    }

    MAP_IDS = {
        'recent': 'digitalglobe.nal0g75k',
        'street': 'digitalglobe.nako6329',
        'terrain': 'digitalglobe.nako1fhg',
        'transparent': 'digitalglobe.nakolk5j',
        'recent_with_streets': 'digitalglobe.nal0mpda'
    }

    def __init__(self, files_dir=None):
        self.map_id = 'recent'
        self.map_format = '1x'
        self.resolution = (256, 256)
        self.api_key = config.config_params['digital-globe']['api-key']

        if files_dir is None:
            self.files_dir = os.path.join(
                os.path.dirname(__file__),
                os.path.pardir,
                os.path.pardir,
                'data',
                'cache',
                'digital-globe',
                self.map_format,
                str(self.resolution[0]),
            )
        else:
            self.files_dir = files_dir

        if not os.path.exists(self.files_dir):
            os.makedirs(self.files_dir)

        self.requests_handler = RequestsHandler()

        # socket.create_connection((DigitalGlobeMapScraper.BASE_URL, 80), timeout=2)
        #
        # s = requests.Session()
        # s.mount(DigitalGlobeMapScraper.BASE_URL, HTTPAdapter(max_retries=2))

    def scrape_image_binary(self, coord, filename=None, zoom_level=18):
        if filename is None:
            filename = "%f_%f.jpg" % (coord.latitude, coord.longitude)

        file_path = os.path.join(self.files_dir, filename)

        if os.path.isfile(file_path):
            # print ('Already Exists')
            return

        url = DigitalGlobeMapScraper.STATIC_IMAGE_URL % (
            DigitalGlobeMapScraper.MAP_IDS[self.map_id],
            coord.longitude,
            coord.latitude,
            zoom_level,
            self.resolution[0],
            self.resolution[1],
            DigitalGlobeMapScraper.FORMAT[self.map_format],
            self.api_key
        )

        self.requests_handler.get_file(url, file_path)

        # req = get(url=url, stream=True)
        #
        # if req.status_code is 200:
        #     with open(file_path, 'wb') as f:
        #         for chunk in req.iter_content(1024):
        #             f.write(chunk)
        # else:
        #     print(req.status_code, req.content)


if __name__ == '__main__':
    d = DigitalGlobeMapScraper(files_dir='/home/tanuj/tmp')
    d.scrape_image_binary(coord=Coordinate(48.275625, 11.676476))
