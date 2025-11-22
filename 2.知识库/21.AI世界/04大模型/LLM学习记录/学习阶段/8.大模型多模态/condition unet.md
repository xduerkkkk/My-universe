# 目标
传统的diffusion 是经过训练后 自己预测杂乱无章图片中的噪音，然后一点一点地去除。  着叫无条件生成， 他会生成什么样的图片，我们也不知道，是取决于训练时图集。 图集全是猫图＋噪声的图片， 他就倾向于从噪声中还原出猫。
那么问题来了，我们怎么做到给模型说“猫”，然后模型真的画出我们想要的动物：”猫“呢？
我们已经学习过传统unet。
在前几版的stable diffusion的架构中， 仅仅是在unet架构中，加入crossattention。就达到了我们”说啥画啥“的效果。
我们不妨先回顾一下unet的架构和数据流动。
# 扩散模型原理回顾

## 模型架构
### Block
是标准的“卷积+归一化+激活”  输出维度dim_out，是在做一个升维，可以理解为理解图片
### mlp
mlp  激活+全连接（Linear） 输出的维度仍然是dim_out 
可以理解为消化一下上一步dimout的知识


### ResnetBlock
用到了刚才的**block**和**mlp**
1. Block1
2. mlp  通过rearrange注入时间给上一步输出的图像向量
3. Block2 
4. 加残差
- 残差是最初的x映射到dim_out的样子
是unet网络的核心模块

### time_mlp
位置编码+线性层+加激活层+线性层  维度最终仍是time_dim
```
self.time_mlp = nn.Sequential(

                SinusoidalPositionEmbeddings(dim),

                nn.Linear(dim, time_dim),

                nn.GELU(),

                nn.Linear(time_dim, time_dim),

            )
```

### unet
1. 下采样-->缩小维度（压缩）
2. 上采样-->扩大维度（还原）

unet的下采样，是先经过block、attention后，保存当前图的高清特征，全局特征，然后再下采样缩小。
结束后，每次上采样前，先把之前保存的特征添加到当前向量，再上采样。
时间步，是每一步都存在的。
这样，势必最后一次下采样前保存的特征，会用在第一次上采样。这叫跳跃连接。

初始化下采样：
1. block1  升维
2. block2 维度不变
3. norm归一化
4. attention 图像自我理解
5. 下采样，降低图片分辨率


进入mid_dim环节，
1. block1 维度不变
2. 归一化
3. attention，图像自我理解
4. 加残差
5. block2 维度不变


初始化上采样
1. block1 升维
2. block2 维度不变
3. norm归一化
4. 上采样，增高图片分辨率


## 关键功能
### 上采样、下采样
名字来源于**空间分辨率的变化方向**，而不是通道数的变化！

```
# 上采样

def Upsample(dim):

    return nn.ConvTranspose2d(dim, dim, 4, 2, 1)

  

# 下采样

def Downsample(dim):

    return nn.Conv2d(dim, dim, 4, 2, 1)
```


### attention
- 在init中，qkv都来自图像，并且之前在图像上作qkv的生成。使用的是
```
self.to_qkv = nn.Conv2d(dim, hidden_dim * 3, 1, bias=False)
```
dim是输入通道，即我们attention要服务的对象‘x’的dim， hidden_dim * 3是输出通道数
`1` 代表卷积核大小为1×1
- 在forward函数里， 就是标准的attention计算过程。
最后通过self.to_out 将维度还原。 

### SinusoidalPositionEmbeddings
位置编码，用来实现时间步的注入

## 数据流动

定义


# Conditional unet的升级
那我们升级在哪呢？
我们应该能发现，其实unet有attention，但是，这个attention是自己跟自己玩！可能图片中左眼留意一下右眼在哪里，是这么个作用。
那我们进阶一下，不要qkv都是自己
如果让q是外部的文字
kv是图片的话，不就能联系起来二者吗

```
+-----------------+ (Q)
|  图像特征 (x)   | -----------+
+-----------------+            |
                               v
                       +-----------------+
                       | Cross-Attention | --> 输出 (融合了文本信息的图像特征)
                       +-----------------+
                               ^
                               |
+-----------------+ (K, V)     |
|  文本特征 (context)| ----------+
+-----------------+
```



```
Input: (x, time, context) 
| 
[init_conv] | [Down Block 1 + Cross-Attention] -> h1 (存入仓库) 
| 
[Downsample]
|
[Down Block 2 + Cross-Attention] -> h2 (存入仓库) 
| ... (下采样) ... 
| 
[Mid Block + Cross-Attention] 
|
... (上采样) ... 
| 
[Upsample] <- [cat(x, h2)] (取出仓库) 
| 
[Up Block 1 + Cross-Attention] 
| 
...
```
