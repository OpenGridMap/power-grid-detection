import config

from utils.scrapers.mercator_tiles_scraper import MercatorTilesScraper
from utils.geo.coordinate import Coordinate, AreaCoordinates


def scrape_area(top_left, bottom_right, files_dir=None):
    scraper = MercatorTilesScraper(files_dir)
    coords = AreaCoordinates(Coordinate(*top_left), Coordinate(*bottom_right))

    scraper.scrape_area(coords, 19)

if __name__ == '__main__':
    # scrape_area((48.305524, 11.605027), (48.226976, 11.727297), config.test_dir)
    # scrape_area((48.291191, 11.629483), (48.257629, 11.678604), config.test_dir)
    scrape_area((48.285432, 11.650527), (48.257629, 11.678604), config.test_dir)
