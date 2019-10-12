from redis import Redis
from redisgraph import Node, Edge, Graph
from tqdm import tqdm

from .triplet_loader import load_rdf_graph


def get_total_edges(redis_graph: Graph):
    response = redis_graph.query('MATCH ()-[r]->() RETURN COUNT(r)')
    return response.result_set[0][0]


def insert_edge(redis_graph: Graph, edge: Edge):
    reversed_edge = Edge(edge.dest_node, f'{edge.relation}_r', edge.src_node)
    edge.dest_node.alias = "dest_node"
    edge.src_node.alias = "src_node"
    query = f'MERGE {edge.src_node}'
    redis_graph.query(query)
    query = f'MERGE {edge.dest_node}'
    redis_graph.query(query)
    query = f'MATCH {edge.src_node}, {edge.dest_node} CREATE {edge}, {reversed_edge}'
    redis_graph.query(query)


def load(rdf_file: str, redis_graph_name: str, redis_host: str, redis_port: int):
    rdf_graph = load_rdf_graph(rdf_file)

    redis_connector = Redis(host=redis_host, port=redis_port)
    redis_graph = Graph(redis_graph_name, redis_connector)

    for subj, pred, obj in tqdm(rdf_graph):
        edge = Edge(Node(label='Node', properties={'value': subj}),
                    pred,
                    Node(label='Node', properties={'value': obj}))
        insert_edge(redis_graph, edge)
