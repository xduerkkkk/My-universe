# 公式

$$\hat{\mathbf{y}} = \mathrm{softmax}(\mathbf{o})\quad \text{其中}\quad \hat{y}_j = \frac{\exp(o_j)}{\sum_k \exp(o_k)}$$

  

这里，对于所有的$j$总有$0 \leq \hat{y}_j \leq 1$。

因此，$\hat{\mathbf{y}}$可以视为一个正确的概率分布。

softmax运算不会改变未规范化的预测$\mathbf{o}$之间的大小次序，只会确定分配给每个类别的概率。

因此，在预测过程中，我们仍然可以用下式来选择最有可能的类别。

  

$$

\operatorname*{argmax}_j \hat y_j = \operatorname*{argmax}_j o_j.

$$

  

尽管softmax是一个非线性函数，但softmax回归的输出仍然由输入特征的仿射变换决定。

因此，softmax回归是一个*线性模型*

**指数函数的作用**

- **拉大数值差异**：指数函数​ 会放大高分值的权重，抑制低分值，使概率分布更显著（例如输入 [2,1,0.1] 经 Softmax 变为 [0.7, 0.2, 0.1]） 。
- **导数简化**：指数函数求导方便，便于反向传播（梯度计算仅需概率与标签的差值）

### 小结
- softmax运算获取一个向量并将其映射为概率。
    
- softmax回归适用于分类问题，它使用了softmax运算中输出类别的概率分布。
    
- 交叉熵是一个衡量两个概率分布之间差异的很好的度量，它测量给定模型编码数据所需的比特数。

## 用法
- **`num_inputs`**：
    
    - 输入特征的数量。对于 FashionMNIST 数据集，每张图像是 28×28 的灰度图像，因此输入特征数量为 28×28=784。




这段代码定义了一个函数 `train_epoch_ch3`，用于训练一个深度学习模型在一个迭代周期（epoch）内的行为。它涵盖了模型训练过程中的主要步骤，包括前向传播、损失计算、反向传播和参数更新。下面我将逐行解释这段代码的语法和功能。

---
# **训练函数定义**
def train_ch3(net, train_iter, test_iter, loss, num_epochs, updater):  #@save

```python
    animator = Animator(xlabel='epoch', xlim=[1, num_epochs], ylim=[0.3, 0.9],

                        legend=['train loss', 'train acc', 'test acc'])

    for epoch in range(num_epochs):

        train_metrics = train_epoch_ch3(net, train_iter, loss, updater)

        test_acc = evaluate_accuracy(net, test_iter)

        animator.add(epoch + 1, train_metrics + (test_acc,))

    train_loss, train_acc = train_metrics

    assert train_loss < 0.5, train_loss

    assert train_acc <= 1 and train_acc > 0.7, train_acc

    assert test_acc <= 1 and test_acc > 0.7, test_acc```
   
```python
def train_epoch_ch3(net, train_iter, loss, updater):
```
- **`net`**：模型，通常是一个继承自 `torch.nn.Module` 的神经网络。
- **`train_iter`**：训练数据的迭代器（例如 `DataLoader`），用于提供训练数据和标签。
- **`loss`**：损失函数，用于衡量模型预测值与真实标签之间的差异。
- **`updater`**：优化器，用于更新模型的参数。可以是 PyTorch 内置的优化器（如 `torch.optim.SGD`），也可以是自定义的优化器。

---

### **设置模型为训练模式**
```python
if isinstance(net, torch.nn.Module):
    net.train()
```
- 如果 `net` 是一个 `torch.nn.Module` 实例，则调用 `net.train()` 将模型设置为训练模式。这会影响某些层的行为（如 `Dropout` 和 `BatchNorm`），使它们在训练时启用特定功能。

---

### **初始化训练指标**
```python
metric = Accumulator(3)
```
- `Accumulator` 是一个辅助类，用于累加训练过程中的多个指标。这里初始化为存储 3 个指标：
  1. 损失总和。
  2. 准确度总和。
  3. 样本总数。

---

### **训练循环**
```python
for X, y in train_iter:
```
- 遍历训练数据迭代器 `train_iter`，每次获取一批输入数据 `X` 和对应的标签 `y`。

---

### **前向传播**
```python
y_hat = net(X)
```
- 将输入数据 `X` 传递给模型 `net`，得到预测输出 `y_hat`。

---

### **计算损失**
```python
l = loss(y_hat, y)
```
- 使用损失函数 `loss` 计算模型预测值 `y_hat` 与真实标签 `y` 之间的损失值 `l`。

---

### **更新参数**
```python
if isinstance(updater, torch.optim.Optimizer):
    updater.zero_grad()
    l.mean().backward()
    updater.step()
else:
    l.sum().backward()
    updater(X.shape[0])
```
- **PyTorch 内置优化器**：
  - 如果 `updater` 是 `torch.optim.Optimizer` 的实例：
    1. 调用 `updater.zero_grad()` 清空之前的梯度。
    2. 调用 `l.mean().backward()` 计算损失的平均值的梯度（`l.mean()` 是为了确保损失值是一个标量）。
    3. 调用 `updater.step()` 更新模型参数。
- **自定义优化器**：
  - 如果 `updater` 是自定义的优化器：
    1. 调用 `l.sum().backward()` 计算损失的总和的梯度（`l.sum()` 是为了确保损失值是一个标量）。
    2. 调用 `updater(X.shape[0])` 更新模型参数，其中 `X.shape[0]` 是当前批次的样本数量。

---

### **累加训练指标**
```python
metric.add(float(l.sum()), accuracy(y_hat, y), y.numel())
```
- 调用 `metric.add` 累加以下指标：
  1. 当前批次的损失总和 `float(l.sum())`。
  2. 当前批次的准确度 `accuracy(y_hat, y)`。
  3. 当前批次的样本总数 `y.numel()`（`y.numel()` 返回 `y` 中的元素总数）。

---

### **返回训练损失和训练精度**
```python
return metric[0] / metric[2], metric[1] / metric[2]
```
- 返回两个指标：
  1. **平均训练损失**：`metric[0] / metric[2]`，即损失总和除以样本总数。
  2. **平均训练精度**：`metric[1] / metric[2]`，即准确度总和除以样本总数。

---

### **总结**
这段代码实现了一个完整的训练循环，用于在一个 epoch 内训练模型。它涵盖了以下关键步骤：
1. **设置模型为训练模式**。
2. **遍历训练数据**。
3. **前向传播**：计算模型的预测值。
4. **计算损失**：衡量预测值与真实值之间的差异。
5. **反向传播**：计算梯度。
6. **参数更新**：使用优化器更新模型参数。
7. **累加训练指标**：记录损失和准确度。
8. **返回平均训练损失和精度**。

这种结构在深度学习训练过程中非常常见，适用于大多数基于 PyTorch 的模型训练任务。