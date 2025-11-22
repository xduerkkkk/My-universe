本次llm开发借鉴minimind项目
https://github.com/jingyaogong/minimind
是该开源项目的学习项目，旨在分析全流程，让未接触过llm的同学也能创造并使用自己的llm
# 所有流程
要开发整个llm，先要设计好模型架构，以及tokenizer 
准备好这俩个，就相当于准备好了模型骨架，以及模型能跟人类交流的工具了
下面我们要丰满骨肉 以及使用  经历4个阶段  
称为pipeline
预训练--后训练--评估测试---部署

下面一一介绍本次项目 的
模型架构，tokenizer的设计，以及4个阶段

# 模型架构
最基础的模型架构：
- pytorch基本原理
- 拼接神经网络的示例
- 传统transformer
如何添加/修改：
- 各个厂商怎么做
- 本次minimind怎么做
# tokenizer
- 分词：长段句子需要拆分  组建词库
- 编码：每个词一个数字 特殊符号，比如`<|im_end|>` 
以上流程，构建出`input_ids` 也就是自然语言翻译后，输入给模型的东西
这些流程由tokenizer完成，  而labels、attention_mask呢？是人工构建的吗？

# 后训练流程


1. 让模型学会6说人话，学会回答人的问题：SFT
2.  说质量更高的人话
    - dpo:通过对比偏好对（chosen和rejected回答）的似然比来优化模型，使得模型更倾向于生成高奖励的回答。
    - distillation：让教师模型给出高质量回答，学生模型（本模型）去学老师
3. 让模型学会推理：本质仍是sft，只不过要针对”推理“这一步骤给模型设置奖励与惩罚
4. 让模型学会专业领域： peft参数高效微调，最常见的就是lora
# 所需数据集
## 预训练
- 直接拿网上的数据集：
{"text": "这里是第一段文本内容...", "other_key": "其他信息..."}
- 自己收集
最终构造出{'text':...}格式的jsonl
 字典的key叫text只是习惯
 
## SFT
收集的数据类似下面格式
```
[ {"role": "user", "content": "What is the most recent version of the Android operating system?"}, {"role": "assistant", "content": "As of my last update..."} ]

```

针对不同的tokenizer  进行格式转化
qwen类的就转化为：
```
<|im_start|>user
What is the most recent version of the Android operating system?<|im_end|>
<|im_start|>assistant
As of my last update...<|im_end|>
```

## DPO、Distillation、Reasoning
DPO、Distillation、Reasoning数据与SFT数据格式大体一致
DPO需要给出两种回答，好的和不好的
Distillation数据 中assistant是空的，需要由教师模型生成
Reasoning数据中，assistant回答多了推理步骤和标签

# 数据预处理
# 训练流程
