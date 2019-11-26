import os

import pandas as pd
import numpy as np
from cfpq_redis.configs.common import Config


def get_results():
    results = []
    for suite in os.listdir('results'):
        for file in filter(lambda x: 'statistic' in x, os.listdir(os.path.join('results', suite))):
            df = pd.read_csv(os.path.join('results', suite, file))
            common_res = df[['graph', 'grammar', 'time_mean_cpu1', 'rss_max_cpu1']]
            if 'time_mean_cpu3' in df.columns and 'rss_max_cpu3' in df.columns:
                common_res['time_mean_cpu3'] = df['time_mean_cpu3']
                common_res['rss_max_cpu3'] = df['rss_max_cpu3']
            else:
                common_res['time_mean_cpu3'] = ""
                common_res['rss_max_cpu3'] = ""

            common_res['suite'] = suite
            results.append(common_res)
    return pd.concat(results)


def get_result_2():
    df_stat = pd.read_csv('../statistics/results/statistics.csv')

    for suite in os.listdir('results'):
        results = []
        for file in filter(lambda x: 'statistic' in x, os.listdir(os.path.join('results', suite))):
            df = pd.read_csv(os.path.join('results', suite, file))

            result = pd.DataFrame()
            grammars = set(df['grammar'])
            for grammar in grammars:
                df_gr = df[df['grammar'] == grammar]

                if 'graph' in result.columns:
                    assert all(result['graph'].values == df_gr['graph'].values)

                result['graph'] = df_gr['graph'].values
                result[f'{grammar}_time'] = df_gr['time_mean_cpu1'].values
                result[f'{grammar}_memory'] = df_gr['rss_max_cpu1'].values
                result[f'{grammar}_iters'] = df_gr['iterations_cpu1'].values

            result = result.set_index('graph').merge(df_stat.set_index('graph'), how='left', on='graph')
            results.append(result)

        pd.concat(results).to_csv(os.path.join('union_results', f'{suite}.csv'))


get_result_2()
