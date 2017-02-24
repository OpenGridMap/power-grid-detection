import pandas as pd

import config


def to_csv(nodes, filepath=None):
    if filepath is None:
        filepath = config.nodes

    df = pd.DataFrame(nodes)
    # print(df.head())
    df.to_csv(filepath, sep=',')

    return df.shape[0]


def get_nodes_df(filename=None, n=None):
    if filename is None:
        filename = config.nodes
    nodes = pd.read_csv(filename, index_col=0, nrows=n)
    return nodes, nodes.shape[0]

