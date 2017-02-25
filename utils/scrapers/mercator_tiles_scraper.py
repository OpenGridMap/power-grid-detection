from __future__ import print_function

import os
import sys
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

import config

from utils.geo.coordinate import Coordinate
from utils.tasks.handler import TasksHandler
from utils.tiles.tasks import TilesScrapeTask, TilesAffixTask, TileScrapeTask
from utils.dataset.nodes import get_nodes_df
from utils.tiles.adapters import get_adapter
from utils.requests.requests_handler import RequestsHandler


class MercatorTilesScraper(object):
    def __init__(self, files_dir=None):
        self.adapter = get_adapter(files_dir=files_dir)

    def scrape(self, filename=None, n=None, zoom=18, ipython_notebook=False):
        nodes, n = get_nodes_df(filename, n)

        tiles_scrape_tasks = self.get_tiles_scrape_tasks(nodes, zoom, self.adapter)
        TasksHandler.map(tiles_scrape_tasks, n_tasks=n, n_workers=64, requests_handler=True,
                         ipython_notebook=ipython_notebook)
        print('Downloaded all tasks\n')

    def affix_tiles(self, n=None, filename=None, zoom=18, ipython_notebook=False):
        nodes, n = get_nodes_df(filename, n)

        tiles_affix_tasks = self.get_tiles_affix_tasks(nodes, zoom, self.adapter)
        TasksHandler.map(tiles_affix_tasks, n_tasks=n, ipython_notebook=ipython_notebook)
        print('Finished affixing tiles')

    def scrape_area(self, area_coords, zoom=18, ipython_notebook=False):
        # r = RequestsHandler()
        # t = TilesScrapeTask(area_coords, zoom, self.adapter)
        # t(r)

        n = area_coords.get_tiles_count(zoom)

        tiles_scrape_tasks = self.get_tile_scrape_tasks(area_coords, zoom, self.adapter)
        TasksHandler.map(tiles_scrape_tasks, n_tasks=n, n_workers=64, requests_handler=True,
                         ipython_notebook=ipython_notebook)
        print('Downloaded all tasks\n')

        affix_task = TilesAffixTask(1, area_coords, zoom, self.adapter)

        affix_task()

    @staticmethod
    def get_tile_scrape_tasks(coord, zoom, adapter):
        tiles = coord.get_tiles(zoom)

        for tile in tiles:
            yield TileScrapeTask(tile, adapter)

    @staticmethod
    def get_tiles_scrape_tasks(nodes, zoom, adapter):
        for node in nodes.iterrows():
            coord = Coordinate(lat=node[1]['lat'], lon=node[1]['lon'])

            yield TilesScrapeTask(coord, zoom, adapter)

    @staticmethod
    def get_tiles_affix_tasks(nodes, zoom, adapter):
        for node in nodes.iterrows():
            coord = Coordinate(lat=node[1]['lat'], lon=node[1]['lon'])
            osm_id = int(node[1]['osm_id'])

            yield TilesAffixTask(osm_id, coord, zoom, adapter)
