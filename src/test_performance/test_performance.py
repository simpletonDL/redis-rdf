import time
from statistics import mean
from tqdm import tqdm

from src.utils.mem_prof import MemDeltaProfiler
from src.utils.cfpq_query import cfpq_query


ALGO_LIST = ['cpu1', 'cpu3']
MEM_INTERVAL_COUNT = 20


def get_grammar_file(grammar_path):
    return grammar_path.split('/')[-1]


def test_performance_on_graph(graph_name, grammar_path, redis_instance, exec_count=1):
    result = {
        algo: {
            column: []
            for column in ['iterations', 'control_sum', 'time', 'rss', 'vms', 'shared']
        } for algo in ALGO_LIST
    }

    for algo in ALGO_LIST:
        print(f'\tAlgo: {algo}')
        # Get approximately query time
        # exec_time = cfpq_query(algo, graph_name, grammar_path, redis_instance).time * 1.5
        # exec_time = 1

        # Run exec_count times algorithm
        for i in range(exec_count):
            print(f'\t\tIter: {i}/{exec_count}')
            # mem_prof = MemDeltaProfiler()
            # mem_prof.start(redis_pid, exec_time / MEM_INTERVAL_COUNT, exec_time)
            resp = cfpq_query(algo, graph_name, grammar_path, redis_instance)
            # max_mem = mem_prof.end()

            result[algo]['iterations'].append(resp.iterations)
            result[algo]['control_sum'].append(resp.control_sums)
            result[algo]['time'].append(resp.time)
            result[algo]['rss'].append(resp.rss)
            result[algo]['vms'].append(resp.vms)
            result[algo]['shared'].append(resp.shared)
            # result[algo]['mem'].append(max_mem)
    return result


def test_performance_on_suite(test_suite, redis_instance, execute_count=10, statistics=(mean, min, max)):
    full_results = {
        'graph': [],
        'grammar': []
    }

    statistics_results = {
        'graph': [],
        'grammar': []
    }

    for graph_name, grammar_path in test_suite:
        print(f'Graph: {graph_name}\n')
        res_test = test_performance_on_graph(graph_name, grammar_path, redis_instance, execute_count)

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

            # Write statistics
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
