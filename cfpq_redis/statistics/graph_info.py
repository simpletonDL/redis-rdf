from redis import Redis
from redisgraph import Graph


def get_distinct_edges(graph_name, redis=Redis()):
    g = Graph(graph_name, redis)
    resp = g.query('MATCH ()-[r]->() RETURN DISTINCT type(r)')
    return [x[0][2:-1] for x in resp.result_set]


def get_edges_counter(graph_name, redis=Redis()):
    g = Graph(graph_name, redis)
    return {
        rel_type: g.query(f'MATCH ()-[r:{rel_type}]->() RETURN COUNT (r)').result_set[0][0]
        for rel_type in get_distinct_edges(graph_name, redis)
    }


def get_node_count(graph_name, redis=Redis()):
    g = Graph(graph_name, redis)
    return g.query(f'MATCH (node) RETURN COUNT(node)').result_set[0][0]


def get_edge_count(graph_name, redis=Redis()):
    g = Graph(graph_name, redis)
    return g.query(f'MATCH ()-[edge]->() RETURN COUNT(edge)').result_set[0][0]


from cfpq_redis.utils.server import *
from cfpq_redis.configs.common import Config

conf = Config('../config.ini')
start_redis_server(conf.redis_bin, conf.redis_conf, '/home/simleton/Repo/redis-dumps/atom-primitive.rdb')

print(get_distinct_edges('atom-primitive.txt'))
print(get_edges_counter('atom-primitive.txt'))
print(get_node_count('atom-primitive.txt'))
print(get_edge_count('atom-primitive.txt'))
stop_redis_server()
