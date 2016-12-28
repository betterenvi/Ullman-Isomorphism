import sys, collections, copy, re
import networkx as nx
from networkx.classes.graph import Graph as NXGraph
import numpy as np
import pandas as pd
from pandas import Series, DataFrame

class Graph(NXGraph):
    """docstring for Graph"""
    def __init__(self):
        super(Graph, self).__init__()

    def from_graph_str(self, graph_str, as_int=False, invalid_gid='-1'):
        '''
        return True if the graph data format is ok
        '''
        trans_func = lambda v : v
        if as_int:
            trans_func = lambda v : int(v)
        try:
            lines = graph_str.strip().split('\n')
            self.gid = trans_func(lines[0].split(' ')[-1])
            if self.gid == trans_func(invalid_gid):
                return False
            for line in lines[1:]:
                cols = line.split(' ')
                if cols[0] == 'v':
                    self.add_node(trans_func(cols[1]), label=trans_func(cols[2]))
                elif cols[0] == 'e':
                    self.add_edge(trans_func(cols[1]), trans_func(cols[2]), label=trans_func(cols[3]))
            self.num_nodes = len(self.nodes())
            self.num_edges = len(self.edges())
            self.nodelist = sorted(self.nodes())
            self.node_ids = Series(self.nodelist, index=range(self.num_nodes))
            self.node_id2idx = Series(range(self.num_nodes), index=self.nodelist)
            self.node_labels = Series([self.node[nid]['label'] for nid in self.nodelist], index=self.nodelist)
            self.node_degrees = Series([self.degree(nid) for nid in self.nodelist], index=self.nodelist)
            tmp = np.zeros((self.num_nodes, self.num_nodes))
            for nid1, nid2 in self.edges():
                idx1, idx2 = self.node_id2idx[nid1], self.node_id2idx[nid2]
                tmp[idx1, idx2] = tmp[idx2, idx1] = self.edge[nid1][nid2]['label']
            self.edge_labels = DataFrame(tmp)
            self.edge_labels.index = self.nodelist
            self.edge_labels.columns = self.nodelist
            return True
        except Exception, e:
            print e
            print 'Wrong graph data format'
            return False

    def get_adjacency_matrix(self):
        a = nx.adjacency_matrix(self, nodelist=self.nodelist)
        self.adj_mat = a.toarray()
        return self.adj_mat


def read_graphs(file_name):
    '''
    one file has multiple graphs
    '''
    with open(file_name) as fin:
        content = fin.read()
        graph_strs = content.split('t')
        graphs = []
        for graph_str in graph_strs:
            graph_str = graph_str.strip()
            if len(graph_str) <= 0:
                continue
            g = Graph()
            if g.from_graph_str(graph_str, as_int=True, invalid_gid='-1'):
                graphs.append(g)
        return graphs
