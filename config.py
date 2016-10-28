import yaml
import os
import sys

sys.path.append(os.path.dirname(__file__))

config_file_path = os.path.join(os.path.dirname(__file__), './config.yaml')

with open(config_file_path, 'r') as f:
    config = yaml.load(f)
