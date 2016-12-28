import sys, collections, copy, re
from networkx.algorithms import isomorphism as iso

from UllmanAlgorithm import *
from Graph import *

data_dir = './data/graphDB/'
db_graphs_file_name = data_dir + 'mygraphdb.data'
query_graphs_file_name = data_dir + 'Q4.my'


db_graphs = read_graphs(db_graphs_file_name)
query_graphs = read_graphs(query_graphs_file_name)

ua = UllmanAlgorithm()

# example code
gi, qi = 0, 0
ua.run(db_graphs[gi], query_graphs[qi], display_mapping=True)
# there two ways to run UllmanAlgorithm:
# ua._init_params(db_graphs[gi], query_graphs[qi])
# ua._dfs()
# or
# ua.run(db_graphs[gi], query_graphs[qi])

# run in one bacth
cmp_with_nx = False
for gi in range(10):
    for qi in range(10):
        ua.run(db_graphs[gi], query_graphs[qi], display_mapping=False)
        if cmp_with_nx:
            gm = iso.GraphMatcher(db_graphs[gi], query_graphs[qi],
                node_match=iso.categorical_node_match('label', -1),
                edge_match=iso.categorical_node_match('label', -1))
            print gi, qi, len(ua.Ms_isomorphic), gm.subgraph_is_isomorphic()
            # print gm.mapping
