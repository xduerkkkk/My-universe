from pathlib import Path
import json,hashlib,re
out=Path('.tmp/math-ode-20260906')
inv=json.loads((out/'inventory.json').read_text(encoding='utf-8'))
base=Path('2.知识库/20.North_star_ZJU/201.数学/01高等数学/06微分方程')
cards=[]
def add(id,cat,img,title,recognition,steps,trap,answer,coverage='',anchor=None,direct=False):
 a=inv['images'][img-1]
 heading=a['heading'].strip()
 if anchor is None:
  anchor=heading if heading!='(开头)' and '[' not in heading else ''
 source_link=a['source']+('#'+anchor if anchor else '')
 cards.append(dict(id=id,category=cat,image_index=img,title=title,recognition=recognition,steps=steps,trap=trap,answer=answer,coverage=coverage or recognition,source=a['source'],source_link=source_link,block_id=a['source']+'::'+a['heading'],direct=direct or not anchor))
A='一、给出多个解：做差、验独立、反推方程'
B='二、一阶非线性：先换整体或交换自变量'
C='三、缺项与变系数：降阶或凑乘积导数'
D='四、常系数非齐次：先判撞根，再设特解'
E='五、增量、函数关系与几何积分：先建立方程'
F='六、极限、平均值与有界周期：按所求组织解'
add('02-习2',A,1,'非齐次特解相减：先找齐次基底再代初值',r'$y_1=e^{3x}-xe^{2x},y_2=e^x-xe^{2x},y_3=-xe^{2x}$ 是同一二阶常系数非齐次方程的解，求满足 $y(0)=0,y\'(0)=1$ 的解。'.replace("\\'","'"),[r'相减得 $y_1-y_3=e^{3x},y_2-y_3=e^x$，两者线性无关。',r'写 $y=C_1e^{3x}+C_2e^x-xe^{2x}$。',r'代初值解 $C_1+C_2=0,\ 3C_1+C_2-1=1$。'],r'非齐次解不能任意线性组合；任意常数乘的是齐次基底。',r'$y=e^{3x}-e^x-xe^{2x}$。','15.2：三个特解及两个初始条件；与15.1独立拆卡。',direct=True)
add('03-1',A,17,'两个一阶齐次解不同：用指数因子判断是否相交',r'$P$ 在 $\mathbb R$ 连续且不恒为零，$y_1,y_2$ 是 $y\'+Py=0$ 的不同解；判断差为常数、差生成通解、差处处非零及比值为常数。'.replace("\\'","'"),[r'令 $E(x)=e^{-\int_0^xP(t)dt}>0$，写 $y_i=C_iE$，且 $C_1\ne C_2$。',r'差为 $(C_1-C_2)E$，处处非零，其任意常数倍覆盖全部解。',r'若差为常数，由差满足的齐次方程推出 $P\equiv0$，矛盾；当 $y_1\ne0$ 时比值为 $C_2/C_1$。'],r'“不同”不保证两个解都非零；比值结论必须保留分母非零条件。',r'错误项 A；B、C、D（附 $y_1\ne0$）正确。')
add('04-1',A,23,'三个非齐次解线性无关：系数和为一才留在原方程',r'$y_1,y_2,y_3$ 线性无关，均满足 $L[y]=y\'\'+p(x)y\'+q(x)y=f(x)$；求通解形式。'.replace("\\'","'"),[r'取 $Y_1=y_1-y_3,Y_2=y_2-y_3$，由线性性知 $L[Y_i]=0$。',r'若 $aY_1+bY_2=0$，则 $ay_1+by_2-(a+b)y_3=0$；原三解无关迫使 $a=b=0$。',r'用两独立齐次解加一个特解，写 $y=C_1Y_1+C_2Y_2+y_3$。'],r'齐次组合系数和为零；原非齐次组合系数和应为一。',r'D：$y=C_1y_1+C_2y_2+(1-C_1-C_2)y_3$。')
add('04-3',A,25,'方程缺 y 项：补上常数齐次解',r'$y\'\'+p(x)y\'=q(x)$ 有特解 $x^3$，对应齐次方程有解 $x^{-3}$，求通解。'.replace("\\'","'"),[r'对应齐次方程没有 $y$ 项，直接检验 $y=1$ 也是解。',r'在不含 $0$ 的区间上，$1,x^{-3}$ 线性无关，组成齐次基底。',r'写两独立常数的齐次组合，再加已知特解 $x^3$。'],r'无需先求 $p,q$；不要把 $x^3$ 当作齐次解。',r'$y=C_1x^{-3}+C_2+x^3$，在 $x\ne0$ 的区间上。')
add('04-4',A,26,'两个二阶齐次解：用朗斯基行列式验独立',r'$y_1,y_2$ 均满足 $y\'\'-y\'+y=0$；求 $C_1y_1+C_2y_2$ 能表示通解的充分条件。'.replace("\\'","'"),[r'计算 $W(x)=y_1y_2\'-y_1\'y_2$。'.replace("\\'","'"),r'若某点 $W(x_0)\ne0$，两解独立；本方程还满足 $W\'=W$，故全区间非零。'.replace("\\'","'"),r'二阶齐次解空间为二维，两独立解即可生成通解，选含 $W\ne0$ 的条件。'],r'不要全程除以 $y_1$：非零解函数仍可能有零点。',r'A：$y_1y_2\'-y_1\'y_2\ne0$。'.replace("\\'","'"))
add('03-5',A,22,'特解混有不同指数：分离系数反读特征根',r'$y\'\'+ay\'+by=ce^x$（$a,b,c$ 为常数）有特解 $y^*=e^{-x}(1+xe^{2x})$，求通解。'.replace("\\'","'"),[r'拆成 $e^{-x}+xe^x$；设特征多项式 $P(r)=r^2+ar+b$。',r'代入并比较 $e^{-x},xe^x,e^x$：$P(-1)=0,P(1)=0,P\'(1)=c$。'.replace("\\'","'"),r'得根 $-1,1$；将特解中的 $e^{-x}$ 吸收到齐次常数中。'],r'“含 $xe^x$ 就撞根”要结合右端只有 $ce^x$；不能脱离右端硬套。',r'$a=0,b=-1,c=2$；$y=C_1e^{-x}+C_2e^x+xe^x$。')
add('04-2',A,24,'与880同题再现：把指数特解中的齐次部分吸收',r'$y\'\'+ay\'+by=ce^x$ 的特解为 $e^{-x}+xe^x$，求通解；这是 03-5 的同题来源。'.replace("\\'","'"),[r'右端不含 $e^{-x}$，故 $1-a+b=0$。',r'代入 $xe^x$，比较 $xe^x$ 系数得 $1+a+b=0$，于是 $a=0,b=-1$。',r'齐次解为 $C_1e^{-x}+C_2e^x$；加特解后合并 $e^{-x}$ 系数。'],r'本卡保留“大观2”的检索入口，不把它统计为新的独立题。',r'$y=C_1e^{-x}+C_2e^x+xe^x$。','与03-5重复的完整题目来源，保留来源卡但唯一题目计数去重。')
add('04-13a',A,42,'三个解共享 xeˣ：做差找基底再求右端',r'$xe^x+e^{2x},\ xe^x+e^x,\ xe^x+e^{2x}-e^x$ 是某二阶非齐次线性方程的三个解，求该方程。',[r'用特解相减及线性组合，取齐次基底 $e^x,e^{2x}$。',r'设标准型 $y\'\'+p(x)y\'+q(x)y=f(x)$，代两基底得 $1+p+q=0,4+2p+q=0$，故 $p=-3,q=2$。'.replace("\\'","'"),r'从任一原特解扣除齐次部分，得特解 $xe^x$；代左端算出 $f=-e^x$。'],r'可以相减找结构；不能未经验证就认定系数是常数，也不能把任意差当作非齐次特解。',r'$y\'\'-3y\'+2y=-e^x$。'.replace("\\'","'"),'1997数二：三个指数型特解求原方程；独立于同节下一图。',direct=True)
add('04-13b',A,43,'给出成倍的两个解：先判断右端是否为零',r'$1,e^{-x},2e^{-x}$ 均为同一二阶常系数线性方程的解，求方程。',[r'由 $L[e^{-x}]=f$ 和 $L[2e^{-x}]=f$ 得 $2f=f$，因此 $f=0$。',r'于是 $1,e^{-x}$ 都是齐次解，对应根 $0,-1$。',r'写首项系数为一的方程，并把三解代回检查。'],r'题干说“线性”不等于“非齐次”；做差法与直接代入法都有效。',r'$y\'\'+y\'=0$。'.replace("\\'","'"),'1000强化28：1、e^-x、2e^-x求方程，包含“能否像上一题做差”的个人疑问。',direct=True)
add('04-14',A,44,'做差得到 x 与 x²：保留变系数再反推',r'$e^x,x+e^x,x^2+e^x$ 是某二阶非齐次线性方程的特解，求方程。',[r'相减得齐次解 $x,x^2$，设 $y\'\'+p(x)y\'+q(x)y=0$。'.replace("\\'","'"),r'代入得 $p+xq=0,\ 2+2xp+x^2q=0$；在 $x\ne0$ 上解得 $p=-2/x,q=2/x^2$。',r'同乘 $x^2$ 后将 $e^x$ 代入左端，求非齐次项。'],r'没写“常系数”就不能假定常数；也不代表系数一定非恒定。标准型只在不含 $0$ 的区间成立。',r'$x^2y\'\'-2xy\'+2y=(x^2-2x+2)e^x$。'.replace("\\'","'"))
add('02-习5',B,3,'e⁻ʸ 与 y′ 相乘：令 u=eʸ 化线性',r'求 $y\'+1=e^{-y}\sin x$ 的通解。'.replace("\\'","'"),[r'两边乘 $e^y$，得 $e^yy\'+e^y=\sin x$。'.replace("\\'","'"),r'令 $u=e^y$，解 $u\'+u=\sin x$；积分因子为 $e^x$。'.replace("\\'","'"),r'积分得 $u=\tfrac12(\sin x-\cos x)+Ce^{-x}$，取对数换回。'],r'$u=e^y$ 必须严格为正，不能把 $u\le0$ 的区间写进实解。',r'$y=\ln[\tfrac12(\sin x-\cos x)+Ce^{-x}]$，限方括号为正的区间。')
add('02-千4',B,8,'y′ 的系数对 x 一次：交换自变量解线性方程',r'求 $(2x-3xy^2-y^3)y\'+y^3=0$ 的通解。'.replace("\\'","'"),[r'先保留常值解 $y=0$；在 $y\ne0$ 的局部反解 $x=x(y)$，得 $\frac{dx}{dy}+(\frac2{y^3}-\frac3y)x=1$。',r'用积分因子 $\mu=y^{-3}e^{-1/y^2}$，凑 $(\mu x)\'=y^{-3}e^{-1/y^2}$（此处对 $y$ 求导）。'.replace("\\'","'"),r'积分得 $\mu x=\tfrac12e^{-1/y^2}+C$，再还原隐式关系；只取能定义可微 $y(x)$ 的分支。'],r'换自变量会除以 $y^3$，必须另查 $y=0$，不要直接丢掉。',r'$x=\tfrac12y^3+Cy^3e^{1/y^2}\ (y\ne0)$；另有 $y=0$。',anchor='4 换自变量')
add('02-千6',B,10,'sec y 与 tan y 同现：乘 cos y 换 sin y',r'求 $y\'=(x+1)\sec y-\tan y$ 的通解。'.replace("\\'","'"),[r'在 $\cos y\ne0$ 上乘 $\cos y$，得 $\cos y\,y\'+\sin y=x+1$。'.replace("\\'","'"),r'令 $u=\sin y$，解 $u\'+u=x+1$，即 $(e^xu)\'=(x+1)e^x$。'.replace("\\'","'"),r'积分还原为 $\sin y=x+Ce^{-x}$，选择连续分支。'],r'乘 $\cos y$ 后仍须保留原方程的限制；不能纳入 $\cos y=0$。',r'$\sin y=x+Ce^{-x}$，在 $|x+Ce^{-x}|<1$ 的适当分支上。',anchor='1000 题',direct=True)
add('03-2',B,18,'齐次换元后分离：先列被除掉的常值 u',r'$y\'=y/x+\tan(y/x)$，求满足 $y(1)=\pi/6$ 的解，并复盘漏解。'.replace("\\'","'"),[r'令 $u=y/x$，得 $xu\'=\tan u$；除以 $\tan u$ 前记下 $u=k\pi$。'.replace("\\'","'"),r'非常值分支积分 $\cot u\,du=dx/x$，得 $\sin(y/x)=Cx$；$C=0$ 可容纳全部 $y=k\pi x$。',r'代初值得 $C=1/2$；取经过 $u(1)=\pi/6$ 的分支，并排除 $x=0$ 和正切极点。'],r'漏掉的不只 $y=0$，而是 $y=k\pi x$；隐式公式还要选满足初值的分支。',r'$y=x\arcsin(x/2)$，该初值解的最大区间为 $0<x<2$。')
add('03-3',B,20,'x/y 指数伴随配套微分：先凑 d(yeˣ⁄ʸ)',r'求 $(1+e^{x/y})dx+e^{x/y}(1-x/y)dy=0\ (y>0)$ 的通解。',[r'识别 $d(ye^{x/y})=e^{x/y}dx+e^{x/y}(1-x/y)dy$。',r'原式即 $d(x+ye^{x/y})=0$，直接积分。',r'检验所得关系的微分与原式一致，并保留 $y>0$。'],r'$y>0$ 不代表 $x/y+e^{x/y}>0$；不必取对数，更不能把 $C$ 限成正数。',r'$x+ye^{x/y}=C$，$C\in\mathbb R$，$y>0$。')
add('04-5',B,27,'分离后出现平方和：常数范围与实解分支一起检查',r'判断 $y\'+x/y=0$ 的通解形式；选项为 $x^2\pm y^2=C^2$ 或 $x^2\pm y^2=C$，称 $C$ 为任意常数。'.replace("\\'","'"),[r'原方程要求 $y\ne0$；乘 $y$ 积分得 $x^2+y^2=K$。',r'实解必须 $K>0$，记 $K=R^2$，其中 $R>0$。',r'解成 $y=\pm\sqrt{R^2-x^2}$，在 $(-R,R)$ 内固定一个符号，排除端点。'],r'$C^2$ 只编码非负值，仍须排除 $C=0$；“$K>0$”与“$K$ 无限制”不是一回事。',r'按原题记法选 A；严格解族为 $x^2+y^2=R^2,\ R>0,\ y\ne0$。')
add('04-7a',B,31,'分母对 x 一次、对 y 高次：反解 x(y)',r'求 $y\'=\frac{y}{x+(y+1)^2}$ 的非恒定解。'.replace("\\'","'"),[r'在非恒定分支 $y\ne0$ 上反解，得 $\frac{dx}{dy}-\frac xy=\frac{(y+1)^2}{y}$。',r'用积分因子 $1/y$，化为 $\frac d{dy}(x/y)=1+2/y+1/y^2$。',r'积分后乘回 $y$，并检查原分母不为零。'],r'决定换元的是“对 $x$ 线性”，不是看到 $y$ 高次就一律交换。',r'$x=y^2+2y\ln|y|-1+Cy$；$y\ne0,\ x+(y+1)^2\ne0$。','同图i：880综合填空1非恒定解；与同图j独立拆卡。',direct=True)
add('04-7b',B,31,'y⁴ln y 不线性但 x 线性：反解并除以 y',r'求 $\frac{dy}{dx}=\frac{y}{x+y^4\ln y}$ 的通解。',[r'由 $\ln y$ 知 $y>0$；反解得 $\frac{dx}{dy}-\frac xy=y^3\ln y$。',r'乘 $1/y$，得 $\frac d{dy}(x/y)=y^2\ln y$。',r'分部积分 $\int y^2\ln y\,dy=\frac{y^3}3\ln y-\frac{y^3}9$，乘回 $y$。'],r'不要漏掉对数定义域，也不要把原方程分母为零的点当作解点。',r'$x=\frac{y^4}3\ln y-\frac{y^4}9+Cy$，$y>0,\ x+y^4\ln y\ne0$。','同图j：660第77题独立练习，原笔记同图i的解析不覆盖本题。',direct=True)
add('02-习6',C,4,'二阶方程缺 y：令 p=y′ 再积分',r'求 $xy\'\'+3y\'=0$ 的通解。'.replace("\\'","'"),[r'在不含 $0$ 的区间令 $p=y\'$，得 $xp\'+3p=0$。'.replace("\\'","'"),r'用积分因子凑 $(x^3p)\'=0$，所以 $p=C_1x^{-3}$，包括 $p=0$。'.replace("\\'","'"),r'再积分一次，保留第二个独立常数；把非零数因子 $-1/2$ 吸收进 $C_1$。'],r'“吸收常数”只能重命名，不能丢失第二个常数；通解区间不跨 $x=0$。',r'$y=C_1/x^2+C_2$（$x>0$ 或 $x<0$）。')
add('02-习8',C,5,'x²y″ 型欧拉方程：用 ln|x| 统一两侧换元',r'求 $x^2y\'\'-2y=x^2$ 的通解。'.replace("\\'","'"),[r'在 $x>0$ 或 $x<0$ 的固定区间令 $t=\ln|x|,\ Y(t)=y(x)$，则 $x^2y\'\'=Y\'\'-Y\'$。'.replace("\\'","'"),r'解 $Y\'\'-Y\'-2Y=e^{2t}$；根为 $2,-1$，右端与单根 $2$ 重合，设 $Y_p=At e^{2t}$，得 $A=1/3$。'.replace("\\'","'"),r'换回 $x$，在各侧分别重命名常数；不要穿过奇点。'],r'不能先默认 $x>0$ 再机械补绝对值；两侧解区间与常数必须分别理解。',r'$y=C_1x^2+C_2/x+\tfrac13x^2\ln|x|$，$x\ne0$ 的区间上。')
add('04-6',C,28,'系数导数恰配 y′：直接合并为乘积导数',r'求 $(x^2-1)dy+(2xy-\cos x)dx=0$，满足 $y(0)=1$ 的解。',[r'认出 $(x^2-1)y\'+2xy=[(x^2-1)y]\'$，故乘积导数等于 $\cos x$。'.replace("\\'","'"),r'积分得 $(x^2-1)y=\sin x+C$。',r'由 $y(0)=1$ 得 $C=-1$，取包含 $0$ 且避开 $\pm1$ 的区间。'],r'不必展开一阶通解公式；若用对数积分因子，应写 $\ln|x^2-1|$，而非在 $x=0$ 附近写 $\ln(x^2-1)$。',r'$y=(\sin x-1)/(x^2-1)$，初值解最大区间 $(-1,1)$。')
add('04-11a',C,36,'缺 y 且 y′ 系数为 2/x：先凑 (x²y′)′',r'求 $y\'\'+\frac2x y\'=x\ (x>0)$ 的通解。'.replace("\\'","'"),[r'两边乘 $x^2$，化为 $(x^2y\')\'=x^3$。'.replace("\\'","'"),r'积分得 $x^2y\'=x^4/4+C_1$，故 $y\'=x^2/4+C_1/x^2$。'.replace("\\'","'"),r'再次积分，把负号吸收入第一个常数，并保留第二个独立常数。'],r'手写中乘积求导第一项应为 $x^2y\'\'$；每积分一次增加一个常数。'.replace("\\'","'"),r'$y=x^3/12+C_1/x+C_2$，$x>0$。','大观11第一道独立题：900第六章数二A类16，含手写乘积导数解法。',direct=True)
add('04-11b',C,37,'已给 y=u/cos x：反写 u=y cos x 少算分式导数',r'按 $y=u/\cos x$ 化简 $y\'\'\cos x-2y\'\sin x+3y\cos x=e^x$，并求通解。'.replace("\\'","'"),[r'反写 $u=y\cos x$，求 $u\'\'=y\'\'\cos x-2y\'\sin x-y\cos x$。'.replace("\\'","'"),r'原方程变为 $u\'\'+4u=e^x$，得 $u=C_1\cos2x+C_2\sin2x+e^x/5$。'.replace("\\'","'"),r'除以 $\cos x$ 换回，并限定在 $\cos x\ne0$ 的区间。'],r'题目已给代换时，先看其乘积形式；无需对 $u/\cos x$ 连求两次商导数。',r'$y=\dfrac{C_1\cos2x+C_2\sin2x+e^x/5}{\cos x}$。','1988数二：代换化简与求通解两问；第二张为同题续解。',direct=True)
add('04-12',C,40,'已知齐次解 eˣ：令另一解为 ueˣ 降阶',r'$(2x-1)y\'\'-(2x+1)y\'+2y=0$ 有解 $e^x,u(x)e^x$；$u(-1)=e,u(0)=-1$。求 $u$ 及原方程通解。'.replace("\\'","'"),[r'代 $y=ue^x$，消去 $u$ 项，得 $(2x-1)u\'\'+(2x-3)u\'=0$。'.replace("\\'","'"),r'令 $p=u\'$，解得 $p=A(2x-1)e^{-x}$，积分为 $u=-A(2x+1)e^{-x}+B$。'.replace("\\'","'"),r'由两条件得 $A=1,B=0$；第二解是 $-(2x+1)$，与 $e^x$ 独立，组合写通解。'],r'已知一个齐次解，代换只保证消去 $u$ 项，不保证 $u\'$ 也消失；标准求解区间避开 $x=1/2$。'.replace("\\'","'"),r'$u=-(2x+1)e^{-x}$；$y=C_1e^x+C_2(2x+1)$，初始条件所在区间为 $x<1/2$。')
add('02-习1',D,1,'多项式加指数：右端拆开，分别判撞根',r'为 $y\'\'-4y\'+4y=x^2+8e^{2x}$ 选择待定系数特解的形式。'.replace("\\'","'"),[r'特征多项式为 $(r-2)^2$，根 $2$ 为二重根。',r'对 $x^2$，指数 $0$ 不撞根，设 $ax^2+bx+c$；低次项不能漏。',r'对 $8e^{2x}$，指数 $2$ 撞二重根，设 $dx^2e^{2x}$，将两部分相加。'],r'乘 $x^2$ 只作用于撞根的指数部分，不作用于整个右端。',r'B：$y_p=ax^2+bx+c+dx^2e^{2x}$。','15.1：选择特解形式；同一图片的15.2已另卡。',direct=True)
add('03-4',D,21,'右端 eˣ 但根为 −1：没撞根就设一次多项式',r'求 $y\'\'+2y\'+y=xe^x$ 满足 $y(0)=y\'(0)=0$ 的解。'.replace("\\'","'"),[r'特征根为 $-1$ 二重根，齐次解 $(C_1+C_2x)e^{-x}$；右端指数 $1$ 不撞根。',r'设 $y_p=(Ax+B)e^x$，比较系数 $4A=1,4A+4B=0$，得 $y_p=(x-1)e^x/4$。',r'合并通解再代两个初值，解得 $C_1=C_2=1/4$。'],r'令 $y=ue^x$ 仍合法，但不会只剩 $u\'\'$；完全消低阶项需选二重根指数 $e^{-x}$。'.replace("\\'","'"),r'$y=\tfrac14[(x+1)e^{-x}+(x-1)e^x]$。')
add('02-技1',D,15,'二重根与右端指数相同：指数换元后连积两次',r'源解析对应 $y\'\'-2y\'+y=2(3x^2-2)e^x$；求一个特解，并补出通解结构。'.replace("\\'","'"),[r'左端特征多项式为 $(r-1)^2$，令 $y=ue^x$。',r'代入消去 $u,u\'$，得 $u\'\'=6x^2-4$。'.replace("\\'","'"),r'积分两次得 $u=x^4/2-2x^2+C_1x+C_2$；只求一个特解时取常数为零。'],r'选择指数靠左端二重根，而不是无条件跟随右端；原图只有解析，不擅加初值。',r'$y_p=(x^4/2-2x^2)e^x$；通解再加 $(C_1x+C_2)e^x$。','计算技巧第一图只有解析：可还原方程与特解形式，没有可见初始条件。',anchor='',direct=True)
add('04-9',D,33,'右端 x+cos x：两种特解各算系数后叠加',r'求 $y\'\'+y=x+\cos x$ 的通解。'.replace("\\'","'"),[r'齐次根为 $\pm i$，齐次解 $C_1\cos x+C_2\sin x$。',r'对右端 $x$ 设 $Ax+B$ 得 $y_{p1}=x$；对 $\cos x$ 因共振设 $x(M\cos x+N\sin x)$。',r'分别代入求得 $M=0,N=1/2$，最后才把两特解与齐次解相加。'],r'两部分的系数分开求；共振补乘 $x$ 只属于三角项。',r'$y=C_1\cos x+C_2\sin x+x+\tfrac12x\sin x$。')
add('02-技2',D,16,'三角右端加负向有界：复指数求特解后筛齐次项',r'源解析对应 $y\'\'+4y\'+5y=8\cos x$，求 $x\to-\infty$ 时有界的解。'.replace("\\'","'"),[r'对复方程右端 $8e^{ix}$ 设 $z_p=Ke^{ix}$，由 $K(i^2+4i+5)=8$ 得 $K=1-i$。',r'取实部得到 $y_p=\cos x+\sin x$，再加齐次项 $e^{-2x}(C_1\cos x+C_2\sin x)$。',r'当 $x\to-\infty$，非零振幅的齐次项在一列点上无界，故 $C_1=C_2=0$。'],r'原图的“负向有界”条件不能被技巧讲解吞掉；$e^{-2x}$ 在负无穷方向增长。',r'唯一满足要求的解为 $y=\cos x+\sin x$。','第二张计算技巧解析含完整方程和x趋于负无穷有界条件，均保留。',anchor='',direct=True)
add('04-10',D,34,'变系数三角组合：用正交关系先求 g(x)',r'$u_1\cos x+u_2\sin x$ 解 $y\'\'+y=g(x)>0$；$u_1\'\cos x+u_2\'\sin x=0,(u_1\')^2+(u_2\')^2=1$。①给 $u_1(0)=1,u_2(0)=0$ 求 $u_1,u_2$；②求同方程满足 $y(0)=0,y\'(0)=1$ 的另一解。'.replace("\\'","'"),[r'按已知约束求导，得 $-u_1\'\sin x+u_2\'\cos x=g$；与约束联立解出 $u_1\'=-g\sin x,u_2\'=g\cos x$。'.replace("\\'","'"),r'平方相加得 $g^2=1$，由 $g>0$ 得 $g=1$；积分并代初值得 $u_1=\cos x,u_2=\sin x$。',r'于是常数 $1$ 是非齐次特解；写 $y=C_1\cos x+C_2\sin x+1$，代②的初值。'],r'$y\'\'+y=g(x)$ 不是总有常数特解；本题必须先证明 $g\equiv1$。源笔记视频定位在约2分20秒。'.replace("\\'","'"),r'① $u_1=\cos x,u_2=\sin x$；② $y=1-\cos x+\sin x$。','两问共享u1,u2及g的设置：求u1/u2；另一个初值解。')
add('04-15',E,46,'增量等式含高阶余项：除以 Δx 取极限',r'$\Delta y=\frac{y\Delta x}{1+x^2}+\alpha$，其中 $\alpha=o(\Delta x)$，$y(0)=\pi$；求 $y(1)$。',[r'固定 $x$，将增量式除以 $\Delta x$ 并取极限，得到 $y\'=y/(1+x^2)$。'.replace("\\'","'"),r'用初值写 $y=\pi e^{\int_0^xdt/(1+t^2)}=\pi e^{\arctan x}$。',r'代 $x=1$，利用 $\arctan1=\pi/4$。'],r'关键是 $\alpha/\Delta x\to0$；不能仅凭 $\alpha\to0$ 就丢掉余项。',r'D：$y(1)=\pi e^{\pi/4}$。')
add('04-16',E,47,'函数方程给 f′(0)：用差商建立微分方程',r'实函数满足 $f(x+h)=\frac{f(x)+f(h)}{1-f(x)f(h)}$，且 $f\'(0)=1$；求 $f$。关系在相关自变量及分母有意义时成立。'.replace("\\'","'"),[r'令两自变量为零，得 $f(0)=0$；由在零点可导知 $f(h)\to0$。',r'整理差商为 $\frac{f(h)}h\frac{1+f(x)^2}{1-f(x)f(h)}$，取极限得 $f\'(x)=1+f(x)^2$。'.replace("\\'","'"),r'分离并用初值积分：$\arctan f(x)=x$，选含零的连续分支。'],r'$\tan x$ 不能作为全实轴处处有定义的实函数解；只在允许的区间及加法关系有意义时使用。',r'$f(x)=\tan x$；含 $0$ 的最大连续解区间为 $(-\pi/2,\pi/2)$。')
add('02-习10',E,6,'圆域二重积分含径向 f：极坐标后求导',r'$f$ 在 $[0,\infty)$ 连续，满足 $f(t)=e^{4\pi t^2}+\iint_{x^2+y^2\le4t^2}f(\tfrac12\sqrt{x^2+y^2})\,dxdy$，求 $f$。',[r'用极坐标及 $u=r/2$，积分化为 $2\pi\int_0^{2t}f(r/2)r\,dr=8\pi\int_0^tuf(u)du$。',r'连续性保证积分项可导，故 $f\'-8\pi tf=8\pi te^{4\pi t^2}$；从原式 $t=0$ 得 $f(0)=1$。'.replace("\\'","'"),r'乘 $e^{-4\pi t^2}$，积分 $(fe^{-4\pi t^2})\'=8\pi t$，代初值。'.replace("\\'","'" )],r'面积微元有 $r$，$r=2u$ 又带来两个因子2；初值要回原积分式取。',r'$f(t)=(1+4\pi t^2)e^{4\pi t^2}$，$t\ge0$。')
add('02-千8',E,11,'注水体积与水面面积速率：引入水深消去时间',r'$y=f(z)\ge0\ (z\ge0)$ 绕 $z$ 轴生成容器；注水率 $dV/dt=3$，水面面积增长率 $dS/dt=\pi$，底面积 $16\pi$，求母线 $f$。',[r'设水深 $h(t)$，写 $S(h)=\pi f(h)^2$，$V(h)=\int_0^h\pi f(z)^2dz$。',r'由链式法则 $dV/dt=S\,dh/dt=3$，及 $dS/dt=(dS/dh)(dh/dt)=\pi$，消去 $t$ 得 $dS/dh=(\pi/3)S$。',r'用 $S(0)=16\pi$ 得 $S=16\pi e^{\pi h/3}$，取非负半径并把 $h$ 换回 $z$。'],r'动态上限 $h(t)$ 与积分哑变量 $z$ 分开；最后半径指数是面积指数的一半。',r'$f(z)=4e^{\pi z/6}$，$z\ge0$。','1000题8完整容器建模题；图片上沿上一题“(2)求斜渐近线”缺少题干，单独登记不编造。',anchor='1000 题',direct=True)
add('02-习11',F,7,'要求三阶无穷小：先消常数、一次与二次项',r'对 $y^{(4)}-y^{(3)}+y\'\'-y\'=0$，①求通解；②求 $x\to0$ 时为 $x$ 的三阶无穷小的解。'.replace("\\'","'"),[r'特征多项式 $r(r-1)(r^2+1)$ 给出 $y=C_0+C_1e^x+C_2\cos x+C_3\sin x$。',r'三阶无穷小要求 $y(0)=y\'(0)=y\'\'(0)=0$；解出 $C_2=C_1,C_3=-C_1,C_0=-2C_1$。'.replace("\\'","'"),r'再验三次系数：$e^x+\cos x-\sin x-2=x^3/3+O(x^4)$，因此剩余系数必须非零。'],r'“三阶”要求 $y/x^3$ 趋于非零有限值，不是默认趋于1，更不能选零解。',r'①通解见步骤1；② $y=C(e^x+\cos x-\sin x-2),\ C\ne0$。','15.11两个子问：四阶方程通解；三阶无穷小解族。',anchor='习题',direct=True)
add('02-千5',F,9,'(x+y)² 与过原点：先换 u=x+y，再算幂指极限',r'曲线过原点，满足 $y\'=(x+y)^2$；求 $\lim_{x\to0^+}[y(x)]^x$。'.replace("\\'","'"),[r'令 $u=x+y$，得 $u\'=1+u^2,u(0)=0$，所以 $u=\tan x,y=\tan x-x$。'.replace("\\'","'"),r'由 $y\sim x^3/3>0$（$x\to0^+$），把幂指式写成 $\exp[x\ln y]$。',r'用 $x\ln y=x(3\ln x-\ln3+o(1))\to0$ 求原极限。'],r'不是看 $y\to0$ 就判结果为0；$0^0$ 型要取对数并确认右侧正性。',r'$\displaystyle\lim_{x\to0^+}[y(x)]^x=1$。',anchor='1000 题',direct=True)
add('04-8',F,32,'解比 x² 更高阶：泰勒消项确定两个常数',r'$\varphi$ 满足 $y\'\'-y=x^2$，且 $\varphi(x)=o(x^2)\ (x\to0)$；求 $\varphi$。'.replace("\\'","'"),[r'齐次解为 $C_1e^x+C_2e^{-x}$，设二次多项式特解得 $-x^2-2$。',r'展开通解：常数项 $C_1+C_2-2$、一次项 $C_1-C_2$ 必须为零，得 $C_1=C_2=1$。',r'继续验二次项抵消，实际余项为 $x^4/12+O(x^6)$，确实是 $o(x^2)$。'],r'高阶条件不只是 $y(0)=0$；定常数后还要核验所要求的阶数。',r'A：$\varphi(x)=e^x+e^{-x}-x^2-2$。')
add('02-千11',F,14,'欧拉型初值加平均值：换元定常数，积分保留 dx',r'$2xy\'-4y=2\ln x-1,\ y(1)=1/4$，求 $y$ 在 $[1,e]$ 上的平均值。'.replace("\\'","'"),[r'令 $t=\ln x,Y(t)=y(e^t)$，得 $2Y\'-4Y=2t-1$，解为 $Y=Ce^{2t}-t/2$。'.replace("\\'","'"),r'初值同步变为 $Y(0)=1/4$，得 $C=1/4$，换回 $y=x^2/4-\ln x/2$。',r'算 $\bar y=\frac1{e-1}\int_1^e y(x)dx$；若留在 $t$ 域，应积分 $Y(t)e^t$，范围 $0$ 至 $1$。'],r'换元求平均值不能漏 $dx=e^tdt$；分母仍是原区间长度 $e-1$。',r'$\bar y=\dfrac{e^3-7}{12(e-1)}$。',anchor='1000 题',direct=True)
add('02-千10',F,12,'抽象右端只给界：写成变上限积分再放缩',r'$\varphi$ 连续且 $|\varphi|\le k$，$y\'+y=\varphi(x),y(0)=0$；求特解并证 $x\ge0$ 时 $|y(x)|\le k(1-e^{-x})$。'.replace("\\'","'"),[r'乘 $e^x$，从 $0$ 积至 $x$，得 $y=e^{-x}\int_0^x e^t\varphi(t)dt$。',r'对 $x\ge0$ 用三角不等式：$|y|\le e^{-x}\int_0^x e^t|\varphi(t)|dt$。',r'代入上界 $k$ 并积分 $e^t$，得到所需估计。'],r'抽象函数不必求显式原函数；积分上下限方向决定能否直接这样放缩。',r'$y=e^{-x}\int_0^xe^t\varphi(t)dt$；$|y(x)|\le k(1-e^{-x})\ (x\ge0)$。',anchor='1000 题',direct=True)
add('04-11c',F,39,'右端趋于常数：指数积分核给极限，再代回求二阶导',r'$f$ 在 $[0,\infty)$ 连续且 $f(x)\to b$，$a>0$。①$y\'+ay=f$ 求 $\lim y$；②$y\'\'+ay\'=f$ 求 $\lim y\',\lim y\'\'$。'.replace("\\'","'"),[r'对①写 $y-b/a=e^{-ax}(y(0)-b/a)+\int_0^xe^{-a(x-t)}[f(t)-b]dt$。',r'选 $T$ 使 $t\ge T$ 时 $|f(t)-b|\le\varepsilon$；把积分拆为 $[0,T]$ 与 $[T,x]$：前段趋零，后段绝对值不超过 $\varepsilon/a$。',r'得 $y\to b/a$；②令 $p=y\'$ 套①，再由 $y\'\'=f-ay\'$ 求极限。'.replace("\\'","'" )],r'不能由 $y\'$ 有极限直接断言 $y\'\'\to0$；这里必须用原微分方程。'.replace("\\'","'"),r'① $\lim y=b/a$；② $\lim y\'=b/a,\ \lim y\'\'=0$。'.replace("\\'","'"),'例4.3两问共享f连续趋b和a>0；包含手写洛必达尝试，以积分拆段法统一保证条件。',direct=True)
add('04-17a',F,48,'全实轴有界与周期：选负无穷积分下限',r'$f$ 在 $\mathbb R$ 连续有界。①证 $y\'+y=f(x)$ 有全实轴有界解；②若 $f$ 以 $T>0$ 为周期，证所构造解也以 $T$ 为周期。'.replace("\\'","'"),[r'设 $|f|\le M$，先证 $\int_{-\infty}^xe^tf(t)dt$ 绝对收敛，再构造 $y_*(x)=e^{-x}\int_{-\infty}^xe^tf(t)dt$。',r'求导验证方程，并估计 $|y_*|\le e^{-x}M\int_{-\infty}^xe^tdt=M$。',r'对 $y_*(x+T)$ 的积分令 $t=s+T$，用 $f(s+T)=f(s)$ 得 $y_*(x+T)=y_*(x)$。'],r'改积分下限需同步改常数且保证收敛；下限 $-\infty$ 是为消掉负向增长项，不是“一律令C=0”。',r'$y_*=\int_{-\infty}^xe^{-(x-t)}f(t)dt$ 有界且继承周期；全实轴有界解唯一，因为两解之差为 $Ce^{-x}$。','例4.4：有界解存在与继承周期两问；保留积分下限与常数转换的个人卡点。',direct=True)
add('04-17b',F,49,'所有齐次解趋零：转成非负积分趋于正无穷',r'$a(t)\ge0$ 且在 $[0,\infty)$ 连续；证 $x\'+a(t)x=0$ 的每个解都趋于零，当且仅当 $\int_0^\infty a(t)dt$ 发散。'.replace("\\'","'"),[r'写所有解 $x(t)=Ce^{-A(t)}$，其中 $A(t)=\int_0^ta(s)ds$，含 $C=0$。',r'充分性：$a\ge0$ 使 $A$ 单调不减，积分发散即 $A(t)\to+\infty$，从而每个解趋零。',r'必要性：取非零解如 $C=1$，由 $e^{-A(t)}\to0$ 推出 $A(t)\to+\infty$。'],r'不能用零解证明必要性；非负条件将“发散”明确成趋于 $+\infty$。',r'$\forall C,\ x(t)\to0\iff\int_0^ta(s)ds\to+\infty$。','题21(I)：非负变系数齐次方程解衰减充要条件；与II设置不同独立成卡。',direct=True)
add('04-17c',F,49,'半轴上所有解有界：保留初值项并估计卷积',r'$a>0$ 为常数，$f$ 在 $[0,\infty)$ 连续有界；证 $x\'+ax=f(t)$ 的所有解在该半轴有界。'.replace("\\'","'"),[r'设 $|f|\le M$，写 $x(t)=x(0)e^{-at}+\int_0^te^{-a(t-s)}f(s)ds$。',r'取绝对值，得 $|x(t)|\le |x(0)|e^{-at}+\frac Ma(1-e^{-at})$。',r'因 $0<e^{-at}\le1$，右端为两个常数的凸组合，至多 $\max\{|x(0)|,M/a\}$。'],r'“每个解各自有界”不代表所有初值共享同一个上界；半轴无需特选常数消项。',r'$|x(t)|\le\max\{|x(0)|,M/a\}$（$t\ge0$）。','题21(II)：常系数强迫方程所有解半轴有界，与I独立成卡。',direct=True)
add('04-18',F,50,'周期系数与首尾值相同：平移做差用唯一性',r'$P,Q$ 在 $\mathbb R$ 连续且以 $T>0$ 为周期，$y$ 解 $y\'+P(x)y=Q(x)$；判断 $y(0)=y(T)$ 是否为 $y$ 以 $T$ 为周期的充要条件。'.replace("\\'","'"),[r'必要性直接由周期定义得 $y(0)=y(T)$。',r'为证充分性，令 $z(x)=y(x+T)-y(x)$；利用 $P,Q$ 的周期性得 $z\'+P(x)z=0$。'.replace("\\'","'"),r'由 $z(0)=0$，唯一性（或积分因子）给出 $z\equiv0$，故 $y(x+T)=y(x)$。'],r'一般函数两点取值相同不能推出周期；这里还用到了同一线性方程及零初值唯一性。',r'C：充要条件。')

# Normalize escaped primes in all user-facing math, and render in recognition categories.
for c in cards:
 for k in ['recognition','trap','answer']:
  c[k]=c[k].replace("\\'", "'")
 c['steps']=[s.replace("\\'", "'") for s in c['steps']]
assert len(cards)==44,len(cards)
head='''# 微分方程｜题型检索与二刷卡片

> [!abstract] 使用方式
> 先看标题和“识别”，遮住核对结果，按步骤口述第一步；完整题图、长推导和其他解法留在源笔记。
> **编号**：02-习＝章节习题，02-千＝1000题，02-技＝原计算技巧；03＝880，04＝大观。字母后缀表示同节拆出的独立题。
> **范围**：44张来源卡，对应43道不重复的完整题（03-5与04-2同题）；51张源图均保留，通过原笔记访问。本页不重复嵌图。
> **缺题干说明**：02-千8原图上沿仅残留上一题“(2)求斜渐近线”，缺少曲线定义，未据此编造题卡；两张“计算技巧”按可见解析还原，不补造初值。

'''
text=head+'\n'.join('- [[#'+cat+']]' for cat in [A,B,C,D,E,F])+'\n\n'
for cat in [A,B,C,D,E,F]:
 text+='## '+cat+'\n\n'
 for c in [x for x in cards if x['category']==cat]:
  a=inv['images'][c['image_index']-1]
  text+='### '+c['id']+'｜'+c['title']+'\n\n'
  text+='> 原题与解析：[['+c['source_link']+'|'+c['id']+' · 原笔记]]'
  if c['direct']:text+='；[['+a['path']+'|原题图／解析图]]'
  text+='\n\n**识别**：'+c['recognition']+'\n\n'
  text+='\n'.join(str(i)+'. '+s for i,s in enumerate(c['steps'],1))+'\n\n'
  text+='**易错**：'+c['trap']+'\n\n> [!faq]- 核对结果\n> '+c['answer']+'\n\n'

# All image occurrences in each original block are attached to all covered exercises in that block.
images=[]
for a in inv['images']:
 block=a['source']+'::'+a['heading']
 ids=[c['id'] for c in cards if c['block_id']==block]
 assert ids,(a,block)
 images.append(dict(path=a['path'],source=a['source'],block_id=block,disposition='source-linked',card_ids=ids,sha256=a['sha256'],inventory_index=a['index']))
items=[{k:c[k] for k in ['id','block_id','source','source_link','category','coverage']} for c in cards]
ledger=dict(version=1,mode='concise',target=(base/'05题型总结.md').as_posix(),sources=inv['sources'],items=items,images=images,
 target_before_sha256='af131863089dfc8a07b108f4ccbefd91f12370b99de11766993d72cbeda17b81',
 backup='.tmp/math-ode-20260906/05题型总结-重构前备份.md',
 duplicates=[dict(card_ids=['03-5','04-2'],reason='同一题目在两份原笔记出现，保留双入口')],
 excluded_fragments=[dict(image_index=11,text='(2)求曲线y(x)的斜渐近线',reason='前题裁切残片；缺少曲线定义，未伪造条件或答案。',disposition='source-linked')],
 annotations=['分离变量遗漏y=kπx而不只y=0；原方程极点及初值分支必须保留','常数重命名不能改变取值范围或漏掉独立常数','x/y指数凑微分避免不合法地移除对数绝对值','欧拉代换在x>0与x<0分别成立，不能跨越0','原04-15、16属于建立方程而非特解反推','04-13做差和代入均可用；不保留原文“复杂右端使代入法卡死”的错误说法','未注明常系数只是不允许预设，不意味着一定变系数','换元后可同步定初值，平均值需dx=e^tdt及原区间长度','有界解选择积分下限需保证收敛并同步定常数','原视频约2分20秒的位置保留在04-10卡，视频地址仍在未修改源笔记'],
 counts=dict(source_notes=3,image_occurrences=51,source_cards=44,unique_complete_exercises=43))
for p,h in inv['sources'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h
for a in images:assert hashlib.sha256(Path(a['path']).read_bytes()).hexdigest()==a['sha256']
assert '\ufffd' not in text and '????' not in text and not re.search(r'\\u[0-9a-fA-F]{4}',text)
(out/'manifest.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'cards.json').write_text(json.dumps(cards,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'05题型总结-候选.md').write_text(text,encoding='utf-8')
print('CANDIDATE',len(text),'characters;',len(cards),'cards; images',len(images))
print(text[:650])
