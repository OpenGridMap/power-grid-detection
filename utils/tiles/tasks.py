import os

from PIL import Image

import config

from utils.tiles.adapters import get_adapter


class TilesScrapeTask:
    def __init__(self, coord, zoom, adapter):
        self.coord = coord
        self.zoom = zoom
        self.adapter = adapter

        print(self.coord.get_tiles_count(19))

    def __call__(self, requests_handler):
        tiles = self.coord.get_tiles(self.zoom)

        print(tiles)

        for tile in tiles:
            url = self.adapter.get_url(tile)
            filepath = self.adapter.get_filepath(tile)

            requests_handler.get_file(url, filepath)
            print(filepath)

        return


class TileScrapeTask:
    def __init__(self, tile, adapter):
        self.tile = tile
        self.adapter = adapter

    def __call__(self, requests_handler):
        url = self.adapter.get_url(self.tile)
        filepath = self.adapter.get_filepath(self.tile)

        requests_handler.get_file(url, filepath)

        return


class TilesAffixTask(object):
    def __init__(self, node, coord, zoom, adapter, affixed_tiles_dir=None):
        self.node = node
        self.coord = coord
        self.zoom = zoom
        self.adapter = adapter

        if affixed_tiles_dir is None:
            affixed_tiles_dir = config.affixed_tiles_dir

        if not os.path.exists(affixed_tiles_dir):
            os.makedirs(affixed_tiles_dir)

        # self.filepath = os.path.join(config.affixed_tiles_dir, str(self.node) + '.jpg')
        self.filepath = os.path.join(affixed_tiles_dir, adapter.get_filename(coord.get_tile(zoom)))

    def __call__(self, **kwargs):
        if os.path.exists(self.filepath):
            return

        xs = []
        ys = []
        res = 256
        tiles = self.coord.get_tiles(self.zoom)

        for tile in tiles:
            x, y = tile[0], tile[1]
            xs.append(x)
            ys.append(y)

        x_min = min(xs)
        y_min = min(ys)

        xs = [x - x_min for x in xs]
        ys = [y - y_min for y in ys]

        x_n = max(xs) + 1
        y_n = max(ys) + 1

        im = Image.new('RGB', (x_n * res, y_n * res))

        try:
            for i in range(x_n):
                for j in range(y_n):
                    filepath = self.adapter.get_filepath((i + x_min, j + y_min, self.zoom))
                    # filename = "{}_{}_{}.jpg".format(i + x_min, j + y_min, self.zoom)
                    # filepath = os.path.join(config.tiles_cache_dir, filename)

                    if os.path.exists(filepath):
                        tile_im = Image.open(filepath)
                        im.paste(tile_im, (i * res, j * res))
                    else:
                        print('Image not found : %s' % filepath)
                        return

            im.save(self.filepath, 'JPEG')
            # return im
        except Exception as e:
            raise e
        finally:
            return
