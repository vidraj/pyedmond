import numpy as np
import networkx as nx
from graph_tool.generation import complete_graph
from _core import build_graph, minimum_branching


def make_graph(graph_type='graph_tool'):

    n = 10
    if graph_type == 'graph_tool':
        g = complete_graph(n, directed=True)
        weights = np.abs(np.random.rand(g.num_edges()))
        return g, weights
    elif graph_type == 'networkx':
        g = nx.complete_graph(n, create_using=nx.DiGraph())
        weights = np.abs(np.random.rand(g.number_of_edges()))
        for k, (i, j) in enumerate(g.edges_iter()):
            g[i][j]['weight'] = weights[k]
        return g

# @profile
def test_cpp():
    g, weights = make_graph('graph_tool')
    # slower
    # edge_and_weights = [(int(e.source()), int(e.target()), w)
    #                     for e, w in zip(g.edges(), weights)]
    edge_and_weights = [(e[0], e[1], w)
                        for e, w in zip(g.get_edges(), weights)]

    g = build_graph(g.num_vertices(), edge_and_weights)
    # print('edges with weights')
    # print(graph_to_string(g))

    # print('optimal branching')
    tree_edges = minimum_branching(g, [0])
    print(tree_edges)

# @profile
def test_networkx():
    g = make_graph('networkx')
    nx.maximum_spanning_arborescence(g, attr='weight', default=1)


if __name__ == '__main__':
    test_cpp()
    # test_networkx()
