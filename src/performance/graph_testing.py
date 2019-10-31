import redis

COMMON_CMD = 'graph.cfg'
ALGO_LIST = ['cpu1', 'cpu3']


def test_performance_on_graph(graph_name, grammar_path):
    r = redis.Redis()

    print(f'Test {graph_name}')
    res_query = [
        [
            s.decode('UTF-8')
            for s in r.execute_command(COMMON_CMD, algo, graph_name, grammar_path)
        ]
        for algo in ALGO_LIST
    ]
    res_dict = {
        'iterations': [],
        'control_sum': [],
        'time': []
    }

    for algo, res in zip(ALGO_LIST, res_query):
        res_dict['iterations'].append(res[1].split()[-1])
        res_dict['control_sum'].append(", ".join(res[2:]))
        res_dict['time'].append(res[0].split()[-1])

    return res_dict


def test_performance_on_suite(test_suite):
    total_res = {
        'name': [],
        'grammar': []
    }
    for graph_name, grammar_path in test_suite:
        res_test = test_performance_on_graph(graph_name, grammar_path)
        for column in['iterations', 'control_sum', 'time']:
            for value, algo in zip(res_test[column], ALGO_LIST):
                key = f'{column}_{algo}'
                total_res.setdefault(key, [])
                total_res[key].append(value)
        total_res['name'].append(graph_name)
        total_res['grammar'].append(grammar_path.split('/')[-1])
    return total_res
