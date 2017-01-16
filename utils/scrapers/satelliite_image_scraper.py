from __future__ import print_function

from Queue import Queue
from threading import Thread
from time import time

from progressbar import Bar, Percentage, ProgressBar, SimpleProgress, Timer

from utils.geo.coordinate import Coordinate
from utils.osm.db.models import DataPoint
from utils.osm.db.models import PowerTag
from utils.scrapers.digital_globe_map_scraper import DigitalGlobeMapScraper

j = 0

pbar = ProgressBar(widgets=[Percentage(), ' (', SimpleProgress(), ')', Bar(), Timer(), ' '], redirect_stdout=True)


class DownloadWorker(Thread):
    def __init__(self, queue, id):
        Thread.__init__(self)
        self.queue = queue
        self.scraper = DigitalGlobeMapScraper()
        # self.scraper = ArcgisOnlineScraper()
        self.i = id

    def run(self):
        global j
        while True:
            datapoint = self.queue.get()

            self.scraper.scrape_image_binary(
                # coord=Coordinate(datapoint.longitude, datapoint.latitude),
                coord=Coordinate(datapoint.latitude, datapoint.longitude),
                filename=str(datapoint.node_id) + '.jpg'
            )
            #
            # self.scraper.scrape_non_towers_image(
            #     coord=Coordinate(datapoint.latitude, datapoint.longitude),
            # )

            # datapoint.downloaded = True
            # datapoint.save()

            # print (self.i, datapoint.node_id)

            self.queue.task_done()
            j += 1
            pbar.update(j)


if __name__ == '__main__':
    i = 0
    no_images = 20000
    n_workers = 16
    pbar.start(max_value=no_images)
    ts = time()
    queue = Queue()

    for x in range(n_workers):
        worker = DownloadWorker(queue, x)
        worker.daemon = True
        worker.start()

    dp = DataPoint.select().join(PowerTag).where(PowerTag.tag == 'tower' and DataPoint.latitude > 37.689172)
    for d in dp:
        queue.put(d)
        i += 1

        if i > no_images - 1:
            break

    # for link in range(100):
    #     queue.put(str(link))

    # while j > 0:
    #     print(j)

    queue.join()
    pbar.finish()
    print('Took {}'.format(time() - ts))
