import sys
from ._core import minimum_branching, maximum_branching
from .converters import from_gt, from_nx


def find_minimum_branching(g, roots=[], **kwargs):
    """
    Args:
    -----------
    
    g: graph_tool.Graph or networkx.DiGraph

    roots: list of roots to consider

    kwargs: either `weights` (for graph_tool) or `weight` (for networkx)

    if `weights`, it's numpy.ndarray or list where each entry corresponds to one edge of g

    Returns:
    ------------

    a list of edges, (int, int)
    """
    try:
        import networkx as nx
        if isinstance(g, nx.DiGraph):
            internal_g = from_nx(g, **kwargs)
        else:
            raise TypeError
    except (ImportError, TypeError) as e:
        try:
            from graph_tool import Graph
            if isinstance(g, Graph):
                internal_g = from_gt(g, **kwargs)
            else:
                raise TypeError('currenly, only networkx.DiGraph and graph_tool.Graph are supported')
        except ImportError:
            print('cannot import neither networkx nor graph_tool')
            sys.exit(-1)

    return minimum_branching(internal_g, roots)

def find_maximum_branching(g, roots=None, **kwargs):
    """
    Args:
    -----------
    
    g: graph_tool.Graph or networkx.DiGraph

    roots: list of roots to consider

    kwargs: either `weights` (for graph_tool) or `weight` (for networkx)

    if `weights`, it's numpy.ndarray or list where each entry corresponds to one edge of g

    Returns:
    ------------

    a list of edges, (int, int)
    """

    if roots is None:
        roots = []

    try:
        import networkx as nx
        if isinstance(g, nx.DiGraph):
            internal_g = from_nx(g, **kwargs)
        else:
            raise TypeError
    except ImportError:
        print('cannot import networkx')
        sys.exit(-1)

    return maximum_branching(internal_g, roots)
