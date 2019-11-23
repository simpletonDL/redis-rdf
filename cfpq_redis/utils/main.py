from argparse import ArgumentParser

from cfpq_redis.utils.server import load_dumps_suit
from cfpq_redis.test_performance.test_suits import get_suite_names
from cfpq_redis.configs.common import Config


def main():
    parser = ArgumentParser('Load dumps')
    parser.add_argument('suite_name', help='name of test suite',
                        choices=get_suite_names())
    parser.add_argument('--host', help='redis host name', default='localhost')
    parser.add_argument('--port', help='redis port', default=6379)
    parser.add_argument('--out', help='response output dir path', default='results')

    args = parser.parse_args()

    conf = Config('../config.ini')
    load_dumps_suit([args.suite_name], conf)


if __name__ == '__main__':
    main()
