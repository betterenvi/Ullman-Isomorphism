import sys, collections, copy, re
import numpy as np

from Graph import *

class UllmanAlgorithm(object):
    """docstring for UllmanAlgorithm"""
    def __init__(self, *args, **kwargs):
        super(UllmanAlgorithm, self).__init__()

    def _init_params(self, g, q, display_M=False, display_mapping=True, max_num_iso=float('inf')):
        self.q = q # the query graph
        self.g = g # the large graph
        self.A = q.get_adjacency_matrix()
        self.B = g.get_adjacency_matrix()
        self.display_M = display_M
        self.display_mapping = display_mapping
        self.max_num_iso = max_num_iso
        self.done = 0 >= max_num_iso
        for attr in ['num_nodes', 'num_edges']:
            setattr(self, attr + '_q', getattr(q, attr))
            setattr(self, attr + '_g', getattr(g, attr))

        self._construct_M()
        self.avail_g = np.ones(self.num_nodes_g) # if one node in g is not used/mapped. the opposite of 'F' vector in the paper
        self.Ms_isomorphic = list()
        self.mappings = list()
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
        self._refine_M(check_elabel=True)

    def _refine_M(self, max_iter=float('inf'), check_elabel=True):
        '''
        for any x, (A[i, x] == 1) ===> exist y s.t. M[x, y] == 1 and B[j, y] == 1 and elabel_q[i, x] == elabel_g[j, y]
        for any x, (A[i, x] == 1) ===> exist y s.t. (M[x, y] == 1 and BT[y, j] == 1 and el_q[i, x] == el_gT[y, j]). i.e.,
        for any x, (A[i, x] == 1) ===> (M[x, :] dot_prod (BT[:, j] col_ele_prod el_gT[:, j] == el_q[i, x])) >= 1 . i.e.,
        (A[i, :] == 1)  ===> diag(M dot_prod (BT[:, j] col_ele_prod (el_gT[:, j] outer_eq el_q[i, :]))) >= 1 . i.e.,
        A[i, :] <= diag(M dot_prod (BT[:, j] col_ele_prod (el_gT[:, j] outer_eq el_q[i, :]))).
        A[i, :] <= rowsum(M ele_prod ((el_qT[:, i] outer_eq el_g[j, :]) row_ele_prod B[j, :]))
        in numpy:
        A[i, :] <= (M * (el_q[:, i][:, None] == el_g[j, :]) * B[j, :]).sum(axis=1)

        if don't want to check edge label, then
        for any x, (A[i, x] == 1) ===> exist y s.t. (M[x, y] == 1 and B[j, y] == 1).
        A[i, :] <= rowsum(M ele_prod (E row_ele_prod B[j, :]))
        A[i, :] <= rowsum(M row_ele_prod B[j, :])  # in numpy: A[i, :] <= (M * E * B[j, :]).sum(axis=1)
        A[i, :] <= (M dot_prod BT[:, j]).
        Let Y = M dot_prod BT, then
        A[i, :] <= Y[:, j] = YT[j, :]

        this refinement process is iterative
        '''
        if check_elabel:
            el_g = self.g.edge_labels.values
            el_q = self.q.edge_labels.values
        changed = True
        num_iter = 0
        while changed and num_iter < max_iter:
            changed = False
            num_iter += 1
            for i in range(self.num_nodes_q):
                for j in range(self.num_nodes_g):
                    if check_elabel:
                        flag = self.M[i, j] > 0 and (self.A[i, :] > (self.M * (el_q[:, i][:, None] == el_g[j, :]) * self.B[j, :]).sum(axis=1)).any()
                    else:
                        flag = self.M[i, j] > 0 and (self.A[i, :] > self.M.dot(self.B.T[:, j])).any()
                    if flag:
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
            self.mappings.append(self._get_mapping(-1))
            self.done = len(self.mappings) >= self.max_num_iso
            if self.display_M:
                print self.M
            if self.display_mapping:
                print self.mappings[-1]
        return isomorphic

    def _get_mapping(self, M_idx=None):
        if M_idx == None:
            res = list()
            for M_idx in range(len(self.Ms_isomorphic)):
                res.append(self._get_mapping(M_idx))
            return res
        elif M_idx >= len(self.Ms_isomorphic):
            return None
        M = self.Ms_isomorphic[M_idx]
        I, J = np.where(M == 1)
        return zip(list(I), list(J))

    def _dfs(self, depth=0):
        if self.done:
            return
        if depth >= self.num_nodes_q:
            self._check_isomorphic()
            return
        row = copy.deepcopy(self.M[depth, :])
        if (row * self.avail_g).sum() == 0:
            return
        self.M[depth, :] = 0
        for j in range(self.num_nodes_g):
            if row[j] == 1 and self.avail_g[j] == 1:
                self.M[depth, j] = 1
                self.avail_g[j] = 0
                self._dfs(depth + 1)
                self.avail_g[j] = 1
                self.M[depth, j] = 0
                if self.done:
                    break
        self.M[depth, :] = row

    def run(self, g, q, display_M=False, display_mapping=True, max_num_iso=float('inf')):
        '''
        max_num_iso: if max_num_iso isomorphic subgraphs have been found, then stop
        '''
        self._init_params(g, q, display_M=display_M, display_mapping=display_mapping, max_num_iso=max_num_iso)
        self._dfs(depth=0)

    def has_iso(self, g, q, display_M=False, display_mapping=True):
        '''
        check if g has at least 1 subgraph isomorphic to q
        '''
        self.run(g, q, display_M=display_M, display_mapping=display_mapping, max_num_iso=1)
        return len(self.mappings) > 0
