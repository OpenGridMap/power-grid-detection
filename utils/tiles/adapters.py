import os
import config


def get_adapter(adapter=None, files_dir=None):
    return get_adapter_class(adapter)(files_dir)


def get_adapter_class(adapter=None):
    if adapter is None:
        adapter = config.config_params['tiles-scraper']

    if adapter == ArcgisOnlineAdapter.NAME:
        return ArcgisOnlineAdapter
    elif adapter == GoogleMapsAdapter.NAME:
        return GoogleMapsAdapter
    else:
        raise ValueError


class MercatorTilesAdapter(object):
    TILE_FILENAME_FORMAT = "{}_{}_{}.jpg"
    TILE_RESOLUTION = 256

    def __init__(self, adapter, files_dir=None):
        if files_dir is None:
            files_dir = config.cache_dir

        self.files_dir = os.path.join(files_dir, adapter, 'tiles')

        if not os.path.exists(self.files_dir):
            os.makedirs(self.files_dir)

    @staticmethod
    def get_filename(tile):
        # return "{}_{}_{}.jpg".format(tile.x, tile.y, tile.z)
        return MercatorTilesAdapter.TILE_FILENAME_FORMAT.format(*tile)

    def get_filepath(self, tile):
        return os.path.join(self.files_dir, self.get_filename(tile))

    def get_url(self):
        raise NotImplementedError

    @staticmethod
    def get_res():
        return MercatorTilesAdapter.TILE_RESOLUTION


class ArcgisOnlineAdapter(MercatorTilesAdapter):
    NAME = 'arcgis-online'
    BASE_URL = 'http://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{}/{}/{}'

    def __init__(self, files_dir=None):
        super(ArcgisOnlineAdapter, self).__init__(self.NAME, files_dir)

    @staticmethod
    def get_url(tile):
        return ArcgisOnlineAdapter.BASE_URL.format(tile[2], tile[1], tile[0])


class GoogleMapsAdapter(MercatorTilesAdapter):
    NAME = 'google-maps'
    BASE_URL = 'https://khms1.googleapis.com/kh?v=713&hl=en-US&&x={}&y={}&z={}'

    def __init__(self, files_dir=None):
        super(GoogleMapsAdapter, self).__init__(self.NAME, files_dir)

    @staticmethod
    def get_url(tile):
        return GoogleMapsAdapter.BASE_URL.format(*tile)
