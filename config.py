import yaml
import os
import sys

sys.path.append(os.path.dirname(__file__))

config_file_path = os.path.join(os.path.dirname(__file__), './config.yaml')

with open(config_file_path, 'r') as f:
    config_params = yaml.load(f)

project_dir = os.path.join(os.path.dirname(__file__))
data_src_dir = os.path.join(project_dir, 'data')

positive_samples_src_dir = os.path.join(data_src_dir, 'cache', 'digital-globe', '1x', '256')
negative_samples_src_dir = os.path.join(data_src_dir, 'cache', 'arcgis-online', 'negative', '256')

dataset_dir = os.path.join(project_dir, 'dataset')

transnet_powerlines_file = os.path.join(project_dir, config_params['transnet-powerlines-csv'])
transnet_powerlines_filtered_file = os.path.join(data_src_dir, 'transnet',
                                                 'transnet_powerlines_' + config_params['loc'] + '.csv')
transnet_nodes_file = os.path.join(data_src_dir, 'transnet', 'transnet_nodes.pkl')
nodes = os.path.join(dataset_dir, 'transnet_nodes_' + config_params['loc'] + '.csv')

cache_dir = os.path.join(os.path.dirname(__file__), 'data', 'cache')
# tiles_cache_dir = os.path.join(cache_dir, 'arcgis-online', 'tiles')
affixed_tiles_dir = os.path.join(cache_dir, config_params['tiles-scraper'], '3x3_tiles')
preprocessed_tiles_dir = os.path.join(cache_dir, config_params['tiles-scraper'], 'preprocessed_3x3_tiles')
cropped_images_dir = os.path.join(data_src_dir, 'raw', 'cropped')

gen_dataset_dir = os.path.join(dataset_dir, 'raw')
final_dataset_dir = os.path.join(dataset_dir, 'processed')

positive_samples_dir = os.path.join(dataset_dir, 'raw', 'positive')
negative_samples_dir = os.path.join(dataset_dir, 'raw', 'negative')
processed_positive_samples_dir = os.path.join(final_dataset_dir, 'positive')
processed_negative_samples_dir = os.path.join(final_dataset_dir, 'negative')


annotations_file = os.path.join(dataset_dir, 'annotations.json')
current_annotations_file = os.path.join(dataset_dir, 'annotations-v4.json')

data_file = os.path.join(dataset_dir, 'data.csv')
train_data_file = os.path.join(dataset_dir, 'train_data.csv')
validation_data_file = os.path.join(dataset_dir, 'validation_data.csv')
test_data_file = os.path.join(dataset_dir, 'test_data.csv')

germany = [
    'bayern',
    'nordrhein-westfalen',
    'niedersachsen',
    'bremen',
    'sachsen-anhalt',
    'hessen',
    'sachsen',
    'hamburg',
    'saarland',
    'berlin',
    'baden-wuerttemberg',
    'thueringen',
    'rheinland-pfalz',
    'schleswig-holstein',
    'mecklenburg-vorpommern',
    'brandenburg'
]

europe = [
     'netherlands',
     'italy',
     'france',
     'poland',
     'switzerland',
     'latvia',
     'great-britain',
     'belarus',
     'spain',
     'finland',
     'bulgaria',
     'ireland-and-northern-ireland',
     'portugal',
     'ukraine',
     'czech-republic',
     'belgium',
     'volga-fed-district',
     'serbia',
     'moldova',
     'hungary',
     'lithuania',
     'norway',
     'denmark',
     'sweden',
     'estonia',
     'slovakia',
     'bosnia-herzegovina',
     'greece',
     'austria',
     'iceland',
     'croatia',
     'luxembourg',
     'slovenia',
     'romania'
 ] + germany

regions = {
    'germany': germany,
    'europe': europe
}

proxies = {
    'http': 'socks5://127.0.0.1:9150',
    'https': 'socks5://127.0.0.1:9150'
}

