from __future__ import print_function

import os
import sys
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

import config

from utils.geo.coordinate import Coordinate
from utils.tasks.handler import TasksHandler
from utils.tiles.tasks import TilesScrapeTask, TilesAffixTask
from utils.dataset.nodes import get_nodes_df
from utils.tiles.adapters import get_adapter


class MercatorTilesScraper(object):
    def __init__(self, files_dir=None):
        self.adapter = get_adapter(files_dir)

    def scrape(self, n=None, filename=None, zoom=18, ipython_notebook=False):
        nodes, n = get_nodes_df(filename, n)

        tiles_scrape_tasks = self.get_tile_scrape_tasks(nodes, zoom, self.adapter)
        TasksHandler.map(tiles_scrape_tasks, n_tasks=n, n_workers=64, requests_handler=True,
                         ipython_notebook=ipython_notebook)
        print('Downloaded all tasks\n')

        tiles_affix_tasks = self.get_tiles_affix_tasks(nodes, zoom, self.adapter)
        TasksHandler.map(tiles_affix_tasks, n_tasks=n, ipython_notebook=ipython_notebook)
        print('Finished affixing tiles')

    @staticmethod
    def get_tile_scrape_tasks(nodes, zoom, adapter):
        for node in nodes.iterrows():
            coord = Coordinate(lat=node[1]['lat'], lon=node[1]['lon'])

            yield TilesScrapeTask(coord, zoom, adapter)

    @staticmethod
    def get_tiles_affix_tasks(nodes, zoom, adapter):
        for node in nodes.iterrows():
            coord = Coordinate(lat=node[1]['lat'], lon=node[1]['lon'])
            osm_id = int(node[1]['osm_id'])

            yield TilesAffixTask(osm_id, coord, zoom, adapter)
