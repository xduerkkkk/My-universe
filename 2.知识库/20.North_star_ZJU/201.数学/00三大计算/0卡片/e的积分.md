## 1. 指数型积分（对应你的图 1）

这类积分通常出现在**指数分布**及其变形中。

### 核心公式

$$\int_{0}^{+\infty} e^{-ax} dx = \frac{1}{a} \quad (a > 0)$$

- **直观记忆：** 它是指数分布 $f(x) = \lambda e^{-\lambda x}$ 在正半轴积分等于 $1$ 的变体。
    
- **本题应用：** 图 1 中是 $\int_0^{\infty} \int_0^{\infty} e^{-(x+y)} dx dy$。利用**变量分离**，它等于 $(\int_0^{\infty} e^{-x} dx) \cdot (\int_0^{\infty} e^{-y} dy) = 1 \cdot 1 = 1$。所以 $c=1$。
    

---

## 2. 高斯积分（对应你的图 2）

这是**正态分布**归一化（规范性）的基础，极其重要。

### 核心公式

$$\int_{-\infty}^{+\infty} e^{-x^2} dx = \sqrt{\pi}$$

以及更通用的变形（由正态分布 $\frac{1}{\sqrt{2\pi}\sigma} e^{-\frac{x^2}{2\sigma^2}}$ 推导）：

$$\int_{-\infty}^{+\infty} e^{-\frac{x^2}{2\sigma^2}} dx = \sqrt{2\pi}\sigma$$

### 本题拆解

图 2 的被积函数是 $k \cdot e^{-\frac{1}{2}x^2 - \frac{1}{8}y^2}$，拆成两个一元积分：

1. **关于 $x$ 部分：** $\int_{-\infty}^{+\infty} e^{-\frac{x^2}{2}} dx$。这里 $\sigma^2 = 1$，所以结果是 $\sqrt{2\pi}$。
    
2. **关于 $y$ 部分：** $\int_{-\infty}^{+\infty} e^{-\frac{y^2}{8}} dx$。这里 $\frac{y^2}{8} = \frac{y^2}{2 \cdot 2^2}$，即 $\sigma = 2$。结果是 $\sqrt{2\pi} \times 2$。
    
3. **合并：** $k \cdot \sqrt{2\pi} \cdot 2\sqrt{2\pi} = k \cdot 4\pi = 1$。
    

---

## 3. 必须掌握的同类型特殊积分

除了上面两个，概率论考试中还有两个常考的“亲戚”积分，建议一并背诵：

### A. 伽马函数（指数型的升级版）

用于求期望或处理 $x^n e^{-x}$ 这种形式：

$$\int_{0}^{+\infty} x^n e^{-ax} dx = \frac{n!}{a^{n+1}} \quad (n \text{ 为正整数})$$

- **例子：** $\int_0^{\infty} x e^{-x} dx = 1$；$\int_0^{\infty} x^2 e^{-x} dx = 2$。
    

### B. 泊松积分的变体（正态分布期望相关）

如果你遇到带 $x$ 的高斯积分：

1. $\int_{-\infty}^{+\infty} x e^{-x^2} dx = 0$ （奇函数在对称区间积分）。
    
2. $\int_{-\infty}^{+\infty} x^2 e^{-ax^2} dx = \frac{1}{2a}\sqrt{\frac{\pi}{a}}$ （正态分布的方差推导结论）。