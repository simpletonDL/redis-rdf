import os
from argparse import ArgumentParser

from cfpq_redis.utils.server import load_dumps, load_dump
from cfpq_redis.test_performance.test_suits import get_suite_names
from cfpq_redis.configs.common import Config


def main():
    parser = ArgumentParser('Load dumps')
    parser.add_argument('suite_name', help='name of test suite',
                        choices=get_suite_names())
    parser.add_argument('--file', action='append', required=False, help='Specify files of suit')
    parser.add_argument('--host', help='redis host name', default='localhost')
    parser.add_argument('--port', help='redis port', default=6379)

    args = parser.parse_args()

    conf = Config('../config.ini')

    if 'file' in args:
        for file in args.file:
            graph_path = os.path.join(conf.cfpq_data_path, 'data', 'graphs', args.suite_name, 'Matrices', file)
            load_dump(graph_path, conf, args.port, args.host)
    else:
        load_dumps([args.suite_name], conf, args.port, args.host)


if __name__ == '__main__':
    main()
