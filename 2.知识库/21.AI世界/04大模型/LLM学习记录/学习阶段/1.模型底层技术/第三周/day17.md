# 微调预训练模型
以同义句判断任务为例（每次输入两个句子，判断它们是否为同义句），带大家构建我们的第一个 Transformers 模型

### 加载数据集
1. dataset 将所有数据导入到环境里
        `tokenizer = AutoTokenizer.from_pretrained(模型名字)
        `encoding = tokenizer(sentence,truncation = ...) `
        `tokens = encoding.tokens`
        

        
2. DateLoader 按批次加载数据，以备预训练
      DataLoader 共填 train_data, batch_size, shuffle, collate_ fn 四个参数
      `train_data`：必须是实现了 `__getitem__` 和 `__len__` 的数据集 
     **`collate_fn`**: 自己手动实现的对数据的编码。一定要返回 pytorch 向量
### 训练模型
1. 构建模型
     - 使用 bert 作为模型
     - 继承预训练模型来创建自己的模型

     定义模型时，要有 encoder（通过 automodel 实现）
     
    
    
    调用模型- **`nn.Module` 的魔法方法** PyTorch 的 `nn.Module` 类定义了 `__call__` 方法（在父类 `torch.nn.Module` 中实现），它会自动调用你的 `forward` 方法。
 ```python
    class Module:     def __call__(self, *args, **kwargs):        
       return self.forward(*args, **kwargs)  
       
   outputs = model(batch_X) # 实际调用model.__call__() → 转发到forward()   
       ```
     
2. 训练循环
        optimizer. zero_grad ()---loss. backward ()----optimizer. step ()---Ir_scheduler. step ()
3. 测试循环
     model. eval\torch. no_grad () 
### 保存和加载模型
根据验证集上的表现来调整超参数以及选出最好的模型，最后再将选出的模型应用于测试集以评估性能