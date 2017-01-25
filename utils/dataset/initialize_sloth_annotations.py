import os
import json
import glob
import pandas as pd

import config

from utils.geo.coordinate import Coordinate

annotations_file = config.annotations_file

if os.path.exists(annotations_file):
    print('File already exists')

annotations = []

# files = glob.iglob(config.affixed_tiles_dir + '/*.jpg')
nodes = pd.read_csv(config.nodes, index_col=0, nrows=30000)

for node in nodes.iterrows():
    coord = Coordinate(lat=node[1]['lat'], lon=node[1]['lon'])
    path = os.path.join(config.affixed_tiles_dir, str(int(node[1]['osm_id'])) + '.jpg')

    if os.path.exists(path):
        crop_res = 180.
        crop_box = coord.get_crop_box(zoom=18, crop_size=crop_res, x_crop_offset=0, y_crop_offset=48)
        tile_coordinates = coord.get_tile_coordinates(zoom=18)
        properties = {
            'annotations': [
                {
                    "class": "tower",
                    "type": "rect",
                    "height": crop_res,
                    "width": crop_res,
                    "x": crop_box[0],
                    "y": crop_box[1]
                },
                # {
                #     "class": "tower-osm-base",
                #     "type": "point",
                #     "x": tile_coordinates[2] + crop_res,
                #     "y": tile_coordinates[3] + crop_res
                # }
            ],
            'class': 'image',
            'filename': os.path.abspath(path)
        }
        annotations.append(properties)

# for f in files:
    # properties = {
    #     'annotations': [],
    #     'class': 'image',
    #     'filename': os.path.abspath(f)
    # }
    # annotations.append(properties)


with open(annotations_file, 'wb') as f:
    json.dump(annotations, f, sort_keys=True, indent=4)
    f.flush()
