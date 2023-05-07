# 3_几何表达

为了解决一个运动规划的问题，我们首先要对问题进行一定的抽象和数学建模。例如对于扫地机器人，我们该如何表达机器人的形状和周围物体的形状，又该如何避免机器人的运动路径中发生碰撞呢？对于自动驾驶汽车，我们如何表达车道线、周围的其他车辆行人等。

## 几何建模

视需要解决的具体问题不同、运行算法的硬件不同或各种其他原因，运动规划问题有许多种不同的几何建模方法。通常我们可以将几何建模的方法归为两大类：

* 边界表示法(boundary representation)：我们通过几何形状的边界来表示各个几何形状。例如二维问题中，我们用圆周表示一个圆形的障碍物，或者一组顶点和边来表示一个多边形；三维问题中，我们通过大量的三角面片表示零件的外轮廓等。
* 体表示法(solid representation)：我们通过几何形状包围范围的集合来表示几何形状。例如在占据栅格地图(occupational grid map)中，将有障碍物存在的地方标记为不可通行；或者通过“点到圆心的距离小于半径”来表达圆。

## 形状的表达

本章节主要研究二维平面中的问题。在地形并非十分复杂、环境相对可控的情况下，将机器人运动规划建模成一个二维的问题可以省去不少麻烦；许多三维情况下的表示方法和算法亦可以用二维的处理方法类比推知。以下为几种常见的二维几何形状的常见数学表达方法：

| 形状       | 数学表达                                           | 解释                                     |
| ---------- | -------------------------------------------------- | ---------------------------------------- |
| 点         | $(x, y)$                                           | 横纵坐标                                 |
| 圆         | $(x, y, r)$                                        | 圆心坐标和半径                           |
| 线段       | $(x_0, y_0, x_1, y_1)$  或 $(x_c, y_c, l, \theta)$ | 两端点坐标，或者中心点坐标、长度和旋转角 |
| 任意矩形   | $(x, y, l, w, \theta)$                             | 中心点坐标，长度，宽度，旋转角           |
| 任意多边形 | $(x_0, y_0, x_1, y_1, \dots, x_n, y_n)$            | 按逆时针顺序存放的顶点坐标               |

形状的表达不能独立于坐标系。以上表达方式在全局坐标系中直接使用，可以很方便地表达静态的物体；而对于运动的物体，我们可以在运动物体上建立独立的坐标系，这样物体相对于它自己的坐标系永远保持静止，我们便把运动物体的表达分为两部分，固有属性和状态：

| 形状     | 数学表达                                            | 固有属性        | 状态                 |
| -------- | --------------------------------------------------- | --------------- | -------------------- |
| 点       | $(x, y)$                                            |                 | $(x, y)$             |
| 圆       | $(x, y, r)$                                         | $(r)$           | $(x, y)$             |
| 线段     | $(x_0, y_0, x_1, y_1)$   或 $(x_c, y_c, l, \theta)$ | $(l)$           | $(x_c, y_c, \theta)$ |
| 任意矩形 | $(x, y, l, w, \theta)$                              | $(l, w)$  |      $(x, y, \theta)$        |

任意多边形的表达可以类比矩形，使用一组原点附近的点表示其形状，再用坐标和角度表示其位置变换。

对于任意多边形和其他一些复杂的情况，我们也可以用固有属性表达其形状，而用不多于横纵坐标与旋转角的三个量来表达它在二维空间中的状态。实际上，点和圆具有旋转对称性（或者说没有方向性），所以我们没有将 $\theta$ 记入状态，想计入也是可以的。

## 齐次变换

平面空间中的运动可以拆解成两个部分：平移和旋转。

其中平移的部分相对容易理解：只需要在横纵坐标上加减对应的位移即可。例如将位于 $(x_0, y_0)$ 的点移动 $(x_d, y_d)$ ，即可得到 $(x_0 + x_d, y_0 + y_d)$。

对于旋转的部分，我们先考虑点  $(x_0, y_0)$ 绕原点旋转 $\theta$ 角的情况：通过一定的几何运算，我们可以得到旋转之后的点 $(x \cos \theta - y \sin \theta, x \sin \theta + y \cos \theta)$。

我们可以将旋转变换写成矩阵的形式：

$$
 \begin{bmatrix} x \cos \theta - y \sin \theta \\ x \sin \theta + y \cos \theta \end{bmatrix} = \begin{bmatrix} \cos \theta & -\sin \theta \\ \sin \theta & \cos \theta \end{bmatrix}  \begin{bmatrix} x \\ y \end{bmatrix}
$$

由此方便起见我们可以定义一个以原点为中心的旋转矩阵：

$$
 R(\theta) := \begin{bmatrix} \cos \theta & -\sin \theta \\ \sin \theta & \cos \theta \end{bmatrix} 
$$

那对于既有旋转又有平移的情况该如何处理呢？要注意的是先平移 $(x_d, y_d)$ 再绕原点旋转和先绕原点旋转再平移 $(x_d, y_d)$ ，我们会得到不同的变换结果。为了方便起见，约定俗成地，我们一般先绕原点进行旋转变换，再进行平移变换。

对于一个任意点 $(x, y)$， 我们将其写作齐次坐标的形式： $[x y 1]^T$ ，这样的话我们便可以用矩阵乘法来表示平移变换和旋转变换：

$$
 \begin{bmatrix} x + x_d \\ y + y_d \\ 1 \end{bmatrix} = \begin{bmatrix} 1 & 0 & x_d \\ 0 & 1 & y_d \\ 0 & 0 & 1\end{bmatrix}  \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}
$$

$$
 \begin{bmatrix} x \cos \theta - y \sin \theta \\ x \sin \theta + y \cos \theta \\ 1 \end{bmatrix} = \begin{bmatrix} \cos \theta & -\sin \theta & 0 \\ \sin \theta & \cos \theta & 0 \\ 0 & 0 & 1 \end{bmatrix}  \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}
$$

我们也可以将旋转变换和平移变换组合成一个矩阵：

$$
\begin{bmatrix} \cos \theta & -\sin \theta & x_d \\ \sin \theta & \cos \theta & y_d \\ 0 & 0 & 1 \end{bmatrix}
$$

这个矩阵便能表示先旋转后平移的变换。

注意到：

$$
\begin{bmatrix} 1 & 0 & x_d \\ 0 & 1 & y_d \\ 0 & 0 & 1\end{bmatrix} \begin{bmatrix} \cos \theta & -\sin \theta & 0 \\ \sin \theta & \cos \theta & 0 \\ 0 & 0 & 1 \end{bmatrix} = \begin{bmatrix} \cos \theta & -\sin \theta & x_d \\ \sin \theta & \cos \theta & y_d \\ 0 & 0 & 1 \end{bmatrix}
$$

而当顺序反过来：

$$
\begin{bmatrix} \cos \theta & -\sin \theta & 0 \\ \sin \theta & \cos \theta & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} 1 & 0 & x_d \\ 0 & 1 & y_d \\ 0 & 0 & 1\end{bmatrix} = \begin{bmatrix} \cos \theta & -\sin \theta & x_d \cos \theta - y_d \sin \theta \\ \sin \theta & \cos \theta & x_d \sin \theta + y_d \sin \theta \\ 0 & 0 & 1 \end{bmatrix}
$$

这恰好是先平移再绕原点旋转的结果。

更一般地讲，对于*依次*进行多个齐次变换操作 $T_1, T_2, \dots, T_n$，最终的总变换可以通过变换矩阵的连乘 $T_n T_{n-1} \dots T_2 T_1$ 计算得到。