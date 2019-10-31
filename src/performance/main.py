import datetime
import pandas as pd
from src.performance import test_performance_on_suite

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


results = test_performance_on_suite(TEST_SUITE)
results_df = pd.DataFrame(results)

now = datetime.datetime.now().strftime('"%Y-%m-%d_%H:%M"')
results_df.to_csv(f'results/results_{now}.csv')
