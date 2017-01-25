from __future__ import print_function

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

import config

from utils.parsers.transnet_parser import TransnetParser
from utils.scrapers.osm_nodes_scraper import OsmNodesScraper

if __name__ == '__main__':
    region = config.config_params['loc']
    min_voltage = 220000
    max_voltage = 380000

    print('Parsing transnet data...')
    transnet_parser = TransnetParser()

    print('Filtering by region : %s' % region)
    transnet_parser.filter_by_regions(regions='config')

    print('Filtering by voltage,\n min voltage : %d \n max voltage : %d' % (min_voltage, max_voltage))
    transnet_parser.filter_by_min_max_voltage(min_voltage=min_voltage, max_voltage=max_voltage)

    nodes = transnet_parser.nodes
    print('Total nodes : %d' % len(nodes))
    print('done..\n')

    print('Scraping osm data...')
    osm_scraper = OsmNodesScraper(nodes, region)
    n = osm_scraper.scrape()
    print('Scraped %d nodes..' % n)
    print('done..')
