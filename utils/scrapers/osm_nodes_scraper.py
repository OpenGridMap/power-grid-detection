from __future__ import print_function

import os
import pickle

import lxml
import pandas as pd
import numpy as np

from lxml import etree

import config

from utils.tasks.handler import TasksHandler
from utils.requests.requests_handler import RequestsHandler
from utils.geo.coordinate import Coordinate
from utils.tasks.progress_bar import ProgressBar


class OsmNodesScraper:
    BASE_URL = "http://api.openstreetmap.org/api/0.6/node/{}"

    def __init__(self, nodes, region):
        self.nodes = nodes
        self.region = region
        # self.requests_handler = RequestsHandler()

    def scrape(self, filepath=None, ipython_notebook=False):
        # nodes = []
        # pbar = ProgressBar(len(self.nodes))

        # results = TasksHandler.map(self.get_osm_scrape_tasks(), n_tasks=len(self.nodes), n_workers=128,
        results = TasksHandler.map(self.get_osm_scrape_tasks(), n_tasks=5000, n_workers=128,
                                   requests_handler=True, ipython_notebook=ipython_notebook)
        n = self.to_csv(results, filepath)

        return n

        # try:
        #     for node in self.nodes:
        #         res = self.requests_handler.get(self.get_url(node))
        #         coord = self.get_coord_from_osm_response(res)
        #         if coord is not None:
        #             point = {'node': node, 'lat': coord.latitude, 'lon': coord.longitude}
        #             nodes.append(point)
        #         pbar.update()
        # finally:
        #     self.to_csv(nodes, filepath)
        #     pbar.finish()

    def get_osm_scrape_tasks(self):
        # for node in self.nodes:
        #     yield ScrapeTask(node)

        for i in range(5000):
            yield ScrapeTask(self.nodes[i])

    @staticmethod
    def to_csv(nodes, filepath=None):
        if filepath is None:
            filepath = config.nodes

        df = pd.DataFrame(nodes)
        print(df.head())
        df.to_csv(filepath, sep=',')

        return df.shape[0]

    @staticmethod
    def get_url(node):
        return OsmNodesScraper.BASE_URL.format(node)

    @staticmethod
    def get_coord_from_osm_response(res):
        try:
            t = etree.fromstring(res.content)
            lat = float(t[0].get('lat'))
            lon = float(t[0].get('lon'))

            return Coordinate(lat, lon)
        except lxml.etree.XMLSyntaxError as e:
            # print(e)
            return None
        except AttributeError as e:
            # print(e)
            return None
        except Exception as e:
            # print(e)
            return None


class ScrapeTask:
    def __init__(self, node):
        self.node = node

    def __call__(self, requests_handler):
        try:
            res = requests_handler.get(OsmNodesScraper.get_url(self.node))
            coord = OsmNodesScraper.get_coord_from_osm_response(res)
            return {'osm_id': self.node, 'lat': coord.latitude, 'lon': coord.longitude}
        except Exception as e:
            return None


if __name__ == '__main__':
    with open(config.transnet_nodes_file, "rb") as f:
        nodes = pickle.load(f)

    scraper = OsmNodesScraper(nodes, config.config_params['loc'])
    scraper.scrape()
