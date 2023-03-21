## 机器人学中的建图方法

## 随机数与采样

// TODO(fanmx): 随机数，伪随机数，随机性检测

上一讲中我们提到了机器人的状态的表示方法。对移动机器人，以及其他种类的机器人而言，我们都是用一组数据表达它目前所处的状态，而每个状态都可以视为一个节点，状态和状态之间可以用边相连，于是我们便有了一张图。路径规划问题，即寻找符合一定条件（从起点到终点，无碰撞，路径相对较短等）的状态的轨迹，当我们建立了这样一张图之后，便可以使用搜索算法求解路径规划问题。

为了方便算法的讨论，我们接下来选择二维平面作为示例。要知道，这里的空间其实是机器人的状态空间，完全可以是更高维度，不仅仅可以包含空间坐标，也可以包含加速度、曲率等各种物理参数。

下面我们来介绍几种机器人学中常用的建图的方法。

### PRM

PRM指概率随机地图（Probablistic Random Map）或概率路图（Probablistic Roadmap）。生成PRM需要以下两步：

1. 在状态空间（或设置空间）中随机取样。这一步中我们也可以剔除不可用的点，比如发生碰撞的点或者出于其他原因不应当选择的状态点等。
2. 采用一个本地规划器（local planner）将邻近的点相连。
3. 加入起点和终点，并与邻近的点相连。

<img src="resources/prm.gif" width="600"/>

由此我们便可以得到一个包含起点和终点的图。我们可以在这张图上使用各种搜索算法去寻找从起点到终点的路线，从而解决规划的问题。

Reference: [Wikipedia](https://en.wikipedia.org/wiki/Probabilistic_roadmap)

### RRT及其变种

PRM是一个相对容易理解并且相对通用的建图方法，但是它也有一些缺点：

1. 为了提高搜索的成功率以及搜索到的路径的质量，往往需要取大量的点，可能会影响运算速度。
2. 对于高维度的状态空间，例如六轴机械臂的configuration space高达6维，Juke Jerk车辆运动学模型可以高达8维，我们可能需要成指数增长的采样点才能完成规划任务。这也称为运动规划的维度灾难。

所以这里来介绍RRT，一个比PRM更快的建图的方法。直接来看伪代码：

```
Algorithm BuildRRT
    Input: Initial configuration qinit, number of vertices in RRT K, incremental distance Δq
    Output: RRT graph G

    G.init(qinit)
    for k = 1 to K do
        qrand ← RAND_CONF()
        qnear ← NEAREST_VERTEX(qrand, G)
        qnew ← NEW_CONF(qnear, qrand, Δq)
        G.add_vertex(qnew)
        G.add_edge(qnear, qnew)
    return G
```
其中，`RAND_CONF`在设置空间中取随机点，`NEAREST_VERTEX`在图上找距离给定点最近的节点，`NEW_CONF`根据给定的两个节点和给定的精度值，寻找符合条件的下一个节点（或多个节点）用来加入树。

二维空间中RRT的建图过程可以可视化如下：

<img src="resources/rrt.png" width="600"/>

可以把RRT理解为，通过从起点开始，向各个随机方向连直线，快速生成一颗尽量密布整个空间的树。

RRT还有许多变种，列举几种相对知名的如下：

1. bidirectional RRT: 从起点和终点分别建立两颗树，当两棵树相连时停止继续建图。
2. RRT*: 在建立树的过程中对局部的节点和边进行调整，使得从起始点到每个节点的距离尽量短。

Reference: [Wikipedia](https://en.wikipedia.org/wiki/Rapidly-exploring_random_tree)

### State Lattice（状态晶格）

以上两种建图方法中，相邻状态之间是由直线连接的，这其实对于机器人的可控性有一定的要求--并非所有类型的机器人，其设置空间或状态空间的每一个自由度都可以独立连续移动。对于六轴机械臂或者三维空间自由移动来说这个假设还算成立，对于常见的移动机器人来说，坐标位置的变换往往与朝向角度相关，从而不能简单地从设置空间或状态空间采样。

一种可能的建图方法是，从每一个节点出发，我们根据机器人的性质和要解决的问题的性质选取一些可能的基础运动单元（motion primitive），尽量覆盖各种方向、转向等，然后再从这些运动片段的终点继续选取新的运动片段。这种方法建立的图仿佛一个个晶体的晶格：

<img src="resources/state_lattice.png" width="600"/>

Reference: [Matthew's paper](https://www.ri.cmu.edu/pub_files/2011/5/20100914_icra2011-mcnaughton.pdf)

这是一种相对最适合移动机器人的建图方法。