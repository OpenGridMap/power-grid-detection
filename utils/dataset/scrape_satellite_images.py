from __future__ import print_function

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

from utils.scrapers.mercator_tiles_scraper import MercatorTilesScraper

if __name__ == '__main__':
    arcgis_scraper = MercatorTilesScraper()
    arcgis_scraper.scrape(zoom=19)
