from __future__ import print_function

import os
import itertools
import multiprocessing
import requests
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from utils.geo.coordinate import Coordinate
from utils.progress_bar import PBar
from utils.download_helpers import DownloadWorker, DownloadTask
from utils.tiles.tile_extractor import extract_image_from_tiles


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

    def scrape_image_binary(self, coord, zoom=18):
        tiles = coord.get_tiles(zoom)
        files = []
        ts = []

        for tile in tiles:
            print(tile)
            # url = ArcgisOnlineScraper.BASE_URL.format(tile.z, tile.y, tile.x)
            url = ArcgisOnlineScraper.BASE_URL.format(tile[2], tile[1], tile[0])
            # filename = "{}_{}_{}.jpg".format(tile.x, tile.y, tile.z)
            filename = "{}_{}_{}.jpg".format(*tile)
            file_path = os.path.join(self.files_dir, filename)

            files.append(os.path.abspath(file_path))

            tile_download_task = DownloadTask(url, file_path)
            tile_download_task()

            ts.append(tile)

        extract_image_from_tiles(coord, self.files_dir)



if __name__ == '__main__':
    d = ArcgisOnlineScraper()
    d.scrape_image_binary(coord=Coordinate(48.27563, 11.676431))
    d.scrape_image_binary(coord=Coordinate(48.277207, 11.666549))
    # d.scrape_image_binary(coord=Coordinate(48.131293, 11.562091))
    # d.scrape_image_binary(coord=Coordinate(48.131293, 15.582091))
    # d.scrape_image_binary(coord=Coordinate(48.131293, 15.582091))
    # d.scrape_image_binary(coord=Coordinate(47.131293, 11.582091))
#