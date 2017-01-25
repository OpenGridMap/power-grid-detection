from __future__ import print_function

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

from utils.scrapers.arcgis_scraper import ArcgisScraper

if __name__ == '__main__':
    arcgis_scraper = ArcgisScraper()
    arcgis_scraper.scrape()
