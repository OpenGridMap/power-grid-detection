import yaml
import os
import sys

sys.path.append(os.path.dirname(__file__))

config_file_path = os.path.join(os.path.dirname(__file__), './config.yaml')

with open(config_file_path, 'r') as f:
    config = yaml.load(f)

project_dir = os.path.join(os.path.dirname(__file__))

positive_samples_src_dir = os.path.join(project_dir, 'data', 'cache', 'digital-globe', '1x', '256')
negative_samples_src_dir = os.path.join(project_dir, 'data', 'cache', 'arcgis-online', 'negative', '256')

dataset_dir = os.path.join(project_dir, 'dataset')
# positive_samples_dir = os.path.join(dataset_dir, 'positive')
# negative_samples_dir = os.path.join(dataset_dir, 'negative')
