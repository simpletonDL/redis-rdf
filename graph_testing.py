import hashlib
from pprint import pprint

import pandas as pd

import redis

COMMON_CMD = 'graph.cfg'
ALGO_LIST = ['cpu1', 'cpu3']

RDF_GRAMMAR_PATH = '/home/jblab/CFPQ-with-RedisGraph/CFPQ_Data/data/graphs/RDF/Grammars'
WS_GRAMMAR_PATH = '/home/jblab/CFPQ-with-RedisGraph/CFPQ_Data/data/graphs/WorstCase/Grammars/Brackets.txt'

TEST_SUITE = [
    ('geospeices.txt', f'{RDF_GRAMMAR_PATH}/geo.cnf'),
    ('go.txt', f'{RDF_GRAMMAR_PATH}/GPPerf1_cnf.txt'),
    ('go-hierarchy.txt', f'{RDF_GRAMMAR_PATH}/GPPerf1_cnf.txt'),
    ('eclass_514en.txt', f'{RDF_GRAMMAR_PATH}/GPPerf1_cnf.txt'),
    ('enzyme.txt', f'{RDF_GRAMMAR_PATH}/GPPerf1_cnf.txt'),
    ('atom-primitive.txt', f'{RDF_GRAMMAR_PATH}/GPPerf1_cnf.txt'),
    ('funding.txt', f'{RDF_GRAMMAR_PATH}/GPPerf1_cnf.txt'),
    ('people_pets.txt', f'{RDF_GRAMMAR_PATH}/GPPerf1_cnf.txt'),
    ('wine.txt', f'{RDF_GRAMMAR_PATH}/GPPerf1_cnf.txt'),
    ('biomedical-mesure-primitive.txt', f'{RDF_GRAMMAR_PATH}/GPPerf1_cnf.txt'),
    ('generations.txt', f'{RDF_GRAMMAR_PATH}/GPPerf1_cnf.txt'),
    ('pizza.txt', f'{RDF_GRAMMAR_PATH}/GPPerf1_cnf.txt'),
    ('travel.txt', f'{RDF_GRAMMAR_PATH}/GPPerf1_cnf.txt'),
    ('core.txt', f'{RDF_GRAMMAR_PATH}/GPPerf1_cnf.txt'),
    ('foaf.txt', f'{RDF_GRAMMAR_PATH}/GPPerf1_cnf.txt'),
    ('pathways.txt', f'{RDF_GRAMMAR_PATH}/GPPerf1_cnf.txt'),
    ('skos.txt', f'{RDF_GRAMMAR_PATH}/GPPerf1_cnf.txt'),
    ('univ-bench.txt', f'{RDF_GRAMMAR_PATH}/GPPerf1_cnf.txt'),
    ('worstcase_4.txt', WS_GRAMMAR_PATH),
    ('worstcase_8.txt', WS_GRAMMAR_PATH),
    ('worstcase_16.txt', WS_GRAMMAR_PATH),
    ('worstcase_32.txt', WS_GRAMMAR_PATH),
    ('worstcase_64.txt', WS_GRAMMAR_PATH),
    ('worstcase_128.txt', WS_GRAMMAR_PATH),
    ('worstcase_256.txt', WS_GRAMMAR_PATH),
    ('worstcase_512.txt', WS_GRAMMAR_PATH)
]

r = redis.Redis()


def test_performance_on_graph(graph_name, grammar_path):
    print(f'Test {graph_name}')
    res_query = [
        [s.decode('UTF-8')
         for s in r.execute_command(COMMON_CMD, algo, graph_name, grammar_path)]
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


def test_performance():
    total_res = {
        'name': [],
        'grammar': []
    }
    for graph_name, grammar_path in TEST_SUITE:
        res_test = test_performance_on_graph(graph_name, grammar_path)
        for column in['iterations', 'control_sum', 'time']:
            for value, algo in zip(res_test[column], ALGO_LIST):
                key = f'{column}_{algo}'
                total_res.setdefault(key, [])
                total_res[key].append(value)
        total_res['name'].append(graph_name)
        total_res['grammar'].append(grammar_path.split('/')[-1])
    return total_res


xs = test_performance()
pprint(xs, indent=4)
ys = pd.DataFrame(xs)
ys.to_csv('test_results.csv')
print(ys)
