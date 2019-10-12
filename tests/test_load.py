import logging
import random
import string
from unittest import TestCase

from redis import Redis
from redisgraph import Graph, Edge

from src.loader import load_in_redis, make_edge
from src.triplet_loader import load_rdf_graph


def print_edge_with_alias(edge: Edge, alias: str):
    return f'{edge.src_node}-[{alias}: {edge.relation} {edge.toString()}]->{edge.dest_node}'


class TestLoad(TestCase):
    def setUp(self):
        logging.disable(logging.WARNING)
        self.redis_connector = Redis(host='localhost', port=6379)

    def testLoadTxt(self):
        self.loadAndCheck(load_rdf_graph('../examples/graph.txt'))

    def testSmallXml(self):
        self.loadAndCheck(load_rdf_graph('../examples/graph.xml'))

    def testBigXml(self):
        self.loadAndCheck(load_rdf_graph('../examples/pizza.xml'))

    def loadAndCheck(self, rdf_graph):
        redis_graph = Graph(self.randomGraphName(), self.redis_connector)

        # load
        load_in_redis(rdf_graph, redis_graph)

        # check every edge
        for subj, pred, obj in rdf_graph:
            self.assertTrue(self.checkEdgeExist(redis_graph, make_edge(subj, pred, obj)))
            self.assertTrue(self.checkEdgeExist(redis_graph, make_edge(obj, f'{pred}_r', subj)))

        # check total edges count
        self.assertEqual(len(rdf_graph) * 2, self.countEdges(redis_graph))

    @staticmethod
    def checkEdgeExist(redis_graph: Graph, edge: Edge):
        query = f'MATCH {print_edge_with_alias(edge, "edge")} RETURN COUNT(edge)'
        return redis_graph.query(query).result_set[0][0] > 0

    @staticmethod
    def countEdges(redis_graph: Graph):
        query = f'MATCH ()-[r]->() RETURN COUNT(r)'
        return redis_graph.query(query).result_set[0][0]

    @staticmethod
    def randomGraphName():
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(10))
