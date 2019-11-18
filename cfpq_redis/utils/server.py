import time
from configparser import ConfigParser
from cfpq_redis.redis_loader.loader import load
from cfpq_redis.configs.common import Config
import os
from shutil import copyfile
import redis


def start_redis_server(bin_path, redis_conf_path, dump_path=None, port=6379):
    if dump_path:
        copyfile(dump_path, 'dump.rdb')

    os.spawnvpe(os.P_NOWAIT, bin_path, [bin_path, redis_conf_path, '--port', str(port)], os.environ)

    r = redis.Redis(port=port)
    while True:
        try:
            if r.ping():
                break
        except redis.exceptions.RedisError as e:
            time.sleep(0.5)
            pass
    print('Redis has started')


def stop_redis_server(port=6379):
    redis.Redis(port=port).shutdown(True)
    print('Redis has stop')


def load_dumps(cfpq_data_path: str, redis_path, redis_dumps_path: str, suits, port=6379, host='localhost'):
    redis_bin_path = os.path.join(redis_path, 'src', 'redis-server')
    redis_conf_path = os.path.join(redis_path, 'redis.conf')

    graph_suit_dir = os.path.join(cfpq_data_path, 'data', 'graphs')
    for suite in suits:
        graph_dir = os.path.join(graph_suit_dir, suite, 'Matrices')

        for graph in filter(lambda s: not s.startswith('.'), os.listdir(graph_dir)):
            print(graph)
            graph_path = os.path.join(graph_dir, graph)

            if os.path.exists('dump.rdb'):
                os.remove('dump.rdb')

            start_redis_server(redis_bin_path, redis_conf_path)
            load(graph_path, graph, host, port)
            stop_redis_server()

            os.replace('dump.rdb', os.path.join(redis_dumps_path, graph.replace('.txt', '.rdb')))


def load_dumps_suit(suits):
    conf = Config('../config.ini')
    load_dumps(conf.cfpq_data_path, conf.redis_path, conf.redis_dumps_path, suits)
