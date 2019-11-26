import os
from statistics import mean

import redis
from cfpq_redis.utils.server import start_redis_server, stop_redis_server
from cfpq_redis.utils.cfpq_query import cfpq_query
from cfpq_redis.configs.common import Config

ALGO_LIST = ['cpu1', 'cpu3']
MEM_INTERVAL_COUNT = 20


def get_grammar_file(grammar_path):
    return grammar_path.split('/')[-1]


def test_performance_on_graph(graph_name, grammar_path, config: Config, exec_count=1):
    redis_instance = redis.Redis()
    graph_rdb = graph_name.replace('.txt', '.rdb')

    result = {
        algo: {
            column: []
            for column in ['iterations', 'control_sum', 'time', 'rss', 'vms', 'shared']
        } for algo in ALGO_LIST
    }

    for algo in ALGO_LIST:
        for i in range(exec_count):
            start_redis_server(config.redis_bin, config.redis_conf,
                               os.path.join(config.redis_dumps_path, graph_rdb))

            print(f'\t\tGraph: {graph_name}, Iter: {i}/{exec_count}, Algorithm: {algo}')
            resp = cfpq_query(algo, graph_name, grammar_path, redis_instance)

            stop_redis_server()

            result[algo]['iterations'].append(resp.iterations)
            result[algo]['control_sum'].append(resp.control_sums)
            result[algo]['time'].append(resp.time)
            result[algo]['rss'].append(resp.rss)
            result[algo]['vms'].append(resp.vms)
            result[algo]['shared'].append(resp.shared)
    return result


def test_performance_on_suite(test_suite, config: Config, execute_count=10, statistics=(mean, min, max)):
    full_results = {
        'graph': [],
        'grammar': []
    }

    statistics_results = {
        'graph': [],
        'grammar': []
    }

    for graph_name, grammar_path in test_suite:
        res_test = test_performance_on_graph(graph_name, grammar_path, config, exec_count=execute_count)

        full_results['graph'].extend([graph_name] * execute_count)
        full_results['grammar'].extend([get_grammar_file(grammar_path)] * execute_count)

        statistics_results['graph'].append(graph_name)
        statistics_results['grammar'].append(get_grammar_file(grammar_path))

        for algo, execute_info in res_test.items():
            # Write total results
            for column, values in execute_info.items():
                key = f'{column}_{algo}'
                full_results.setdefault(key, [])
                full_results[key].extend(values)

            # Write statistic
            for column in ['control_sum', 'iterations']:
                first_value = execute_info[column][0]
                assert all(x == first_value for x in execute_info[column])

                key = f'{column}_{algo}'
                statistics_results.setdefault(key, [])
                statistics_results[key].append(first_value)

            for column in ['time', 'rss', 'vms', 'shared']:
                for statistic in statistics:
                    key = f'{column}_{statistic.__name__}_{algo}'
                    statistics_results.setdefault(key, [])
                    statistics_results[key].append(statistic(execute_info[column]))

    return full_results, statistics_results
