from redis import Redis
from redisgraph import Node, Edge, Graph
from tqdm import tqdm

from .triplet_loader import load_rdf_graph


def insert_edge(redis_graph: Graph, edge: Edge):
    reversed_edge = Edge(edge.dest_node, f'{edge.relation}_r', edge.src_node)
    query = f'MERGE {edge.src_node}'
    redis_graph.query(query)
    query = f'MERGE {edge.dest_node}'
    redis_graph.query(query)
    query = f'MATCH {edge.src_node}, {edge.dest_node} CREATE {edge}, {reversed_edge}'
    redis_graph.query(query)


def make_edge(subj, pred, obj):
    return Edge(Node(label='Node', properties={'value': subj}, alias='src_node'),
                pred,
                Node(label='Node', properties={'value': obj}, alias='dst_node'))


def load_in_redis(rdf_graph, redis_graph: Graph):
    for subj, pred, obj in rdf_graph:
        insert_edge(redis_graph, make_edge(subj, pred, obj))


def load(rdf_file: str, redis_graph_name: str, redis_host: str, redis_port: int):
    rdf_graph = load_rdf_graph(rdf_file)

    redis_connector = Redis(host=redis_host, port=redis_port)
    redis_graph = Graph(redis_graph_name, redis_connector)

    load_in_redis(tqdm(rdf_graph), redis_graph)
