import pytest
import numpy as np
import networkx as nx
from graph_tool.all import Graph, GraphView, complete_graph, label_components, random_spanning_tree

from _core import minimum_branching
from converters import gt2edges_and_weights, nx2edges_and_weights, from_gt


@pytest.fixture
def g():
    return complete_graph(100, directed=True)


@pytest.fixture
def weights(g):
    return np.abs(np.random.rand(g.num_edges()))


def test_graphtool():
    g = Graph(directed=True)
    g.add_vertex(4)
    g.add_edge_list([(0, 1), (1, 2), (2, 3), (3, 0)])
    weight = g.new_edge_property('float')
    weight[g.edge(0, 1)] = 1
    weight[g.edge(1, 2)] = 2
    weight[g.edge(2, 3)] = 3
    weight[g.edge(3, 0)] = 4
    
    assert set(gt2edges_and_weights(g, weight.a)) == {
        (0, 1, 1), (1, 2, 2), (2, 3, 3), (3, 0, 4)
    }


def test_networkx():
    g = nx.DiGraph()
    g.add_edges_from([(0, 1, {'weight': 1}),
                      (1, 2, {'weight': 2}),
                      (2, 3, {'weight': 3}),
                      (3, 0, {'weight': 4})])
    assert set(nx2edges_and_weights(g, 'weight')) == {
        (0, 1, 1), (1, 2, 2), (2, 3, 3), (3, 0, 4)
    }


def is_arborescence(tree):
    # is tree?
    l, _ = label_components(GraphView(tree, directed=False))
    if not np.all(np.array(l.a) == 0):
        print('not connected')
        print(np.array(l.a))
        return False

    in_degs = np.array([v.in_degree() for v in tree.vertices()])
    if in_degs.max() > 1:
        print('in_degree.max() > 1')
        return False
    if np.sum(in_degs == 1) != (tree.num_vertices() - 1):
        print('should be: only root has no parent')
        return False

    roots = get_roots(tree)
    assert len(roots) == 1, '>1 roots'
    
    return True


def get_roots(t):
    """for undirected graph
    """
    return np.nonzero((t.degree_property_map(deg='out').a > 0)
                      & (t.degree_property_map(deg='in').a == 0))[0]


def test_feasibility(g, weights):
    internal_g = from_gt(g, weights)
    edges = minimum_branching(internal_g, [0])

    tree = Graph(directed=True)
    tree.add_edge_list(edges)
    assert is_arborescence(tree)


def test_optimilaity(g, weights):
    weight_prop = g.new_edge_property('float')
    weight_prop.a = weights
    
    internal_g = from_gt(g, weights)
    min_edges = minimum_branching(internal_g, [0])
    min_weight = sum(weight_prop[g.edge(i, j)]
                     for i, j in min_edges)
    
    def graph_weight(graph):
        return sum(weight_prop[e] for e in graph.edges())
        
    for i in range(1000):
        tree_map = random_spanning_tree(g)
        t = GraphView(g, efilt=tree_map, directed=True)
        assert graph_weight(t) >= min_weight
