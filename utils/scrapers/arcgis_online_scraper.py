from __future__ import print_function

import os
import shutil
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

from utils.geo.coordinate import Coordinate
from utils.requests.requests_handler import RequestsHandler


class ArcgisOnlineScraper(object):
    BASE_URL = "http://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{}/{}/{}"
    TILE_RESOLUTION = 256

    def __init__(self, files_dir=None):
        if files_dir is None:
            files_base_dir = os.path.join(
                os.path.dirname(__file__),
                os.path.pardir,
                'data',
                'cache',
                'arcgis-online'
            )

            self.files_dir = os.path.join(files_base_dir, 'positive', str(self.TILE_RESOLUTION))
            self.negative_files_dir = os.path.join(files_base_dir, 'negative', str(self.TILE_RESOLUTION))

        else:
            self.files_dir = files_dir

        if not os.path.exists(self.files_dir):
            os.makedirs(self.files_dir)

        if not os.path.exists(self.negative_files_dir):
            os.makedirs(self.negative_files_dir)

        self.requests_handler = RequestsHandler()

    def scrape_image_binary(self, coord, zoom=18, filename=None):
        tiles = coord.get_tiles(zoom)
        files = []
        ts = []

        for tile in tiles:
            url = self.get_url(tile)
            file_path = self.get_file_path(tile)

            files.append(os.path.abspath(file_path))

            self.requests_handler.get_file(url, file_path)

            # tile_download_task = DownloadTask(url, file_path)
            # tile_download_task()

            ts.append(tile)

        # extract_image_from_tiles(coord, self.files_dir)

    def get_file_path(self, tile):
        # filename = "{}_{}_{}.jpg".format(tile.x, tile.y, tile.z)
        filename = "{}_{}_{}.jpg".format(*tile)
        file_path = os.path.join(self.files_dir, filename)
        return file_path

    def scrape_non_towers_image(self, coord, zoom=18):
        self.scrape_image_binary(coord)

        negative_tiles = coord.get_negative_tiles()

        for tile in negative_tiles:
            src_file = self.get_file_path(tile)

            if os.path.exists(src_file):
                dest_file = os.path.join(self.negative_files_dir, os.path.basename(src_file))
                shutil.copy2(src_file, dest_file)
                # print(dest_file, 'done')

        # tiles = coord.get_tiles(zoom)
        # files = []
        # ts = []

        # for tile in tiles:
        #     url = self.BASE_URL.format(tile[2], tile[1], tile[0])
        #
        #     filename = "{}_{}_{}.jpg".format(*tile)
        #     file_path = os.path.join(self.files_dir, filename)
        #
        #     files.append(os.path.abspath(file_path))
        #
        #     tile_download_task = DownloadTask(url, file_path)
        #     tile_download_task()
        #
        #     ts.append(tile)

    @staticmethod
    def get_url(tile):
        url = ArcgisOnlineScraper.BASE_URL.format(tile[2], tile[1], tile[0])
        return url


if __name__ == '__main__':
    d = ArcgisOnlineScraper()
    # d.scrape_image_binary(coord=Coordinate(48.27563, 11.676431))
    d.scrape_non_towers_image(coord=Coordinate(48.27563, 11.676431))
    # d.scrape_image_binary(coord=Coordinate(48.275414, 11.671253))
    # d.scrape_image_binary(coord=Coordinate(48.277216, 11.666555))
    # d.scrape_image_binary(coord=Coordinate(48.279559, 11.660474))
    # d.scrape_image_binary(coord=Coordinate(48.281356, 11.655743))
    # d.scrape_image_binary(coord=Coordinate(48.284803, 11.646886))
    # d.scrape_image_binary(coord=Coordinate(48.285232, 11.641625))
