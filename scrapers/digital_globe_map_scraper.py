from os import path, makedirs

from requests import get

from config import config


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

    def __init__(self, files_dir='data/raw'):
        self.files_dir = files_dir
        self.api_key = config['digital-globe']['api-key']

        if not path.exists(files_dir):
            makedirs(files_dir)

    def scrape_image_binary(self, coord, filename=None, zoom_level=18, resolution=(1280, 1280), map_id='recent',
                            map_format='2x'):
        if not path.exists(path.join(self.files_dir, map_format)):
            makedirs(path.join(self.files_dir, map_format))

        if filename is None:
            filename = "%f_%f.jpg" % (coord.latitude, coord.longitude)

        url = DigitalGlobeMapScraper.STATIC_IMAGE_URL % (
            DigitalGlobeMapScraper.MAP_IDS[map_id],
            coord.longitude,
            coord.latitude,
            zoom_level,
            resolution[0],
            resolution[1],
            DigitalGlobeMapScraper.FORMAT[map_format],
            self.api_key
        )

        file_path = path.join(self.files_dir, map_format, filename)

        if path.isfile(file_path):
            # print ('Already Exists')
            return

        req = get(url=url, stream=True)

        if req.status_code is 200:
            with open(file_path, 'wb') as f:
                for chunk in req.iter_content(1024):
                    f.write(chunk)


# if __name__ == '__main__':
#     d = DigitalGlobeMapApiScraper()
#     d.scrape_image_binary(
#         coord=GeoCoordinate(48.275625, 11.676476)
#     )
