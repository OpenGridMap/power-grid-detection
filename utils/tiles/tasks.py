import os

from PIL import Image
import config


class TilesAffixTask(object):
    def __init__(self, node, coord, zoom):
        self.node = node
        self.coord = coord
        self.zoom = zoom

        if not os.path.exists(config.affixed_tiles_dir):
            os.makedirs(config.affixed_tiles_dir)

        self.filepath = os.path.join(config.affixed_tiles_dir, str(self.node) + '.jpg')

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
                    filename = "{}_{}_{}.jpg".format(i + x_min, j + y_min, self.zoom)
                    file_path = os.path.join(config.tiles_cache_dir, filename)

                    if os.path.exists(file_path):
                        tile_im = Image.open(file_path)
                        im.paste(tile_im, (i * res, j * res))
                    else:
                        print('Image not found : %s' % file_path)
                        return

            im.save(self.filepath, 'JPEG')
            # return im
        except Exception as e:
            raise e
        finally:
            return
