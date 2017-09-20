import numpy as np
from graph_tool.generation import complete_graph
from _core import build_graph, optimal_branching


def make_graph():
    g = complete_graph(1000, directed=True)
    weights = np.abs(np.random.rand(g.num_edges()))
    return g, weights

@profile
def test_cpp():
    g, weights = make_graph()
    edge_and_weights = [(int(e.source()), int(e.target()), w)
                        for e, w in zip(g.edges(), weights)]

    g = build_graph(g.num_vertices(), edge_and_weights)
    # print('edges with weights')
    # print(graph_to_string(g))

    # print('optimal branching')
    optimal_branching(g)


def test_networkx():
    pass

if __name__ == '__main__':
    test_cpp()
