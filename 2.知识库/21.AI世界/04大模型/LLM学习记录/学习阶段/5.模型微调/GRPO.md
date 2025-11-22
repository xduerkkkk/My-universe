GRPO全称
#### **Group Relative Policy Optimization**
以往的强化学习，要专门训练价值模型
而GRPO
- **组采样**​：对同一问题生成多个输出（如16个不同答案）
- ✅ ​**组内奖励归一化**​：计算每个输出的奖励（如答案正确性），再减去组平均奖励并除以标准差，得到相对优势值
- ✅ ​**策略优化**​：提升高优势值输出的生成概率，抑制低优势值输出

# 引入测试集

整个训练都是一个模型。
先引入GSM8K数据集
格式是这样的
```python
{'question': 'Trevor buys several bouquets of carnations. The first included 9 carnations; the second included 14 carnations; the third included 13 carnations. What is the average number of carnations in the bouquets?', 
'answer': 'The sum is 9+14+13=<<9+14+13=36>>36.\nThere are 3 bouquets.\nThe average is 36/3=<<36/3=12>>12.\n#### 12'}

```
我们将数据处理成

```python
{

            "prompt": [

                {"role": "system", "content": SYSTEM_PROMPT},

                {"role": "user", "content": example["question"]}

            ],

            "answer": extract_answer_from_dataset(example["answer"])

        }

```
这个数据集有啥用呢？用来评估模型
具体评估方式在下面。
那对于评估函数，我们把prompt和答案提取出来，将prompt喂给模型，将输出与原答案对比以评估

```python
# Build the full prompt using the same method as training.

        full_prompt = build_prompt(example["prompt"])

        expected = example["answer"]

        # Tokenize the full prompt and generate a response from the model.

        inputs = tokenizer.encode(full_prompt, return_tensors="pt").to(device)

        outputs = model.generate(

            inputs,

            max_length=512,

            temperature=0.7,

            num_return_sequences=1

        )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

```

那我们可以直接拿测试集测试当前基座模型（未经过sft、rl）的数学推理能力了。
评估后的数值记`pre_sft_accuracy` 
# SFT
好，接着正式训练模型

接着是sftdataset，是GSM8K问题+CoT数据集监督微调。
我们将数据处理为
```python
{
    "messages": [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
        {"role": "assistant", "content": "<reasoning>...</answer>"}
    ]
}
```
这个喂给模型，让模型学习思维链的生成。
此阶段，chatdatacollator可以自己定义。`input_ids` 是由什么样的文本转换的呢？ `prompt+target` 

```python
prompt = build_prompt(example["messages"][:-1])

            target = example["messages"][-1]["content"]
full_text = prompt + "\n" + target

            tokenized = self.tokenizer(full_text, truncation=True, max_length=self.max_length)

            input_ids = torch.tensor(tokenized["input_ids"])
```
`labels` 设置的和input一模一样

使用`Trainer` 函数，完成训练。
注意看函数的参数，待会与RL的`Trainer` 函数对比

```python
 sft_trainer = Trainer(

        model=model,

        args=sft_training_args,

        train_dataset=sft_dataset,

        data_collator=ChatDataCollator(tokenizer)

    )

```

完成训练后可以评估一次
记`post_sft_accuracy`
# RL
基于刚才SFT的模型，进行训练
那我们强化学习使用的数据集是什么呢？
是**训练集分割后的子集**​（排除最开始评估用的30条）
```python
{

            "prompt": [

                {"role": "system", "content": SYSTEM_PROMPT},

                {"role": "user", "content": example["question"]}

            ],

            "answer": extract_answer_from_dataset(example["answer"])

        }

```
在这个数据集的基础上，我们再使用两个奖励函数，进行强化学习

```python
trainer = GRPOTrainer(

        model=model,

        processing_class=tokenizer,

        reward_funcs=[format_reward, correctness_reward],

        args=training_args,

        train_dataset=train_data,

    )
```
最后模型训练完，可以继续评估一次
记
```python
post_grpo_accuracy
```

# 各个部件 
`extract_answer_from_model_output` 模型输出的有reasoning有answer 这个函数用来提取answer
 ​**`extract_answer_from_dataset`**：解析原始数据标签**​
```python
def extract_answer_from_dataset(text):
    if "####" not in text:
        return None  # 格式错误处理
    return text.split("####")[1].strip()  # 取分隔符后内容
```

- ​**数据规范**​：  
    假设数据集使用 `"####"` 分隔问题与答案（如GSM8K、MATH等数学推理数据集）

# 数据流程
dataset格式文件，**测试集***用load_dataset解析后*，每一个索引都是字典
此时数据形式为`question:...answer:...####最终答案` 
我们非序列化修改数据为 `"prompt:[

                {"role": "system", "content": SYSTEM_PROMPT},

                {"role": "user", "content": example["question"]}

            ]
            answer: ####最终答案`
 那我的问题就是，必须要这么修改数据格式吗？还是说没必要？
 - ✅ ​**必须转换**​：对话微调（ChatML格式）要求结构化角色信息
<font color="#f79646"> answe为什么取最终答案而不要原先answer数据的推导过程?</font>
这不是训练集，而是测试集，测试集就是不用过程，验证答案​


- ​**数学问题特性**​：推导过程是推理路径，训练目标是**结果正确性**​
- ​**强化学习需求**​（参考图像Part 5 奖励函数）：
    - 奖励函数通常只验证最终答案匹配度（如：`1.0` if 答案正确 else `0.0`)
    - 减少噪声：推导文本会干扰奖励信号


 然后
我们要给模型训练的，是序列化的input_ids labels  不需要attensionmask？还是在别处体现？？
这里又是怎么处理》？

## 评估函数
提取一个数字 匹配成 不匹配提取最后一个数字 匹配成 还不匹配就算失败
## 正确性奖励函数
### **答案正确性奖励函数**
- ​**精确匹配（2.0分）​**​：鼓励模型输出与标准答案完全一致。
- ​**数值等价（1.5分）​**​：兼容数字格式差异（如 `7` vs `7.0`），提升鲁棒性
### **XML 格式遵循奖励函数**
每检测到一个标签得 `0.2` 分，最高 `0.8` 分