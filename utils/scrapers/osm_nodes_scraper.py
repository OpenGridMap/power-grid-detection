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


class OsmNodeScraper(object):
    BASE_URL = "http://api.openstreetmap.org/api/0.6/node/{}"

    def __init__(self, nodes, region):
        self.nodes = nodes
        self.region = region
        self.requests_handler = RequestsHandler()

    def scrape(self, filepath=None):
        nodes = []
        pbar = ProgressBar(len(self.nodes))

        try:
            for node in self.nodes:
                res = self.requests_handler.get(self.get_url(node))
                coord = self.get_coord_from_osm_response(res)
                if coord is not None:
                    point = {'node': node, 'lat': coord.latitude, 'lon': coord.longitude}
                    nodes.append(point)
                pbar.update()
        finally:
            self.to_csv(nodes, filepath)
            pbar.finish()

    @staticmethod
    def to_csv(nodes, filepath=None):
        if filepath is None:
            filepath = config.nodes

        df = pd.DataFrame(nodes)
        print(df.head())
        df.to_csv(filepath, sep=',')

    @staticmethod
    def get_url(node):
        return OsmNodeScraper.BASE_URL.format(node)

    @staticmethod
    def get_coord_from_osm_response(res):
        try:
            t = etree.fromstring(res.content)
            lat = float(t[0].get('lat'))
            lon = float(t[0].get('lon'))

            return Coordinate(lat, lon)
        except lxml.etree.XMLSyntaxError as e:
            print(e)
            return None
        except AttributeError as e:
            print(e)
            return None
        except Exception as e:
            print(e)
            return None


if __name__ == '__main__':
    with open(config.transnet_nodes_file, "rb") as f:
        nodes = pickle.load(f)

    scraper = OsmNodeScraper(nodes, config.config_params['loc'])
    scraper.scrape()
