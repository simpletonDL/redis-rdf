import os
from typing import List
from cfpq_redis.configs.common import Config

CONFIG = Config('../config.ini')


def _get_grammar_path(cfpq_data: str, suite: str, grammar: str):
    return os.path.join(cfpq_data, 'data', 'graphs', suite, 'Grammars', grammar)


def get_additional_cases():
    return [
        ('geospeices.txt', _get_grammar_path(CONFIG.cfpq_data_path, 'RDF', 'geo.cnf'))
    ]


def get_suits_names():
    suits_path = os.path.join(CONFIG.cfpq_data_path, 'data', 'graphs')
    return os.listdir(suits_path)


def get_grammar_cases():
    return {
        'SG_1': ['SG.yrd'],
        'SG_2': ['SG.yrd'],
        'FreeScale': ['an_bm_cm_dn.txt'],
        'FullGraph': ['A_star0.yrd', 'A_star1.yrd', 'A_star2.yrd'],
        'RDF': ['GPPerf1_cnf.txt', 'GPPerf2_cnf.txt', 'geo.cnf'],
        'MemoryAliases': ['mayAlias.yrd'],
        'WorstCase': ['Brackets.txt']
    }


def get_graph_cases():
    suites_dir = os.path.join(CONFIG.cfpq_data_path, 'data', 'graphs')

    g_test_suits = {}
    for g_file in get_suits_names():
        g_test_suits[g_file] = [g for g in os.listdir(os.path.join(suites_dir, g_file, 'Matrices'))
                                if not g.startswith('.')]
    return g_test_suits


def _get_suits_cases(suits: List[str]):
    graph_cases = get_graph_cases()
    grammar_cases = get_grammar_cases()

    return sum([
        sorted([(graph_case, _get_grammar_path(CONFIG.cfpq_data_path, suite, grammar_case))
                for graph_case in graph_cases[suite]
                for grammar_case in grammar_cases[suite]],
               key=lambda case: (case[1], case[0]))
        for suite in suits], [])


def get_suite_cases(suite: str):
    return _get_suits_cases([suite])


def get_total_cases():
    return get_additional_cases() + _get_suits_cases(get_suits_names())
