import sys, collections, copy, re
from networkx.algorithms import isomorphism

from UllmanAlgorithm import *
from Graph import *

data_dir = './data/graphDB/'
db_graphs_file_name = data_dir + 'mygraphdb.data'
query_graphs_file_name = data_dir + 'Q4.my'

ullman = UllmanAlgorithm()

db_graphs = read_graphs(db_graphs_file_name)
query_graphs = read_graphs(query_graphs_file_name)

ullman.run(query_graphs[0], db_graphs[0])
gm = isomorphism.GraphMatcher(db_graphs[0], query_graphs[0])
gm.subgraph_is_isomorphic()
