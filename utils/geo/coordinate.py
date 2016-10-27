import mercantile


class Coordinate(object):
    BBOX_SIZE = 0.001

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    @property
    def latitude(self):
        return self.lat

    @property
    def longitude(self):
        return self.lon

    def get_bbox(self):
        return self.longitude - Coordinate.BBOX_SIZE, \
               self.latitude - Coordinate.BBOX_SIZE, \
               self.longitude + Coordinate.BBOX_SIZE, \
               self.latitude + Coordinate.BBOX_SIZE

    def get_bbox_tiles(self, zoom_levels):
        return mercantile.tiles(*self.get_bbox(), zooms=zoom_levels)