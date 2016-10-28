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

    def get_bbox(self, zoom=18):
        tile = mercantile.tile(lat=self.lat, lng=self.lng, zoom=zoom)

        ne = mercantile.bounds(mercantile.tile(*mercantile.ul(tile.x + 1, tile.y + 1, zoom), zoom=zoom))
        sw = mercantile.bounds(mercantile.tile(*mercantile.ul(tile.x - 1, tile.y - 1, zoom), zoom=zoom))

        return sw.west, sw.south, ne.east, ne.north

    def get_tiles(self, zoom=18):
        tile = mercantile.tile(lat=self.lat, lng=self.lng, zoom=zoom)
        x_w = tile.x - 1
        x_e = tile.x + 1
        y_s = tile.y - 1
        y_n = tile.y + 1

        # tiles = []

        # for i in range(3):
        #     for j in range(3):
        #         tile = mercantile.tile(*mercantile.ul(i + x_w, j + y_s, zoom), zoom=zoom)
                # tile = i + x_w, j + y_s, zoom
                # tiles.append(tile)

        for i in range(x_w, x_e + 1, 1):
            for j in range(y_s, y_n + 1, 1):
                yield i, j, zoom
        #         tile = mercantile.tile(*mercantile.ul(i, j, zoom), zoom=zoom)
        #         tiles.append(tile)

        # return tiles
        # return mercantile.tiles(*self.get_bbox(zoom), zooms=[zoom])

    def get_bbox_tiles(self, zoom=18):
        bbox = self.get_bbox()

        ne = mercantile.tile(*bbox[2:], zoom=zoom)
        sw = mercantile.tile(*bbox[:2], zoom=zoom)

        return ne, sw

    def get_tiles_count(self, zoom=18):
        return 9
        bbox = self.get_bbox(zoom)

        ne = mercantile.tile(*bbox[2:], zoom=zoom)
        sw = mercantile.tile(*bbox[:2], zoom=zoom)

        # print(ne.x - sw.x)
        # print(ne.y - sw.y)

        return (abs(ne.x - sw.x) + 1) * (abs(ne.y - sw.y) + 1)
