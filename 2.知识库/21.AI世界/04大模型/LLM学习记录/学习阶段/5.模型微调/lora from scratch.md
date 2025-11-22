# loralinear 函数
在初始化里，
- 最重要的是r，即低秩矩阵的维度，‘

```
这里的知识点应为，A的形状为（r，in_features）
```

- alpha，绝对低秩矩阵对模型参数的影响程度
- dropout，正则化率
- 使用nn.parameter(torch,empty)来初始化，为0

使用nn.init.normal_来进一步初始化矩阵（此刻填入数字）

冻结baselayer
忽略该张量的梯度计算，使用的是

```python
param.requires_grad = False

```

定义forward函数   输出self.base_layer(x) + lora_adjustment * scaling
# 替换函数
没有特殊字符串，也不是线性层，递归进入。
# QLoRA
- load_in_4bit
- bnb_4bit_use_double_quant
- bnb_4bit_quant_type
- bnb_4bit_compute_dtypew