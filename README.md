# Ullman Algorithm

Ullman Algorithm [1] 是一个子图同构检测算法.

### 实现

我使用**Python 2**实现了Ullman算法。使用到的第三方库有 Networkx, Numpy和Pandas。

我比较了Networkx的子图同构检测算法和我实现的Ullman算法的运行结果，验证了我实现的算法的正确性。

##### 代码说明

- Graph.py
    + 用于表示图的类的实现

- UllmanAlgorithm.py
    + Ullman算法的实现

- main.py
    + 运行示例
    + 比较Networkx的子图同构检测算法和我实现的Ullman算法的检测结果

### 参考文献
[1] Ullmann J R. An algorithm for subgraph isomorphism[J]. Journal of the ACM (JACM), 1976, 23(1): 31-42.
