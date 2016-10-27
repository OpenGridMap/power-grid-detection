from __future__ import print_function

import os
import requests

from utils.geo.coordinate import Coordinate


class ArcgisOnlineScraper(object):
    BASE_URL = "http://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{}/{}/{}"
    TILE_RESOLUTION = 256

    def __init__(self, files_dir=None):
        if files_dir is None:
            self.files_dir = os.path.join(
                os.path.dirname(__file__),
                os.path.pardir,
                'data',
                'cache',
                'arcgis-online',
                str(ArcgisOnlineScraper.TILE_RESOLUTION)
            )
        else:
            self.files_dir = files_dir

        if not os.path.exists(self.files_dir):
            os.makedirs(self.files_dir)

    def scrape_image_binary(self, coord, zoom_level=None):
        if zoom_level is None:
            zoom_level = [18]

        tiles = coord.get_bbox_tiles(zoom_level)

        files = []

        for tile in tiles:
            print()
            print(tile)

            url = ArcgisOnlineScraper.BASE_URL.format(tile.z, tile.y, tile.x)

            filename = "%d_%d_%d.jpg" % (tile.y, tile.x, tile.z)
            files += filename

            file_path = os.path.join(self.files_dir, filename)

            if os.path.isfile(file_path):
                print('Already Exists')
                continue

            req = requests.get(url=url, stream=True)

            if req.status_code is 200:
                with open(file_path, 'wb') as f:
                    for chunk in req.iter_content(1024):
                        f.write(chunk)
                print('Success')
            else:
                print(req.status_code)


if __name__ == '__main__':
    d = ArcgisOnlineScraper()
    d.scrape_image_binary(coord=Coordinate(48.27563, 11.676431))
