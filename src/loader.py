import rdflib
import redis
from redisgraph import Node, Edge, Graph
from tqdm import tqdm


def get_total_edges(redis_graph: Graph):
    response = redis_graph.query('MATCH ()-[r]->() RETURN COUNT(r)')
    return response.result_set[0][0]


def get_value(rdf_graph: rdflib.Graph, identifier):
    if isinstance(identifier, rdflib.URIRef):
        prefix, namespace, name = rdf_graph.compute_qname(identifier)
        return name
    return identifier


def insert_edge(redis_graph: Graph, edge: Edge):
    edge.dest_node.alias = "dest_node"
    edge.src_node.alias = "src_node"
    query = f'MERGE {edge.src_node}'
    redis_graph.query(query)
    query = f'MERGE {edge.dest_node}'
    redis_graph.query(query)
    query = f'MATCH {edge.src_node}, {edge.dest_node} CREATE {edge}'
    redis_graph.query(query)


def load(rdf_path: str, redis_graph_name: str, redis_host: str, redis_port: int):
    rdf_graph = rdflib.Graph()
    rdf_graph.load(rdf_path)

    redis_connector = redis.Redis(host=redis_host, port=redis_port)
    redis_graph = Graph(redis_graph_name, redis_connector)

    for subj, pred, obj in tqdm(rdf_graph):
        edge = Edge(Node(label='Node', properties={'value': get_value(rdf_graph, subj)}),
                    get_value(rdf_graph, pred),
                    Node(label='Node', properties={'value': get_value(rdf_graph, obj)}))
        insert_edge(redis_graph, edge)

    assert len(rdf_graph) == get_total_edges(redis_graph)
