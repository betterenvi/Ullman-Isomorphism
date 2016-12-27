import sys, collections, copy, re
import numpy as np

from Graph import *

class UllmanAlgorithm(object):
    """docstring for UllmanAlgorithm"""
    def __init__(self, *args, **kwargs):
        super(UllmanAlgorithm, self).__init__()

    def _init_params(self, g, q):
        self.q = q # the query graph
        self.g = g # the large graph
        self.A = q.get_adjacency_matrix()
        self.B = g.get_adjacency_matrix()
        for attr in ['num_nodes', 'num_edges']:
            setattr(self, attr + '_q', getattr(q, attr))
            setattr(self, attr + '_g', getattr(g, attr))

        self._construct_M()
        self.avail_g = np.ones(self.num_nodes_g) # if one node in g is not used/mapped. the opposite of 'F' vector in the paper
        self.Ms_isomorphic = list()
        # for i, arg in enumerate(args):
        #     setattr(self, 'arg_' + str(i), arg)
        # for kw, arg in kwargs.items():
        #     setattr(self, kw, arg)

    def _construct_M(self):
        self.M = np.logical_and(self.q.node_labels.values[:, None] == self.g.node_labels.values,
            self.q.node_degrees.values[:, None] <= self.g.node_degrees.values)
        # the above code is equivalent to the following
        # self.M = np.zeros((self.num_nodes_q, self.num_nodes_g))
        # for i, nid_q in enumerate(self.q.nodelist):
        #     for j, nid_g in enumerate(self.g.nodelist):
        #         if self.q.node_labels[nid_q] == self.g.node_labels[nid_g] and self.q.degree(nid_q) <= self.g.degree(nid_g):
        #             self.M[i, j] = 1

        self.M = self.M.astype(int)
        self._refine_M()

    def _refine_M(self):
        '''
        for any x, (A[i][x] == 1) ===> exist y s.t. (M[x][y] == 1 and B[j][y] == 1). iie.,
        for any x, (A[i][x] == 1) ===> exist y s.t. (M[x][y] == 1 and BT[y][j] == 1). i.e.,
        for any x, (A[i][x] == 1) ===> (M[x, :] dot_prod BT[:, j]) >= 1 . i.e.,
        (A[i, :] == 1)  ===> (M dot_prod BT[:, j]) >= 1 . i.e.,
        A[i, :] <= (M dot_prod BT[:, j]). i.e.,
        Let Y = M dot_prod BT, then
        A[i, :] <= Y[:, j] = YT[j, :]
        this refinement process is iterative
        '''
        BT = self.B.T
        changed = True
        while changed:
            changed = False
            for i in range(self.num_nodes_q):
                for j in range(self.num_nodes_g):
                    if self.M[i, j] > 0 and (self.A[i, :] <= self.M.dot(BT[:, j])).all():
                        self.M[i, j] = 0
                        changed = True

    def _check_isomorphic(self):
        '''
        check if (A[i, j] = 1) ==> (C[i, j] == 1) for any i, j
        '''
        C = self.M.dot((self.M.dot(self.B)).T)
        isomorphic = (self.A <= C).all()
        if isomorphic:
            self.Ms_isomorphic.append(copy.deepcopy(self.M))
            print self.M
        return isomorphic

    def _dfs(self, depth):
        if depth >= self.num_nodes_q:
            self._check_isomorphic()
            return
        row = copy.deepcopy(self.M[depth, :])
        if (row * self.avail_g).sum() == 0:
            return
        for j in range(self.num_nodes_g):
            if row[j] == 1 and self.avail_g[j]:
                self.M[depth, :] = 0
                self.M[depth, j] = 1
                self.avail_g[j] = 0
                self._dfs(depth + 1)
                self.avail_g[j] = 1
        self.M[depth, :] = row

    def run(self, g, q):
        self._init_params(g, q)
        self._dfs(0)
