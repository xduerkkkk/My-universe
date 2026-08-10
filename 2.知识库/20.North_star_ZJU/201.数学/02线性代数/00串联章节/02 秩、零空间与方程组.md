# 操作方向与保秩条件

## 1. 各行、各列元素之和

设 $A$ 为 $m\times n$ 矩阵，记

$$
\mathbf 1_m=(1,\dots,1)^T\in\mathbb R^m,
\qquad
\mathbf 1_n=(1,\dots,1)^T\in\mathbb R^n.
$$

则：

- 各列元素之和组成的行向量：

$$
\mathbf 1_m^TA;
$$

- 各行元素之和组成的列向量：

$$
A\mathbf 1_n.
$$

> [!tip] 记忆
> 求列和，需要沿“行方向”累加，所以左乘全 $1$ 行向量；求行和，需要沿“列方向”累加，所以右乘全 $1$ 列向量。

## 2. 左乘、右乘时谁的秩被保住

设

$$
A\in\mathbb R^{m\times n},\qquad B\in\mathbb R^{n\times p}.
$$

### 左因子列满秩：保住右边 $B$ 的秩

若

$$
r(A)=n,
$$

即 $A$ 列满秩，则 $N(A)=\{0\}$，线性映射 $x\mapsto Ax$ 是单射。因此 $B$ 的列向量之间原有的线性无关关系不会被 $A$ 压掉：

$$
\boxed{r(AB)=r(B)}.
$$

### 右因子行满秩：保住左边 $A$ 的秩

若

$$
r(B)=n,
$$

即 $B$ 行满秩，则存在右逆 $C$ 使 $BC=E_n$。于是

$$
A=(AB)C.
$$

结合 $r(AB)\le r(A)$，得到

$$
\boxed{r(AB)=r(A)}.
$$

> [!important] 统一口诀
> **左因子列满秩，保右边；右因子行满秩，保左边。**

## 3. 不要把“满秩”说得过于笼统

对 $m\times n$ 矩阵 $A$：

- 列满秩：$r(A)=n$，要求 $m\ge n$；
- 行满秩：$r(A)=m$，要求 $m\le n$；
- 只有方阵中，“行满秩”“列满秩”“可逆”才等价。

> [!warning] 常见误判
> - “左乘一个满秩矩阵一定保秩”不够准确，要看它是否**列满秩**以及乘法尺寸；
> - “右乘一个满秩矩阵一定保秩”也不够准确，要看它是否**行满秩**；
> - 对长方阵，满秩可能只意味着行满秩或列满秩中的一种。

## 4. 满秩块为什么能消去相邻块

设 $A\in\mathbb R^{m\times n}$。

### $A$ 行满秩：可消去右边的任意同高块

若 $r(A)=m$，则

$$
\operatorname{Col}(A)=\mathbb R^m.
$$

对任意 $B\in\mathbb R^{m\times p}$，方程

$$
AX=-B
$$

有解。因此在分块矩阵 $(A\mid B)$ 中，可以用列变换

$$
C_2\leftarrow C_2+C_1X
$$

把 $B$ 消成零块。

### $A$ 列满秩：可消去下面的任意同宽块

若 $r(A)=n$，则

$$
\operatorname{Row}(A)=\mathbb R^n.
$$

对任意 $C\in\mathbb R^{q\times n}$，方程

$$
YA=-C
$$

有解。因此在分块矩阵

$$
\begin{pmatrix}A\\C\end{pmatrix}
$$

中，可以用行变换把 $C$ 消成零块。

> [!tip] 与上一节的对应
> - 行满秩说明列空间铺满，能处理右边同高的列块；
> - 列满秩说明行空间铺满，能处理下面同宽的行块。

## 5. 三句底层公式

以后如果口诀不确定，就回到下面三句：

$$
\operatorname{Col}(AB)\subseteq\operatorname{Col}(A),
$$

$$
\operatorname{Row}(AB)\subseteq\operatorname{Row}(B),
$$

$$
r(AB)\le\min\{r(A),r(B)\}.
$$

相关内容：[[03 分块矩阵]]、[[04自测题]]。