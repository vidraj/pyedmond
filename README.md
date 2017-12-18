# pyedmond

Edmond's optimal branching algorithm in C++ wrapped by Python.

As it's in C++ internally, it's faster and more memory-efficient than [networkx.maximum_spanning_arborescence](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.tree.branchings.maximum_spanning_arborescence.html)

# Example usage

```python
import numpy as np
import networkx as nx
from pyedmond import find_minimum_branching

g = nx.complete_graph(10, create_using=nx.DiGraph())
weights = np.abs(np.random.rand(g.number_of_edges()))
for k, (i, j) in enumerate(g.edges_iter()):
    g[i][j]['weight'] = weights[k]

edges = find_minimum_branching(g, roots=[0, 1])  # returns a list of (int, int) edges
```

# Installation

    pip3 install pyedmond

# Test

    python3 setup.py test

# notes on code

## `_core.cpp`

the interface between python and edmonds algorithm

## Main classes/functions

- `Graph`: the graph type
- `build_graph`: build graph from a list of edges and weights
- `optimal_branching`: find the optimal branching (used internally, need to convert the graph by yourself)
- `find_optimal_branching`: higher level function (graph is converted automatically)


# Todo

- [X] setup.py
- [X] usage documentation
- [ ] test coverage
- [ ] benchmark plot

# Reference

the C++ part is based on [atofigh/edmonds-alg](https://github.com/atofigh/edmonds-alg)