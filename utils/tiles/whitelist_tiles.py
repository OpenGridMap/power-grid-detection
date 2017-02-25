import os
import glob
import json

import config

files = glob.glob1(config.affixed_tiles_dir, '*.jpg')

print(len(files))

path = os.path.join(config.dataset_dir, 'tiles_whitelist.json')

with open(path, 'wb') as f:
    json.dump(files, f, sort_keys=True, indent=4)
    f.flush()
