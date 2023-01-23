# 移动机器人运动规划笔记

笔记定位：希望可以作为自动驾驶、移动机器人运动规划的入门参考，如果读者能够理解笔记中大多数内容，并且完成大多数推荐练习项目，应该可以有能力独立完成一些运动规划相关的项目设计与实现，或者在自动驾驶或移动机器人行业找一份运动规划算法开发的工作。笔记对于比较重要的内容力求解释清楚，如果有读者遇到不熟悉的概念，希望可以善用搜索引擎学习。

目标人群：希望最好可以有计算机相关专业全日制本科或同等学力的编程水平和数学水平，部分章节涉及到略微复杂的矩阵运算。

# 目录

## 架构浅谈

简单介绍自动驾驶运动规划系统的架构，列举几种常见架构并对其优缺点进行分析，顺带一些关于运动规划周边模块的碎碎念。尽量不涉及商业分析，不过如果难免有一些涉及，这里仅作为知识分享和技术讨论，不构成任何商业建议。

## 运动规划基础知识

### 移动机器人运动学模型

列举几个常见的运动学模型，介绍移动机器人在运动规划问题中的数学模型。

### 计算几何学简介

矢量，矩阵，碰撞检测，轨迹的数学表达

## 基于采样的搜索算法

### 用搜索算法解决实际问题

通过一些有趣的案例向读者展示图搜索算法在实践中的用途。

### 采样算法综述

PRM, RRT, RRT-star, State Lattice, 他们各自的优缺点以及搜索算法的限制。

### 搜索算法综述

DFS, BFS, A*, beam search, focal search

## 优化算法综述

### 代价函数

列举几个常见的运动规划问题，以及可能的代价函数

### 优化算法

LQR及其各种变种

## 机器学习与前瞻

模仿学习，强化学习，逆强化学习
