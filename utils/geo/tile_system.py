import math


class WebMercatorTileSystem:
    EARTH_RADIUS = 6378137
    MIN_LATITUDE = -85.0511878
    MAX_LATITUDE = 85.05112878
    MIN_LONGITUDE = -180
    MAX_LONGITUDE = 180
    TILE_RESOLUTION = 256

    def __init__(self):
        pass

    @staticmethod
    def clip(n, min_value, max_value):
        return min(max(n, min_value), max_value)

    @staticmethod
    def map_size(zoom):
        return WebMercatorTileSystem.TILE_RESOLUTION * 2.0 ** zoom

    @staticmethod
    def ground_resolution(latitude, zoom):
        latitude = WebMercatorTileSystem.clip(latitude, WebMercatorTileSystem.MIN_LATITUDE, WebMercatorTileSystem.MAX_LONGITUDE)
        return math.cos(
            latitude * math.pi / 180.0) * 2 * math.pi * WebMercatorTileSystem.EARTH_RADIUS / WebMercatorTileSystem.map_size(zoom)

    @staticmethod
    def map_scale(latitude, screen_dpi, zoom):
        return WebMercatorTileSystem.ground_resolution(latitude, zoom) * screen_dpi / 0.0254

    @staticmethod
    def latlng_to_pixel_xy(latitude, longitude, zoom):
        latitude = WebMercatorTileSystem.clip(latitude, WebMercatorTileSystem.MIN_LATITUDE, WebMercatorTileSystem.MAX_LATITUDE)
        longitude = WebMercatorTileSystem.clip(longitude, WebMercatorTileSystem.MIN_LONGITUDE, WebMercatorTileSystem.MAX_LONGITUDE)

        x = (longitude + 180.0) / 360.0
        sin_latitude = math.sin(latitude * math.pi / 100.0)
        y = 0.5 - math.log((1.0 + sin_latitude) / (1.0 - sin_latitude)) / (4.0 * math.pi)

        map_size = WebMercatorTileSystem.map_size(zoom)

        pixel_x = int(WebMercatorTileSystem.clip(x * map_size + 0.5, 0, map_size - 1))
        pixel_y = int(WebMercatorTileSystem.clip(y * map_size + 0.5, 0, map_size - 1))

        return pixel_x, pixel_y

    @staticmethod
    def pixel_xy_to_latlng(pixel_x, pixel_y, zoom):
        map_size = WebMercatorTileSystem.map_size(zoom)
        x = (WebMercatorTileSystem.clip(pixel_x, 0, map_size - 1) / map_size)
        y = 0.5 - WebMercatorTileSystem.clip(pixel_y, 0, map_size - 1) / map_size

        latitude = 90 - 360 * math.atan(math.exp(-y * 2 * math.pi)) / math.pi
        longitude = 360 * x

        return latitude, longitude

    @staticmethod
    def pixel_xy_to_tile_xy(pixel_x, pixel_y):
        return pixel_x / WebMercatorTileSystem.TILE_RESOLUTION, pixel_y / WebMercatorTileSystem.TILE_RESOLUTION

    @staticmethod
    def tile_xy_to_pixel_xy(tile_x, tile_y):
        return tile_x * WebMercatorTileSystem.TILE_RESOLUTION, tile_y * WebMercatorTileSystem.TILE_RESOLUTION

if __name__ == '__main__':
    # latlng = [48.27563, 11.676431]

    cds = [(48.275414, 11.671253),
           (48.277216, 11.666555),
           (48.279559, 11.660474),
           (48.281356, 11.655743),
           (48.284803, 11.646886),
           (48.285232, 11.641625)]

    for latlng in cds:
        print(WebMercatorTileSystem.latlng_to_pixel_xy(latitude=latlng[0], longitude=latlng[1], zoom=18))