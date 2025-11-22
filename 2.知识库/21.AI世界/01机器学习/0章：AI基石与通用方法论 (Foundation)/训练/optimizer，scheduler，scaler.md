```python
class GradScaler:
    def __init__(self):
        # self._scale 是一个【FP32】的张量，比如 tensor(65536.0, dtype=torch.float32)
        self._scale = torch.tensor(65536.0, device="cuda", dtype=torch.float32)

    def scale(self, loss_fp16: torch.Tensor) -> torch.Tensor:
        # 1. 把输入的 FP16 loss，先转换成 FP32
        loss_fp32 = loss_fp16.float() # .float() 是 .to(torch.float32) 的简写
        
        # 2. 在 FP32 精度下，进行乘法运算
        scaled_loss_fp32 = loss_fp32 * self._scale
        
        # 3. 返回这个 FP32 的结果
        return scaled_loss_fp32

```
我再次总结一下。  
首先loss是在autocast环境下计算的，精度是fp16，为了计算的效率！但是也有部分有精度需求的，会被autograd识别，仍然保存fp32.  
计算完loss我们开始反向传播了。 我们刚才是fp16的loss，特别小， 那么计算梯度时，此时梯度仍然是fp16.就可能也是特别特别小， 这会造成，存入.grad时，直接变为0. 我们得先scale一下 放大loss。 放大后再进行backward() 这叫做反向传播，这个动作是计算梯度，并且打上.grad的标签。 所以这个动作，是为了弥补fp16精度不够的缺点  
接下来呢， 我们每个属性的grad有了，就可以参数更新了。  
我们使用的是optimizer，这下我们捕获.grad了，但我们必须把刚才的scale除过去。 除过去没问题的，不会变成0的呀。  
所以本来，很小的数放不了fp16，经过我们放大再缩小，反而能放到fp16了。  
接着我们正式更新权重，刚才还埋了雷，就是刚才scale如果把梯度scale成inf了，那么unscale就无效了，也就是我们无法还原本来的梯度了。 那我们直接scaler.step（optimiezer）而不是optimizer.step() 会检查有没有这情况，有的话就跳过更新。  
这里的更新，还有个操作，就是把fp16恢复成fp32. 但我的理解是， 值大小肯定就没变呀，毕竟是小精度恢复成高精度。

整体流程，我的理解对不对