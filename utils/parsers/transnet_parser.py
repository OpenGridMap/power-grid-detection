import os
import pandas as pd
import numpy as np

import config


class TransnetParser:
    def __init__(self, filename=None):
        if filename is None:
            filename = config.transnet_powerlines_file

        cols = ['osm_id', 'country', 'tags', 'voltage', 'lat', 'lon', 'length', 'nodes']
        self.df = pd.read_csv(filename, delimiter="$", index_col='osm_id', usecols=cols)

    def filter_by_regions(self, regions='config'):
        if regions is not None:
            if regions is 'config':
                regions = config.regions[config.config_params['loc']]
            elif type(regions) is list:
                pass
            else:
                return

            self.df = self.df[self.df['country'].isin(regions)]

    def filter_by_voltages(self, voltages):
        df = None

        for v in voltages:
            df_v = self.df['voltage'].str.contains(str(v))

            if df is None:
                df = df_v
            else:
                df |= df_v

        self.df = self.df[df]

    def filter_by_min_max_voltage(self, min_voltage=None, max_voltage=None):
        voltages = self.voltages
        filtered_voltages = None

        if min_voltage is not None:
            filtered_voltages = voltages['voltage'] >= min_voltage

        if max_voltage is not None:
            vs = voltages['voltage'] <= max_voltage

            if filtered_voltages is None:
                filtered_voltages = vs
            else:
                filtered_voltages &= vs

        if filtered_voltages is not None:
            voltages = voltages[filtered_voltages]
            voltages = voltages.values.reshape((voltages.shape[0], ))

            self.filter_by_voltages(voltages)

    @property
    def data(self):
        return self.df

    @property
    def nodes(self):
        nodes = []
        for row in self.df['nodes']:
            nodes += row[1:-1].split(',')

        return nodes

    @property
    def voltages(self):
        filtered_voltages = []
        voltages = self.df['voltage'].unique()

        for v in voltages:
            filtered_voltages += v[1:-1].split(',')

        filtered_voltages = np.unique(np.asarray(filtered_voltages, dtype=int))
        filtered_voltages = pd.DataFrame(filtered_voltages, columns=['voltage'], dtype=int)

        return filtered_voltages


# if __name__ == '__main__':
#     t = TransnetParser()
#     t.filter_by_regions()
    # t.filter_by_voltages([380000])
    # t.filter_by_min_max_voltage(min_voltage=220000, max_voltage=380000)
    # print(t.data.info())
    # print(len(t.nodes))
    # voltages = []
    # vs = t.data['voltage'].unique()
    # for v in vs:
    #     v = v[1:-1]
    #     vss = v.split(',')
    #     voltages += vss
    #
    # # voltages = map(int, voltages)
    # # voltages = set(voltages)
    # # print(len(voltages))
    #
    # df = pd.DataFrame(voltages, columns=['voltage'], dtype=int)
    # # df = df['voltage'].unique()
    #
    # print(df.shape)
    #
    # # df = pd.DataFrame(voltages, dtype=int)
    # # df = df.rename(columns={0: 'voltage'})
    # # print(voltages)
    # # print(df['voltage'].unique().shape)
    #
    # df = df['voltage'][df['voltage'] > 370000].unique()
    # print(df.shape)
    # t.filter_by_voltage(df)
    # print(len(t.nodes))
    #
    #
