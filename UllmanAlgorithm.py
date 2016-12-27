import sys, collections, copy, re
import numpy as np

from Graph import *

class UllmanAlgorithm(object):
    """docstring for UllmanAlgorithm"""
    def __init__(self, q, g, *args, **kwargs):
        super(UllmanAlgorithm, self).__init__()
        self.q = q # the query graph
        self.g = g # the large graph
        self.A = q.get_adjacency_matrix()
        self.B = g.get_adjacency_matrix()
        for attr in ['num_nodes', 'num_edges']:
            setattr(self, attr + '_q', getattr(q, attr))
            setattr(self, attr + '_g', getattr(g, attr))

        self._construct_M0()
        # for i, arg in enumerate(args):
        #     setattr(self, 'arg_' + str(i), arg)
        # for kw, arg in kwargs.items():
        #     setattr(self, kw, arg)

    def _construct_M0(self):
        self.M = np.zeros((self.num_nodes_q, self.num_nodes_g))








