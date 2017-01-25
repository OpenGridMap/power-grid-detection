from __future__ import print_function

import os
import sys
import cPickle
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

import config


def read_transnet_powerlines(filename=None, filter_by_regions=True, save):
    if filename is None:
        filename = config.transnet_powerlines_file

    df = pd.read_csv(config.transnet_powerlines_file, delimiter="$", usecols=['country', 'nodes'])

    if filter_by_regions is not False:
        df = filter_df_by_regions(df, filter_by_regions)



def filter_df_by_regions(df, regions='config'):
    if regions is not None:
        if type(regions) is list:
            regions = regions
        elif regions:
            regions = config.regions[config.config_params['loc']]

        return df[df['country'].isin(regions)]

    return df


# regions = config.regions[config.config_params['loc']]
#
# df = pd.read_csv(config.transnet_powerlines_file, delimiter="$", usecols=['country', 'nodes'])
#
# if regions is not None:
#     df = df[df['country'].isin(regions)]
#
# df.to_csv(config.transnet_powerlines_filtered_file, sep=',', encoding='utf-8')
#
# nodes = []
# for row in df['nodes']:
#     nodes += row[1:-1].split(',')
#
# with open(config.transnet_nodes_file, 'wb') as f:
#     cPickle.dump(nodes, f)
