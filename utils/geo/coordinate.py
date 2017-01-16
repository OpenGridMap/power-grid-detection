import math
import mercantile


class Coordinate(object):
    def __init__(self, lat, lon):
        self.lat = lat
        self.lng = lon

    @property
    def latitude(self):
        return self.lat

    @property
    def longitude(self):
        return self.lng

    @property
    def latlng(self):
        return self.lat, self.lng

    def get_tile_coordinates(self, zoom):
        lat_rad = math.radians(self.lat)
        n = 2.0 ** zoom
        x = (self.lng + 180.0) / 360.0 * n
        y = (1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n

        xpixel, xtile = math.modf(x)
        ypixel, ytile = math.modf(y)

        xtile = int(xtile)
        ytile = int(ytile)
        xpixel = int(xpixel * 256)
        ypixel = int(ypixel * 256)

        return xtile, ytile, xpixel, ypixel

    def get_tile(self, zoom=18):
        return mercantile.tile(lat=self.lat, lng=self.lng, zoom=zoom)

    def get_bbox(self, zoom=18):
        tile = self.get_tile(zoom)

        ne = mercantile.bounds(mercantile.tile(*mercantile.ul(tile.x + 1, tile.y + 1, zoom), zoom=zoom))
        sw = mercantile.bounds(mercantile.tile(*mercantile.ul(tile.x - 1, tile.y - 1, zoom), zoom=zoom))

        return sw.west, sw.south, ne.east, ne.north

    def get_tiles(self, zoom=18):
        tile = self.get_tile(zoom)
        x_w = tile.x - 1
        x_e = tile.x + 1
        y_s = tile.y - 1
        y_n = tile.y + 1

        for i in range(x_w, x_e + 1, 1):
            for j in range(y_s, y_n + 1, 1):
                yield i, j, zoom

    def get_negative_tiles(self, zoom=18):
        tile = self.get_tile(zoom)
        w, s, e, n = mercantile.bounds(tile)

        bound_distances = [abs(w - self.lng), abs(s - self.lat), abs(e - self.lng), abs(n - self.lat)]
        min_bound_index = bound_distances.index(min(bound_distances))

        if min_bound_index is 0:
            ignore = tile.x - 1, tile.y
        elif min_bound_index is 1:
            ignore = tile.x, tile.y - 1
        elif min_bound_index is 2:
            ignore = tile.x + 1, tile.y
        elif min_bound_index is 3:
            ignore = tile.x, tile.y + 1

        for x, y, z in self.get_tiles(zoom):
            if tile.x == x and tile.y == y or x == ignore[0] and y == ignore[1]:
                continue

            yield x, y, z

    def get_bbox_tiles(self, zoom=18):
        bbox = self.get_bbox()

        ne = mercantile.tile(*bbox[2:], zoom=zoom)
        sw = mercantile.tile(*bbox[:2], zoom=zoom)

        return ne, sw

    def get_tiles_count(self, zoom=18):
        return 9
        # bbox = self.get_bbox(zoom)
        #
        # ne = mercantile.tile(*bbox[2:], zoom=zoom)
        # sw = mercantile.tile(*bbox[:2], zoom=zoom)
        #
        # print(ne.x - sw.x)
        # print(ne.y - sw.y)
        #
        # return (abs(ne.x - sw.x) + 1) * (abs(ne.y - sw.y) + 1)
    
    def get_crop_box(self, zoom, tile_res=256, crop_size=256, x_crop_offset=0, y_crop_offset=20):
        tile_coord = self.get_tile_coordinates(zoom)
        xpix, ypix = tile_coord[2], tile_coord[3]

        return (
            tile_res + xpix - crop_size / 2. - x_crop_offset,
            tile_res + ypix - crop_size / 2. - y_crop_offset,
            tile_res + xpix + crop_size / 2. - x_crop_offset,
            tile_res + ypix + crop_size / 2. - y_crop_offset
        )
