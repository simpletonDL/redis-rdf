import math

import redis
from statistics import mean, median

from tqdm import tqdm

COMMON_CMD = 'graph.cfg'
ALGO_LIST = ['cpu1', 'cpu3']


def test_performance_on_graph(graph_name, grammar_path, execute_count=1, statistics=(mean,)):
    r = redis.Redis()
    resp_query = [
        [
            [
                s.decode('UTF-8')
                for s in r.execute_command(COMMON_CMD, algo, graph_name, grammar_path)
            ]
            for _ in range(execute_count)
        ]
        for algo in ALGO_LIST
    ]
    result = {
        algo: {
            column: None
            for column in ['iterations', 'control_sum', 'time'] + [statistic.__name__ for statistic in statistics]
        } for algo in ALGO_LIST
    }

    def get_iterations(resp):
        return resp[1].split()[-1]

    def get_control_sum(resp):
        return ', '.join(resp[2:])

    def get_time(resp):
        return float(resp[0].split()[-1])

    for algo, responses in zip(ALGO_LIST, resp_query):
        control_sum = get_control_sum(responses[0])
        assert all(get_control_sum(response) == control_sum for response in responses)
        result[algo]['control_sum'] = control_sum

        iterations = get_iterations(responses[0])
        assert all(get_iterations(response) == iterations for response in responses)
        result[algo]['iterations'] = iterations

        for statistic in statistics:
            result[algo][statistic.__name__] = statistic([get_time(response) for response in responses])

    return result


def test_performance_on_suite(test_suite, execute_count=10, statistics=(mean, min, max)):
    total_results = {
        'graph': [],
        'grammar': []
    }
    for graph_name, grammar_path in tqdm(test_suite):
        total_results['graph'].append(graph_name)
        total_results['grammar'].append(grammar_path.split('/')[-1])

        res_test = test_performance_on_graph(graph_name, grammar_path, execute_count, statistics)
        for algo, execute_info in res_test.items():
            for column, value in execute_info.items():
                key = f'{column}_{algo}'
                total_results.setdefault(key, [])
                total_results[key].append(value)
    return total_results
