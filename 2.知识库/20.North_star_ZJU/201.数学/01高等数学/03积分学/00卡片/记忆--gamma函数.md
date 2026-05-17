### 1. Gamma 函数的标准定义

在数学中，Gamma 函数 $\Gamma(s)$ 的标准积分定义是（通常要求 $s > 0$）：

$$\Gamma(s) = \int_0^{+\infty} x^{s-1} e^{-x} dx$$
$$\Gamma(s) = 2\int_0^{+\infty} x^{2s-1} e^{-x^2} dx$$
> **注意：** 这里的积分变量用 $x$ 还是 $t$ 都无所谓，关键看形式：一个是**幂函数** $x^{s-1}$，另一个是**指数函数** $e^{-x}$，且积分区间必须是 $(0, +\infty)$。

### 2. Gamma 函数的核心性质（为什么它等于阶乘？）

通过分部积分法，我们可以推导出一个极其重要的**递推公式**：

$$\Gamma(s+1) = s\Gamma(s)$$


### $\Gamma(s+1) = s\Gamma(s)$ 是怎么来的？

这个公式的推导核心只用到了一个高中/大一就会的技巧：


**推导过程：**

首先，写出 $\Gamma(s+1)$ 的积分定义（把 $\Gamma(s)$ 定义中的 $s$ 换成 $s+1$）：

$$\Gamma(s+1) = \int_0^{+\infty} x^{(s+1)-1} e^{-x} dx = \int_0^{+\infty} x^s e^{-x} dx$$

现在，我们对这个积分使用分部积分法。

令：

- $u = x^s$，则 $du = s x^{s-1} dx$
    
- $dv = e^{-x} dx$，则 $v = -e^{-x}$
    

套用分部积分公式：

$$\int_0^{+\infty} x^s e^{-x} dx = \left[ -x^s e^{-x} \right]_0^{+\infty} - \int_0^{+\infty} (-e^{-x}) \cdot s x^{s-1} dx$$

我们来分别计算这两部分：

**1. 前半部分（代入上下限）：**

$$\left[ -x^s e^{-x} \right]_0^{+\infty} = \left( \lim_{x \to +\infty} \frac{-x^s}{e^x} \right) - \left( -0^s e^0 \right)$$

- 当 $x \to +\infty$ 时，由于指数函数 $e^x$ 的增长速度远远快于任意幂函数 $x^s$，所以极限为 $0$（洛必达法则可证）。
    
- 当 $x \to 0$ 时（且 $s > 0$），$0^s = 0$。
    
    所以，前半部分等于 $0 - 0 = 0$。
    

**2. 后半部分（剩下的积分）：**

把负号和常数 $s$ 提出来：

$$- \int_0^{+\infty} (-e^{-x}) \cdot s x^{s-1} dx = s \int_0^{+\infty} x^{s-1} e^{-x} dx$$

看仔细了，后面这个积分 $\int_0^{+\infty} x^{s-1} e^{-x} dx$ 正是 $\Gamma(s)$ 的本尊！

**结论：**

$$\Gamma(s+1) = 0 + s\Gamma(s) = s\Gamma(s)$$
有了这个递推公式，魔法就出现了：

- 首先，我们可以算出 $\Gamma(1) = \int_0^{+\infty} e^{-x} dx = 1$。
    
- 根据递推公式：
    
    - $\Gamma(2) = 1 \cdot \Gamma(1) = 1 = 1!$
        
    - $\Gamma(3) = 2 \cdot \Gamma(2) = 2 \cdot 1 = 2!$
        
    - $\Gamma(4) = 3 \cdot \Gamma(3) = 3 \cdot 2 \cdot 1 = 3!$
        

以此类推，当 $n$ 为正整数时，就得到了你死死记住的那个公式：

$$\Gamma(n+1) = n!$$

这也是为什么我们说你记住的公式 $\int_0^{+\infty} x^n e^{-x} dx = n!$ 实际上求的是 $\Gamma(n+1)$。




### 3. 考研/高数必背的三个“开挂”结论

在做积分题时，如果你能敏锐地察觉到被积函数可以凑成 Gamma 函数的形式，很多极其复杂的广义积分就能瞬间秒杀。除了上面的阶乘公式，你还需要记住以下两个结论：

- **半整数的基准值：**
    
    $$\Gamma\left(\frac{1}{2}\right) = \sqrt{\pi}$$


- **高斯积分（也就是上一题用到的结论）：**
    
    结合 $\Gamma(1/2) = \sqrt{\pi}$ 和换元法，就得到了高斯积分的值：
    
    $$\int_0^{+\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$$

**推导过程：**

**第 1 步：把 $\Gamma(1/2)$ 转化为高斯积分**

根据定义，代入 $s = 1/2$：

$$\Gamma\left(\frac{1}{2}\right) = \int_0^{+\infty} x^{-1/2} e^{-x} dx$$

为了消去这个难看的负半次方，我们做一个换元：令 $x = t^2$（因为 $x>0$，所以 $t>0$）。

那么 $dx = 2t dt$。积分上下限不变，依然是 $0$ 到 $+\infty$。代入原式：

$$\Gamma\left(\frac{1}{2}\right) = \int_0^{+\infty} (t^2)^{-1/2} e^{-t^2} (2t) dt = \int_0^{+\infty} \frac{1}{t} e^{-t^2} 2t dt$$

消掉 $t$，得到：

$$\Gamma\left(\frac{1}{2}\right) = 2 \int_0^{+\infty} e^{-t^2} dt$$

现在，我们的目标变成了求 $I = \int_0^{+\infty} e^{-t^2} dt$ 这个值。只要算出它，乘上 2 就是答案。

**第 2 步：计算高斯积分 $I$（名场面来了）**

这个积分 $e^{-t^2}$ 的原函数不是初等函数，无法直接求牛顿-莱布尼茨公式。数学家想出了一个“升维打击”的方法：把它平方一下。

既然 $I = \int_0^{+\infty} e^{-x^2} dx$，那么也可以写成 $I = \int_0^{+\infty} e^{-y^2} dy$（积分变量用什么字母无所谓）。

把它们乘起来构成一个二重积分：

$$I^2 = \left( \int_0^{+\infty} e^{-x^2} dx \right) \left( \int_0^{+\infty} e^{-y^2} dy \right)$$

$$I^2 = \int_0^{+\infty} \int_0^{+\infty} e^{-x^2} e^{-y^2} dx dy = \iint_{D} e^{-(x^2+y^2)} dx dy$$

这里的积分区域 $D$ 是 $x > 0, y > 0$，即**第一象限**。

**第 3 步：转化为极坐标**

看到 $x^2 + y^2$，果断换成极坐标：

- $x^2 + y^2 = r^2$
    
- 面积微元 $dx dy = r dr d\theta$
    
- 在第一象限，角度 $\theta$ 的范围是 $[0, \frac{\pi}{2}]$，半径 $r$ 的范围是 $[0, +\infty)$。
    

代入后，原本无法计算的二重积分瞬间变得有解了，因为多出了一个 $r$：

$$I^2 = \int_0^{\pi/2} d\theta \int_0^{+\infty} e^{-r^2} r dr$$

- 前半部分角度积分：$\int_0^{\pi/2} d\theta = \frac{\pi}{2}$
    
- 后半部分半径积分：凑微分，$\int e^{-r^2} r dr = -\frac{1}{2} \int e^{-r^2} d(-r^2) = -\frac{1}{2} e^{-r^2}$。代入上下限 $0$ 到 $+\infty$，得到 $-\frac{1}{2}(0 - 1) = \frac{1}{2}$。
    

把两部分乘起来：

$$I^2 = \frac{\pi}{2} \times \frac{1}{2} = \frac{\pi}{4}$$

开平方得到 $I$：

$$I = \int_0^{+\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$$

**第 4 步：得出最终结论**

回到我们第 1 步推导出的式子：

$$\Gamma\left(\frac{1}{2}\right) = 2 \times I = 2 \times \frac{\sqrt{\pi}}{2} = \sqrt{\pi}$$

**实战串联：**

如果题目让你求 $\int_0^{+\infty} x^2 e^{-x^2} dx$，你会怎么做？

不用傻傻去算，直接令 $t = x^2$ 换元，它就会变成 $\frac{1}{2}\Gamma(3/2)$。而根据递推公式 $\Gamma(3/2) = \frac{1}{2}\Gamma(1/2) = \frac{\sqrt{\pi}}{2}$，最终答案就是 $\frac{\sqrt{\pi}}{4}$。这比分部积分快得多！



例：
![[记忆--gamma函数-1773372302006.jpeg]]