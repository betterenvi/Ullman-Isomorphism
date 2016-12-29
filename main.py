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

# run in one bacth
# and compare result with Networkx's
cmp_methods = ['has_iso', 'all_mappings_match']
extract_mapping = lambda gm : sorted(zip(gm.mapping.values(), gm.mapping.keys()))
extract_all_mappings = lambda gm : sorted([sorted(zip(mapping.values(), mapping.keys())) for mapping in list(gm.subgraph_isomorphisms_iter())])

cmp_method = cmp_methods[0]
num_unmatched = 0
for gi in range(10):
    # print gi
    for qi in range(10):
        gm = iso.GraphMatcher(db_graphs[gi], query_graphs[qi],
            node_match=iso.categorical_node_match('label', -1),
            edge_match=iso.categorical_edge_match('label', -1))
        if cmp_method == 'has_iso':
            ua_res = ua.has_iso(db_graphs[gi], query_graphs[qi], display_mapping=False)
            unmatched = ua_res != gm.subgraph_is_isomorphic()
            num_unmatched +=  unmatched
        else:
            ua.run(db_graphs[gi], query_graphs[qi], display_mapping=False)
            nx_mappings = extract_all_mappings(gm)
            unmatched = ua.mappings != nx_mappings
            num_unmatched += unmatched

        if unmatched:
            print gi, qi,
            print '\t|\tNX iso =', gm.subgraph_is_isomorphic(),
            if cmp_method == 'has_iso':
                print '\t|\tUA iso =', ua_res, '\t|\thas iso UA==NX :', False,
            else:
                print '\t|\tUA #iso =', len(ua.mappings), '\t|\t NX #iso = ', len(nx_mappings), '\t|\tmapping U==NX :', False,
            print ''

print '\nNum of unmatched:', num_unmatched
