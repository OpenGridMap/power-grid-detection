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

    @staticmethod
    def get_coordinates_from_tile_coordinates(xtile, ytile, xpixel, ypixel, zoom):
        xtile += xpixel / 256.
        ytile += ypixel / 256.

        n = 2.0 ** zoom
        lng = xtile / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
        lat = math.degrees(lat_rad)

        return lat, lng

    def get_tile(self, zoom=18):
        return mercantile.tile(lat=self.lat, lng=self.lng, zoom=zoom)

    def get_bbox(self, zoom=18):
        tile = self.get_tile(zoom)

        ne = mercantile.bounds(mercantile.tile(*mercantile.ul(tile.x + 1, tile.y + 1, zoom), zoom=zoom))
        sw = mercantile.bounds(mercantile.tile(*mercantile.ul(tile.x - 1, tile.y - 1, zoom), zoom=zoom))

        return sw.west, sw.south, ne.east, ne.north

    def get_tiles(self, zoom=18):
        tile = self.get_tile(zoom)
        n = int(self.get_tiles_count(zoom)[0] / 2)

        x_w = tile.x - n
        x_e = tile.x + n
        y_s = tile.y - n
        y_n = tile.y + n

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

    @staticmethod
    def get_tiles_count(zoom=18):
        if zoom > 19:
            return 5, 5

        return 3, 3
        # bbox = self.get_bbox(zoom)
        #
        # ne = mercantile.tile(*bbox[2:], zoom=zoom)
        # sw = mercantile.tile(*bbox[:2], zoom=zoom)
        #
        # print(ne.x - sw.x)
        # print(ne.y - sw.y)
        #
        # return (abs(ne.x - sw.x) + 1) * (abs(ne.y - sw.y) + 1)
    
    def get_crop_box(self, zoom, tile_res=256, crop_size=(256, 256), crop_x_offset=0, crop_y_offset=20):
        tile_coord = self.get_tile_coordinates(zoom)
        xpix, ypix = tile_coord[2], tile_coord[3]
        tiles_shape = self.get_tiles_count(zoom)

        tile_x_offset = int(tiles_shape[0] / 2)
        tile_y_offset = int(tiles_shape[1] / 2)

        return (
            tile_x_offset * tile_res + xpix - crop_size[0] / 2. - crop_x_offset,
            tile_y_offset * tile_res + ypix - crop_size[1] / 2. - crop_y_offset,
            tile_x_offset * tile_res + xpix + crop_size[0] / 2. - crop_x_offset,
            tile_y_offset * tile_res + ypix + crop_size[1] / 2. - crop_y_offset
        )

    def get_transnet_node(self, osm_id=None):
        if osm_id is not None:
            osm_id = str(int(osm_id))

        return dict(lat=self.lat, lon=self.lng, node=osm_id)

    @classmethod
    def from_transnet_node(cls, node):
        return cls(lat=node[1]['lat'], lon=node[1]['lon'])

    @classmethod
    def from_rect(cls, rect, tile):
        xtile, ytile, zoom = tile
        xpixel, ypixel, width, height = rect

        x_offset, y_offset = Coordinate.get_tiles_count(zoom)
        x_offset = int(x_offset / 2)
        y_offset = int(y_offset / 2)

        xpixel += width / 2
        ypixel += height / 2
        xtile += (xpixel / 256) - x_offset
        ytile += (ypixel / 256) - y_offset

        xpixel %= 256
        ypixel %= 256

        latlng = Coordinate.get_coordinates_from_tile_coordinates(xtile, ytile, xpixel, ypixel, zoom)

        return cls(*latlng)


class AreaCoordinates(object):
    def __init__(self, top_left_coord, bottom_right_coord):
        self.top_left_coord = top_left_coord
        self.bottom_right_coord = bottom_right_coord

    def get_tiles(self, zoom=18):
        top_left_tile = self.top_left_coord.get_tile(zoom)
        bottom_right_tile = self.bottom_right_coord.get_tile(zoom)

        for i in range(top_left_tile.x, bottom_right_tile.x + 1, 1):
            for j in range(top_left_tile.y, bottom_right_tile.y + 1, 1):
                yield i, j, zoom

    def get_tiles_count(self, zoom=18):
        top_left_tile = self.top_left_coord.get_tile(zoom)
        bottom_right_tile = self.bottom_right_coord.get_tile(zoom)

        return abs(bottom_right_tile.x - top_left_tile.x + 1) * abs(top_left_tile.y - bottom_right_tile.y + 1)

    # @property
    # def top(self):
    #     return self.top_left_coord.y
    #
    # @property
    # def bottom(self):
    #     return self.bottom_right_coord.y
    #
    # @property
    # def left(self):
    #     return self.top_left_coord.x
    #
    # @property
    # def right(self):
    #     return self.bottom_right_coord.x
