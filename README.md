# Ullman Algorithm

Ullman算法是一个子图同构检测算法.

### 实现

我使用**Python 2**实现了Ullman算法。使用到的第三方库有 Networkx, Numpy和Pandas。我比较了使用Networkx的子图同构检测算法和我实现的Ullman算法的检测结果，验证了算法实现的正确性。

##### 代码说明

- Graph.py
    + 用于表示图的类的实现

- UllmanAlgorithm.py
    + Ullman算法的实现

- main.py
    + 运行示例
    + 比较Networkx的子图同构检测算法和我实现的Ullman算法的检测结果
