from cfpq_redis.statistics.graph_info import *
from cfpq_redis.utils.server import *
import pandas as pd


def main():
    conf = Config('../config.ini')

    resp = {
        'graph': [],
        'node_count': [],
        'edge_count': [],
        'edges_counter': []
    }

    for dump in os.listdir(conf.redis_dumps_path):
        graph_name = dump.replace('.rdb', '.txt')
        start_redis_server(conf.redis_bin, conf.redis_conf, os.path.join(conf.redis_dumps_path, dump))

        resp['graph'].append(graph_name)
        resp['node_count'].append(get_node_count(graph_name))
        resp['edge_count'].append(get_edge_count(graph_name))
        resp['edges_counter'].append(get_edges_counter(graph_name))

        stop_redis_server()

    df = pd.DataFrame(resp)
    df.to_csv(os.path.join('results', 'statistic.csv'), index=False)


if __name__ == '__main__':
    main()
