from pathlib import Path
import json,re,shutil,hashlib
w=Path('_temp/math02_organizer'); L=json.loads((w/'ledger.json').read_text(encoding='utf-8')); images=json.loads((w/'images.json').read_text(encoding='utf-8')); hashes=json.loads((w/'hashes.json').read_text(encoding='utf-8'))
skill=Path('C:/Users/kkkkkk/.codex/skills/math-exercise-organizer'); target=Path(L[0]['source']).parent/'02随机变量-题型检索整理.md'
backup=w/'revision_backup'
for p in [target,skill/'SKILL.md',skill/'scripts/audit_math_summary.py',skill/'agents/openai.yaml']:
 dest=backup/p.name
 if not dest.exists(): shutil.copy2(p,dest)
# Each row: category, stable ID, original block index, title, setup, three steps, trap, short answer.
rows=[
('分布函数与密度：先检查定义','02-1a',0,'分段 CDF 求密度：只在可导区间求导',r'$F_X(x)$ 在 $x<0$ 为 0，在 $0\le x<1$ 为 $x^2$，在 $x\ge1$ 为 1。',r'按 CDF 的分段点 0、1 划区间。',r'在开区间逐段求导：$(0,1)$ 内为 $2x$，其余为 0。',r'检查 $F$ 在分段点无跳跃，再验密度积分为 1。',r'密度在有限个端点的取值不影响概率；不能因此说 $F$ 在 1 处可导。',r'$f_X(x)=2x\;(0<x<1)$，其余取 0。'),
('分布函数与密度：先检查定义','02-1b',0,'正弦 CDF：先补两端，再求导',r'手写补题：$F_X(x)=\sin x$（$0\le x<\pi/2$），左侧为 0，右侧为 1。',r'确认两端衔接：$\sin0=0$、$\sin(\pi/2)=1$。',r'只在 $(0,\pi/2)$ 内求导，得到 $\cos x$。',r'区间外密度取 0，并验非负、积分为 1。',r'不能把 $\cos x$ 当作全实轴上的密度。',r'$f_X(x)=\cos x\;(0<x<\pi/2)$，其余为 0。'),
('分布函数与密度：先检查定义','03-1',3,'CDF 复合变换：两端、单调、右连续',r'判断 $F(2x-1),F(1-x),F(x^2),1-F(-x)$ 是否必为分布函数。',r'先看两端极限：$F(x^2)$ 在 $x\to-\infty$ 时趋于 1，排除。',r'再看单调性：$F(1-x)$ 非增，排除。',r'最后看右连续：$1-F(-x)$ 遇原分布的跳点可能失败；$F(2x-1)$ 三项都满足。',r'负号会把右侧逼近变成左侧逼近；有原子时，反射公式要写 $1-F_X((-y)^-)$。',r'只有 $F(2x-1)$ 必然成立。'),
('分布函数与密度：先检查定义','03-5',7,'CDF 与密度的组合：归一化条件不同',r'比较 $aF_1+bF_2$、$cF_1F_2$ 与 $cf_1f_2$。',r'线性组合先验两端：需 $a+b=1$；再看非减，$a,b\ge0$ 可保证。',r'CDF 乘积非减且右连续；由右端极限 $c=1$ 确定常数。',r'密度乘积改查积分：若 $0<\int f_1f_2<\infty$，取 $c=(\int f_1f_2)^{-1}$。',r'$a+b=1$ 单独不够；非负权重是通用充分条件，并非每一对固定 $F_1,F_2$ 的必要条件。',r'CDF 看端点极限，密度看总积分；不能共用 $c=1$。'),
('分布函数与密度：先检查定义','880-1',22,'单点概率为零：等价于 CDF 连续',r'已知对任意 $x$，$P(X=x)=0$，判断能推出什么。',r'写跳跃公式：$P(X=x)=F(x)-F(x^-)$。',r'单点质量全为 0，说明无左跳；结合 CDF 右连续，得到处处连续。',r'反向用连续性代回跳跃公式；用均匀分布反驳“密度必须连续”。',r'CDF 连续不等于有密度，更不等于密度连续。',r'$P(X=x)=0\ (\forall x)\iff F$ 连续。'),
('离散计数：翻译事件、识别分布','02-3',2,'0–1 变量乘积与和：先看是否同一事件',r'$X,Y\in\{0,1\}$，边缘概率均为 $P(0)=1/4,P(1)=3/4$；已知 $P(XY\ne1)=3/8$，求 $P(X+Y\le1)$。',r'列四种取值：$(0,0),(0,1),(1,0),(1,1)$。',r'$XY\ne1$ 和 $X+Y\le1$ 都只排除 $(1,1)$。',r'直接使用事件相等；若补联合表，由 $P_{11}=5/8$ 和边缘概率倒推其余格子。',r'同分布不等于独立；本题不需要假设独立。',r'目标概率 $3/8$；$P_{00}=P_{01}=P_{10}=1/8$。'),
('离散计数：翻译事件、识别分布','03-3',5,'伯努利和近似泊松：参数取 np',r'20 个独立 $\mathrm{Bernoulli}(0.1)$ 变量之和 $T$，近似求 $P(T\le1)$。',r'精确模型先写 $T\sim B(20,0.1)$。',r'用泊松近似，参数 $\lambda=np=2$。',r'累加 0、1 两项：$e^{-2}+2e^{-2}$。',r'泊松是近似，不是把二项分布改成精确泊松分布。',r'$P(T\le1)\approx3e^{-2}$。'),
('离散计数：翻译事件、识别分布','03-4',6,'泊松奇偶概率：和为 1，差用指数级数',r'$X\sim\mathrm{Poisson}(\lambda)$，比较取奇数与偶数的概率。',r'设 $p_e=P(X\text{ 为偶数}),p_o=P(X\text{ 为奇数})$，有 $p_e+p_o=1$。',r'作差：$p_e-p_o=E[(-1)^X]=e^{-\lambda}\sum_{k\ge0}(-\lambda)^k/k!=e^{-2\lambda}$。',r'联立和差式，分别求两类概率。',r'0 是偶数，不能从偶数概率中漏掉 $P(X=0)$。',r'$p_e=(1+e^{-2\lambda})/2$，$p_o=(1-e^{-2\lambda})/2$，故 $p_e>p_o$。'),
('离散计数：翻译事件、识别分布','03-12',14,'阶乘分母的概率级数：先归一化再认参数',r'$P(X=k)=ae^{-2}/k!$，$k=0,1,\ldots$，求 $a$。',r'把概率求和等于 1：$ae^{-2}\sum_{k\ge0}1/k!=1$。',r'识别指数级数 $\sum1/k!=e$，解出 $a=e$。',r'代回得 $e^{-1}/k!$，再与泊松分布律比较。',r'不能只看到 $e^{-2}$ 就说参数是 2；必须看完整归一化后的分布律。',r'$a=e$，$X\sim\mathrm{Poisson}(1)$。'),
('离散计数：翻译事件、识别分布','04-1',16,'至少正常多少个：改数损坏个数',r'80 个独立元件，200 小时内损坏概率为 0.05，求至少 78 个正常的概率（泊松近似）。',r'设损坏数 $D$，则 $D\sim B(80,0.05)$。',r'翻译事件：正常数 $\ge78\iff D\le2$。',r'以 $\lambda=4$ 近似，累加 $e^{-4}(1+4+4^2/2!)$。',r'按题给粗表 $e^{-4}=0.018$ 得 0.234；这是表值精度所致，不是精确泊松值的四舍五入。',r'近似式 $13e^{-4}\approx0.238$；按原题粗表为 0.234。'),
('离散计数：翻译事件、识别分布','04-3',18,'独立泊松和：参数相加，计数仍为 k',r'$X_1,X_2$ 独立且都服从 $\mathrm{Poisson}(\lambda)$，求和的分布。',r'先确认独立，才能直接用泊松可加性。',r'把参数相加，得 $S=X_1+X_2\sim\mathrm{Poisson}(2\lambda)$。',r'代入分布律；若用卷积，须对 $X_1=m,X_2=k-m$ 的所有 $m=0,\ldots,k$ 求和。',r'参数变成 $2\lambda$，不代表目标取值要写成 $2k$；只乘某一对概率也不是整个事件。',r'$P(S=k)=e^{-2\lambda}(2\lambda)^k/k!$，$k\ge0$。'),
('离散计数：翻译事件、识别分布','04-4a',19,'伯努利样本均值：去分母后数成功次数',r'3 个独立 $\mathrm{Bernoulli}(1/2)$ 样本，求 $P(\bar X>1/3)$。',r'去分母：$\bar X>1/3\iff S=X_1+X_2+X_3>1$。',r'识别 $S\sim B(3,1/2)$，且整数取值只需 2、3。',r'累加 $[\binom32+\binom33](1/2)^3$。',r'严格大于 1 不包含 1；不要把阈值 1/3 直接代入离散分布律。',r'$P(\bar X>1/3)=1/2$。'),
('离散计数：翻译事件、识别分布','04-4b',19,'比较 CDF：分段比概率，不比样本大小',r'$X\sim\mathrm{Bernoulli}(p)$，$Y\sim B(2,p)$，比较 $F_X,F_Y$。',r'按支持点 0、1、2 划分自变量 $z$ 的区间。',r'$0\le z<1$：比较 $1-p$ 与 $(1-p)^2$；$1\le z<2$：比较 1 与 $1-p^2$。',r'区间外两者相等，合并得 $F_X(z)\ge F_Y(z)$。',r'边缘 CDF 的大小不能推出给定联合模型下 $X\le Y$ 几乎处处；独立时 $P(X>Y)=p(1-p)^2$。',r'对所有 $z$，$F_X(z)\ge F_Y(z)$。'),
('离散计数：翻译事件、识别分布','04-5',20,'球入指定盒：二项分布的众数',r'100 个球独立等概率进入 40 个盒子，问指定盒子最可能有几个球。',r'把“进入指定盒子”看作成功，$p=1/40$。',r'球数 $X\sim B(100,1/40)$，计算 $(n+1)p=101/40$。',r'此值非整数，众数取下整，得 2；也可用相邻概率之比判断增减。',r'不是把均值四舍五入；若 $0<p<1$ 且 $(n+1)p=m$ 为整数，则 $m-1,m$ 都是众数。',r'最可能为 2 个球。'),
('单调与多对一变换：先求原像','02-2a',1,'递减立方根变换：反函数导数取绝对值',r'$f_X(x)=1/[\pi(1+x^2)]$，$Y=1-\sqrt[3]{X}$，求密度。',r'确认变换在全实轴单调递减，$Y$ 的范围仍为 $\mathbb R$。',r'解反函数 $x=(1-y)^3$，求 $|dx/dy|=3(1-y)^2$。',r'代入 $f_Y(y)=f_X((1-y)^3)\,3(1-y)^2$。',r'若走 CDF 法，递减变换会翻转不等号；密度不能带负号。',r'$f_Y(y)=\dfrac{3(1-y)^2}{\pi[1+(1-y)^6]}$，$y\in\mathbb R$。'),
('单调与多对一变换：先求原像','02-2b',1,'标准正态平方：左右两支都要收',r'$X\sim N(0,1)$，$Y=X^2$，求密度。',r'先定范围：$y<0$ 时 $F_Y(y)=0$。',r'$y\ge0$ 时，$Y\le y\iff-\sqrt y\le X\le\sqrt y$，故 $F_Y(y)=2\Phi(\sqrt y)-1$。',r'在 $y>0$ 上求导，写出密度并补区间外为 0。',r'非单调变换不能只取 $+\sqrt y$ 一支；通用路线是“CDF 定义 → X 事件 → 求概率 → 求导”。',r'$f_Y(y)=e^{-y/2}/\sqrt{2\pi y}$（$y>0$），其余取 0。'),
('单调与多对一变换：先求原像','880-2',23,'均匀变量取负对数：不等号翻转',r'$X\sim U(0,1)$，$Y=-2\ln X$。',r'由 $0<X<1$ 得 $Y>0$，先补 $y<0$ 的 CDF。',r'$y\ge0$ 时，$Y\le y\iff X\ge e^{-y/2}$。',r'利用均匀分布算区间概率 $1-e^{-y/2}$，再求导。',r'除以负数必须翻转不等号；用反函数公式时同样要取导数绝对值。',r'$F_Y(y)=1-e^{-y/2}$（$y\ge0$），$f_Y(y)=\tfrac12e^{-y/2}$（$y>0$）。'),
('单调与多对一变换：先求原像','880-3',24,'max(X,1/X)：两个约束变成交集',r'$X\sim\mathrm{Exp}(\lambda)$，$Y=\max(X,1/X)$，求 CDF。',r'由 $X>0$，先看出 $Y\ge1$，故 $y<1$ 时 CDF 为 0。',r'$y\ge1$ 时，同时解 $X\le y$ 与 $1/X\le y$，得到 $1/y\le X\le y$。',r'用指数 CDF 作差：$F_X(y)-F_X(1/y)$。',r'$X$ 与 $1/X$ 不是独立变量，不能把两个概率相乘。',r'$F_Y(y)=e^{-\lambda/y}-e^{-\lambda y}$（$y\ge1$），其余为 0。'),
('分段、取整与混合分布：找断点和点质量','03-2',4,'端点原子 + 区间均匀：先分配剩余质量',r'$P(X=-1)=1/8$，$P(X=1)=1/4$，余下概率条件均匀分布于 $(-1,1)$。',r'剩余质量为 $5/8$；区间长为 2，故区间内无条件密度为 $5/16$。',r'$-1\le x<1$ 时，CDF 为左端原子 $1/8$ 加积分 $5(x+1)/16$。',r'补 $x<-1$ 为 0、$x\ge1$ 为 1，并核对两端跳跃质量。',r'$1/2$ 是条件密度，不是区间内的无条件密度；$F(1)$ 要包含右端原子。',r'$F(x)=1/8+5(x+1)/16$（$-1\le x<1$），区间外分别为 0、1。'),
('分段、取整与混合分布：找断点和点质量','03-8',10,'分段变换含常值段：连续部分和原子分开算',r'$f_X(x)=x^2/9$（$0<x<3$）；$Y=3$（$X\le1$）、$2X$（$1<X<2$）、1（$X\ge2$）。另求 $P(X\le Y)$。',r'先算常值段：$P(Y=1)=19/27$，$P(Y=3)=1/27$。',r'按 Y 的断点 1、2、3、4 分段；连续段只积 $1<X\le y/2$，再加已进入的原子质量。',r'另问回到 X 的三段判断 $X\le g(X)$：前两段成立、第三段不成立，合并成 $X<2$。',r'常值段压成点质量，不能只套密度变换公式；在 $y=3$ 处必须加跳跃。',r'$F_Y(y)$ 五段依次为 $0$（$y<1$）、$19/27$（$1\le y<2$）、$y^3/216+2/3$（$2\le y<3$）、$y^3/216+19/27$（$3\le y<4$）、1（$y\ge4$）。$P(X\le Y)=8/27$。'),
('分段、取整与混合分布：找断点和点质量','03-9',11,'分段曲线求 CDF：逐支解不等式再合并',r'$X\sim\mathrm{Exp}(3)$；$Y=-X$（$X<1$），$Y=(X-1)^2-1$（$X\ge1$）。另求 $P(Y>-X+2)$。',r'Y 的最小值为 $-1$；按 $y<-1$、$-1\le y<0$、$y\ge0$ 分段。',r'中间段逐支求原像，合并为 $[-y,1+\sqrt{1+y}]$；非负段合并为 $(0,1+\sqrt{1+y}]$。',r'用指数 CDF 算区间概率；另问逐支解 $g(X)>-X+2$，最终得到 $X>2$。',r'必须把每个解与该支的 X 定义域相交；中间段左端是 $-y$，不是抛物线另一根。',r'$F_Y(y)=0$（$y<-1$）；$e^{3y}-e^{-3(1+\sqrt{1+y})}$（$-1\le y<0$）；$1-e^{-3(1+\sqrt{1+y})}$（$y\ge0$）。另问为 $e^{-6}$。'),
('分段、取整与混合分布：找断点和点质量','03-11',13,'把变量送入别人的 CDF：平台会压出原子',r'$X\sim\mathrm{Exp}(\lambda)$，$G$ 是 $U[0,1]$ 的 CDF，$Y=G(X)$。',r'把 $G$ 展开；因 $X>0$，实际为 $Y=\min(X,1)$。',r'$0\le y<1$ 时，$Y\le y\iff X\le y$；$y\ge1$ 时概率为 1。',r'算跳跃 $P(Y=1)=P(X\ge1)=e^{-\lambda}$，判断是混合分布。',r'$G$ 是连续但含平台的 CDF，不是阶梯 CDF；也不是 X 自己的 CDF，不能套均匀化。',r'$F_Y(y)=0$（$y<0$）、$1-e^{-\lambda y}$（$0\le y<1$）、1（$y\ge1$）。'),
('分段、取整与混合分布：找断点和点质量','04-2',17,'指数变量取整：整数值对应一段区间',r'$X\sim\mathrm{Exp}(1)$，$Y=\lfloor X+1\rfloor$，求分布律。',r'先列支持集 $k=1,2,\ldots$，再翻译 $Y=k\iff k-1\le X<k$。',r'积分或 CDF 作差：$P(Y=k)=e^{-(k-1)}-e^{-k}$。',r'整理为 $(e^{-1})^{k-1}(1-e^{-1})$，与从 1 开始的几何分布匹配。',r'映射图用来找区间；概率是密度曲线下的面积，不是区间长度。用 $P(Y=1)$ 检查参数。',r'$Y\sim\mathrm{Geom}(p)$（支持从 1 开始），$p=1-e^{-1}$。'),
('模型关系与参数：用期望、方差或生存概率','03-6',8,'泊松过程到等待时间：等待超过 t 等价于零次发生',r'齐次泊松过程中 $N(t)\sim\mathrm{Poisson}(\lambda t)$，T 为首次故障等待时间；已 8 小时无故障，再等 10 小时仍无故障。',r'翻译 $T>t\iff N(t)=0$，得 $P(T>t)=e^{-\lambda t}$。',r'取补集，得到 $T\sim\mathrm{Exp}(\lambda)$。',r'条件概率取比值：$P(T>18)/P(T>8)=e^{-10\lambda}$。',r'这里依赖齐次泊松过程模型；不能仅由某个时点的计数服从泊松分布，就推出所有间隔性质。',r'$F_T(t)=1-e^{-\lambda t}$（$t\ge0$），条件概率为 $e^{-10\lambda}$。'),
('模型关系与参数：用期望、方差或生存概率','03-7',9,'正态线性变换含同一参数：分开列均值方差',r'$X\sim N(a,a^2)$，$Y=aX+b\sim N(0,1)$，求 $a,b$。',r'均值方程：$EY=aEX+b=a^2+b=0$。',r'方差方程：$\operatorname{Var}(Y)=a^2\operatorname{Var}(X)=a^4=1$。',r'先得 $a=\pm1$，再代均值方程得 $b=-1$。',r'方差乘系数的平方；不能从 $a^4=1$ 漏掉负解。',r'$(a,b)=(1,-1)$ 或 $(-1,-1)$。'),
('模型关系与参数：用期望、方差或生存概率','03-10',12,'正态线性变换后用自己的 CDF：概率积分变换',r'$X\sim N(1,1)$，$Y=2X+1$；F 为 Y 的 CDF，$Z=F(Y)$。',r'由均值和方差得 $Y\sim N(3,4)$，按需写正态密度。',r'确认 F 是 Y 自己的连续 CDF；本题还严格递增，可在 $0<u<1$ 用反函数。',r'$P(Z\le u)=P(Y\le F^{-1}(u))=u$，再补两端。',r'不能把“任意 CDF 代入任意变量”都叫均匀化；普通反函数证明不要硬套 $u=0,1$。',r'$f_Y(y)=\frac1{2\sqrt{2\pi}}e^{-(y-3)^2/8}$；$Z\sim U(0,1)$。'),
('模型关系与参数：用期望、方差或生存概率','03-13',15,'正态区间概率对方差取最值：先标准化',r'$X\sim N(0,\sigma^2)$，固定 $0<a<b$，最大化 $P(a<X<b)$。',r'把目标写成 $P(\sigma)=\Phi(b/\sigma)-\Phi(a/\sigma)$，$\sigma>0$。',r'求导并令零：$P\prime(\sigma)=[a\varphi(a/\sigma)-b\varphi(b/\sigma)]/\sigma^2=0$；代正态密度后取对数。',r'解出唯一驻点；结合 $\sigma\to0^+,\infty$ 时概率都趋于 0，确定为最大值点。',r'先标准化能避开长篇积分号下求导；$0<a<b$ 是本题端点结论的重要条件。',r'最优 $\displaystyle\sigma^2=\frac{b^2-a^2}{2\ln(b/a)}$。'),
('模型关系与参数：用期望、方差或生存概率','04-6',21,'分类频数求无偏估计：期望对系数，方差合事件',r'$P(X=1,2,3)$ 依次为 $1-\theta,\theta-\theta^2,\theta^2$；n 次独立抽样频数为 $N_i$。令 $T=\sum a_iN_i$ 无偏估计 $\theta$，并求方差。',r'用 $EN_i=np_i$ 展开 $ET=n[a_1+(a_2-a_1)\theta+(a_3-a_2)\theta^2]$。',r'要求对所有 $\theta$ 恒等于 $\theta$，按常数、一次、二次项比较，得 $a_1=0,a_2=a_3=1/n$。',r'合并事件：$N_2+N_3$ 数的是 $X\in\{2,3\}$，成功概率为 $\theta$，故服从 $B(n,\theta)$，再除以 $n^2$ 求方差。',r'$N_1,N_2,N_3$ 并不独立；期望可直接相加，方差不能漏协方差。先合类最省事。',r'$T=(N_2+N_3)/n$，$\operatorname{Var}(T)=\theta(1-\theta)/n$。')
]
assert len(rows)==28
head='''# 02 随机变量｜题型检索与三步解法

> 这是一张**做题导航**，不是原解析副本。先看“识别”和三步做法，核对时再展开答案；完整题面、板书与长解析点每题的“原题与解析”。
> 范围：02习题、03 强化习题、04套卷阶段查漏、880；不含 01视频笔记。原来的 25 个记录块拆为 28 张卡片（含一张手写补题）。

**通用路线**：先认变量取值与题型 → 把目标转成 X 的事件或计数事件 → 算概率 → 需要密度时再求导。

'''
cats=list(dict.fromkeys(r[0] for r in rows))
head+='**题型入口**\n\n'+'\n'.join(f'- [[#{c}|{c}]]' for c in cats)+'\n'
parts=[head]; manifest={'version':1,'mode':'concise','target':target.as_posix(),'sources':hashes,'items':[],'images':[]}
for cat in cats:
 parts.append('\n## '+cat+'\n')
 for c,id,idx,title,setup,s1,s2,s3,trap,answer in rows:
  if c!=cat: continue
  block=L[idx]; source=block['source']; txt=Path(source).read_text(encoding='utf-8')
  hs=re.findall(r'^\s*#\s+(.+)$',txt,re.M)
  anchor=next((re.sub(r'!\[\[.*?\]\]','',h).strip() for h in hs if re.match(r'^'+re.escape(block['number'])+r'(?:\s|$)',h)),None)
  # A heading containing an embed is not a reliable simple heading anchor; link the original asset instead.
  if Path(source).stem=='880' and block['number']=='1': anchor=None
  link=source+('#'+anchor if anchor else '')
  assets=[im['path'] for im in images if im['item']==block['id']]
  prov=f'> 原题与解析：[[{link}|{Path(source).stem} · {block["number"]}]]'
  if not anchor and assets: prov+=f' · [[{assets[0]}|定位题图]]'
  parts.append(f'\n### {id}｜{title}\n\n{prov}\n\n**识别**：{setup}\n\n1. {s1}\n2. {s2}\n3. {s3}\n\n**易错**：{trap}\n\n> [!faq]- 核对结果\n> {answer}\n')
  manifest['items'].append({'id':id,'block_id':block['id'],'source':source,'source_link':link,'category':cat,'coverage':'独立题；同设定的小问一并覆盖'})
for im in images:
 manifest['images'].append({'path':im['path'],'source':next(b['source'] for b in L if b['id']==im['item']),'block_id':im['item'],'disposition':'source-linked','card_ids':[r[1] for r in rows if L[r[2]]['id']==im['item']]})
body='\n'.join(parts)
target.write_text(body,encoding='utf-8')
(w/'concise_ledger.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'target':target.as_posix(),'cards':len(rows),'categories':len(cats),'characters':len(body),'source_images':len(images)},ensure_ascii=False))