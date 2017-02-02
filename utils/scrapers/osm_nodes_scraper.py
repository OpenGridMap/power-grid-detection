from __future__ import print_function

import os
import sys
import traceback
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
from utils.dataset.nodes import to_csv


class OsmNodesScraper:
    BASE_URL = "http://api.openstreetmap.org/api/0.6/node/{}"

    def __init__(self, nodes, region):
        self.nodes = nodes
        self.region = region
        # self.requests_handler = RequestsHandler()

    def scrape(self, filepath=None, ipython_notebook=False):
        results = TasksHandler.map(self.get_osm_scrape_tasks(), n_tasks=len(self.nodes), n_workers=128,
                                   requests_handler=True, ipython_notebook=ipython_notebook)
        return to_csv(results, filepath)

    def get_osm_scrape_tasks(self):
        for node in self.nodes:
            yield ScrapeTask(node)
        #
        # for i in range(5000):
        #     yield ScrapeTask(self.nodes[i])

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
            print(e)
            traceback.print_exc(file=sys.stdout)
            raise e
            return None
        except AttributeError as e:
            print(e)
            traceback.print_exc(file=sys.stdout)
            raise e
            return None
        except Exception as e:
            print(e)
            traceback.print_exc(file=sys.stdout)
            raise e
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
