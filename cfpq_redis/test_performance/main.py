#!/usr/bin/python3

import datetime
import os
from argparse import ArgumentParser
from cfpq_redis.configs.common import Config

import pandas as pd
import redis
from cfpq_redis.test_performance.test_performance import test_performance_on_suite
from cfpq_redis.test_performance.test_suits import get_total_cases, get_suite_cases, get_suits_names, get_additional_cases

FULL = 'full'
ADDITIONAL = 'additional'


def main():
    # Parse args
    parser = ArgumentParser('Launch tests query suits')
    parser.add_argument('test_suite_name', help='name of test suite',
                        choices=get_suits_names() + [FULL, ADDITIONAL], default='FULL')
    parser.add_argument('--host', help='redis host name', default='localhost')
    parser.add_argument('--port', help='redis port', default=6379)
    parser.add_argument('--out', help='response output dir path', default='results')

    args = parser.parse_args()

    # Load config
    config = Config('../config.ini')

    # Get suits
    test_suite_name = args.test_suite_name
    if test_suite_name == FULL:
        test_cases = get_total_cases()
    elif test_suite_name == ADDITIONAL:
        test_cases = get_additional_cases()
    else:
        test_cases = get_suite_cases(test_suite_name)

    # Run test performance
    full_results, statistic_results = test_performance_on_suite(test_cases, config, execute_count=4)

    # Write results
    statistic_results_df = pd.DataFrame(statistic_results)
    full_results_df = pd.DataFrame(full_results)

    now = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')
    path_result = f'results/{args.test_suite_name}'
    if not os.path.isdir(path_result):
        os.mkdir(path_result)

    full_results_df.to_csv(f'{path_result}/{now}_full.csv')
    statistic_results_df.to_csv(f'{path_result}/{now}_statistic.csv')


if __name__ == '__main__':
    main()
