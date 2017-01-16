from __future__ import print_function

import os
import sys
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

import config

from utils.geo.coordinate import Coordinate
from utils.tasks.handler import TasksHandler
from utils.tiles.tasks import TilesAffixTask


# from utils.tasks.tile_download_task import TileDownloadTask


class ArcgisScraper(object):
    BASE_URL = "http://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{}/{}/{}"
    TILE_FILENAME_FORMAT = "{}_{}_{}.jpg"
    TILE_RESOLUTION = 256

    def __init__(self, files_dir=None):
        if files_dir is None:
            files_dir = config.tiles_cache_dir

        self.files_dir = files_dir

        if not os.path.exists(self.files_dir):
            os.makedirs(self.files_dir)

    def scrape(self, n, filename=None, zoom=18, ipython_notebook=False):
        tile_download_tasks = self.get_tile_downloads_tasks(n, zoom, filename)
        TasksHandler.map(tile_download_tasks, n_tasks=n, n_workers=128, requests_handler=True,
                         ipython_notebook=ipython_notebook)
        print('Downloaded all tasks\n')

        tiles_affix_tasks = self.get_tiles_affix_tasks(n, zoom, filename)
        TasksHandler.map(tiles_affix_tasks, n_tasks=n, ipython_notebook=ipython_notebook)
        print('Finished affixing tiles')

    def get_tile_downloads_tasks(self, n, zoom, filename=None):
        nodes = self.get_nodes_df(filename, n)

        for node in nodes.iterrows():
            coord = Coordinate(lat=node[1]['lat'], lon=node[1]['lon'])

            yield TileDownloadTask(coord, zoom, self.files_dir)

    def get_tiles_affix_tasks(self, n, zoom, filename):
        nodes = self.get_nodes_df(filename, n)

        for node in nodes.iterrows():
            coord = Coordinate(lat=node[1]['lat'], lon=node[1]['lon'])

            yield TilesAffixTask(node[1]['node'], coord, zoom)

    @staticmethod
    def get_nodes_df(filename, n):
        if filename is None:
            filename = config.nodes
        nodes = pd.read_csv(filename, index_col=0, nrows=n)
        return nodes

    @staticmethod
    def get_url(tile):
        url = ArcgisScraper.BASE_URL.format(tile[2], tile[1], tile[0])
        return url

    @staticmethod
    def get_filename(tile):
        # filename = "{}_{}_{}.jpg".format(tile.x, tile.y, tile.z)
        filename = "{}_{}_{}.jpg".format(*tile)
        return filename


class TileDownloadTask:
    def __init__(self, coord, zoom, files_dir):
        self.coord = coord
        self.zoom = zoom
        self.files_path = files_dir

    def __call__(self, requests_handler):
        tiles = self.coord.get_tiles(self.zoom)

        for tile in tiles:
            url = ArcgisScraper.get_url(tile)
            filepath = os.path.join(self.files_path, ArcgisScraper.get_filename(tile))
            requests_handler.get_file(url, filepath)

        return


if __name__ == '__main__':
    scraper = ArcgisScraper()
    scraper.scrape(30000)
