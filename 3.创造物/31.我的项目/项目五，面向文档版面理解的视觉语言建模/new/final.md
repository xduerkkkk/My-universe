# FUNSD 项目下一阶段：可视化 + Demo 集成 + 报告撰写

你已经完成了整个实验主线里最难的一部分：

- 数据读取与预处理
    
- OCR-only baseline
    
- Text + Layout baseline
    
- LayoutLMv3
    
- 统一训练与评估
    
- 自动日志与分析
    

而且结果是非常“像论文”的：

|Model|Entity F1|
|---|---|
|OCR-only|0.3352|
|Text+Layout|0.3317|
|LayoutLMv3|0.7479|

这意味着：

1. 你的实验链路是可信的；
    
2. LayoutLMv3 确实学到了页面结构与视觉信息；
    
3. 你的 baseline 对比具有研究意义；
    
4. 已经足够支撑课程项目报告。
    

现在项目已经进入“收尾强化阶段”。

接下来最重要的不是继续训练，而是：

1. 做可视化
    
2. 做 Demo 集成
    
3. 做错误案例展示
    
4. 写最终报告
    
5. 做 PPT
    

---

# 一、先解释你的实验结果（非常重要）

这是后面写报告和答辩时最核心的部分。

## 1. OCR-only vs LayoutLMv3

你的结果：

|Model|Entity F1|
|---|---|
|OCR-only|0.3352|
|LayoutLMv3|0.7479|

说明：

- 仅使用文本 token，无法充分理解表单结构；
    
- 文档理解任务不仅依赖语义，还强依赖版面布局与视觉上下文；
    
- LayoutLMv3 同时利用：
    
    - token 文本
        
    - bbox 坐标
        
    - 页面图像 patch
        
- 因此能够显著提升 QUESTION / ANSWER 对齐能力。
    

这是你报告里的核心结论。

---

## 2. 为什么 Text+Layout 没提升？

你的结果：

|Model|Entity F1|
|---|---|
|OCR-only|0.3352|
|Text+Layout|0.3317|

这个结果其实很正常，而且很值得分析。

你可以在报告中写：

### 可能原因 1：FUNSD 数据量较小

FUNSD 训练集只有约 149 页。

bbox MLP：

- 参数较少
    
- 学习能力有限
    
- 难以充分建模复杂布局关系
    

因此位置信息没有有效转化为性能提升。

---

### 可能原因 2：简单 bbox MLP 表达能力不足

你当前方法：

```text
bbox -> MLP -> concat(text_hidden)
```

这是一种轻量 baseline。

但它无法像 LayoutLMv3 那样：

- 联合建模文本与视觉 patch
    
- 使用 Transformer 融合空间关系
    
- 学习复杂二维布局结构
    

因此位置特征贡献有限。

---

### 可能原因 3：DistilBERT 本身不适合布局学习

DistilBERT 本来是通用 NLP 模型。

它没有：

- 2D position embedding
    
- image-text pretraining
    
- layout-aware attention
    

所以即使加入 bbox，也难以真正理解页面结构。

---

## 3. HEADER 类别为什么难？

你的结果：

|Category|LayoutLMv3 F1|
|---|---|
|QUESTION|0.7587|
|ANSWER|0.7575|
|HEADER|0.6042|

HEADER 是最难类别，这非常合理。

原因包括：

- HEADER 数量少（类别不平衡）
    
- HEADER 文本形式多变
    
- HEADER 边界不固定
    
- 有些 HEADER 更依赖页面视觉区域而不是文本语义
    

这是一个很好的“错误分析点”。

---

## 4. 为什么 entity_to_O 错误最多？

说明模型更倾向于：

```text
保守预测
```

也就是：

```text
宁愿不识别实体，也不愿误识别。
```

这在 token classification 很常见。

原因可能包括：

- O 标签占比远大于实体标签；
    
- 模型受到类别不平衡影响；
    
- entity-level evaluation 对边界非常敏感；
    
- 模型在不确定时倾向输出 O。
    

这部分可以写进错误分析章节。

---

# 二、下一阶段：可视化展示（推荐优先做）

这是你现在最值得做的阶段。

目标：

把模型预测结果画回页面图像。

例如：

- QUESTION -> 蓝框
    
- ANSWER -> 绿框
    
- HEADER -> 橙框
    
- 错误预测 -> 红框
    

这样你会得到：

- 可写进报告的图
    
- 可放进 PPT 的图
    
- 可集成进 Gradio Demo 的图
    
- 可展示错误分析的图
    

---

# 三、建议新增模块

建议新增：

```text
funsd_experiment/
├── src/
│   └── visualization/
│       ├── draw_predictions.py
│       └── compare_visualization.py
│
├── scripts/
│   └── 08_generate_visualizations.py
│
├── outputs/
│   └── visualization/
│       ├── text_only/
│       ├── text_layout/
│       └── layoutlmv3/
│
└── report/
    └── figures/
```

---

# 四、推荐可视化内容

## 1. 单模型预测可视化

展示：

- token bbox
    
- gold label
    
- pred label
    

例如：

```text
QUESTION -> 蓝色
ANSWER -> 绿色
HEADER -> 橙色
```

---

## 2. 错误高亮

例如：

```text
预测错误 -> 红色边框
```

这样报告里会非常直观。

---

## 3. 三模型对比图（非常推荐）

同一页面：

|OCR-only|Text+Layout|LayoutLMv3|
|---|---|---|
|图 1|图 2|图 3|

你会很直观看到：

- OCR-only 漏掉字段；
    
- LayoutLMv3 更完整；
    
- HEADER 更稳定。
    

这会让你的报告质量提升非常明显。

---

# 五、下一阶段之后：接回原 Gradio Demo

你原来的仓库已经有：

- PDF 上传
    
- OCR 可视化
    
- VLM 问答
    
- Hybrid Markdown
    
- QA 证据高亮
    

现在你可以新增：

```text
FUNSD Field Extraction Demo
```

新增一个 Tab：

```text
[OCR-only]
[Text+Layout]
[LayoutLMv3]
```

上传一张表单：

- 显示字段框
    
- 显示预测标签
    
- 显示错误对比
    

这样整个项目会非常完整。

---

# 六、最终报告推荐结构（你已经够写了）

## 1. Introduction

- 文档理解背景
    
- OCR-only 的局限
    
- Layout-aware/VLM 方法意义
    
- 本项目目标
    

---

## 2. Dataset

介绍 FUNSD：

- 表单字段抽取
    
- QUESTION / ANSWER / HEADER
    
- OCR token + bbox
    
- train/test 数量
    

---

## 3. Data Processing

你已经做了：

- OCR token 读取
    
- bbox 清洗
    
- bbox 归一化
    
- 文本框排序
    
- BIO 转换
    
- train/val/test 划分
    
- 数据统计
    

这一章已经够完整。

---

## 4. Methods

### 4.1 OCR-only baseline

输入：

```text
tokens
```

模型：

```text
DistilBERT token classification
```

---

### 4.2 Text+Layout baseline

输入：

```text
tokens + bboxes_norm
```

bbox MLP + text fusion。

---

### 4.3 LayoutLMv3

输入：

```text
tokens + bbox + image
```

重点说明：

- processor
    
- patch embedding
    
- 2D position embedding
    
- multimodal fusion
    

---

## 5. Experiments

包括：

- training config
    
- GPU
    
- epochs
    
- batch size
    
- lr
    
- evaluation metrics
    

---

## 6. Results

直接放：

- model_comparison. md
    
- class_level_comparison. md
    

然后分析：

- LayoutLMv3 优势
    
- bbox baseline 不明显
    
- HEADER 难点
    

---

## 7. Error Analysis

放：

- entity_to_O
    
- boundary error
    
- question-answer confusion
    

再配可视化图。

---

## 8. Demo System

介绍：

- Gradio
    
- OCR visualization
    
- field extraction visualization
    
- QA evidence highlight
    

---

## 9. Conclusion

总结：

- layout + image 对文档理解非常关键；
    
- LayoutLMv3 明显优于纯文本方法；
    
- bbox-only baseline 提升有限；
    
- future work 可以探索更强 layout encoder 或 larger dataset。
    

---

# 七、你现在已经达到什么水平？

你现在已经不是“简单调 API”。

你实际上已经完成了：

- 文档理解 pipeline
    
- token classification
    
- BIO labeling
    
- bbox alignment
    
- multimodal training
    
- baseline comparison
    
- VLM fine-tuning workflow
    
- evaluation & error analysis
    
- experiment management
    

这已经是非常标准的 Document AI 课程项目。

后面重点就是：

```text
可视化 + 报告表达
```

而不是继续堆模型。

---

# 八、推荐的下一步顺序

建议按这个顺序：

## Step 1（推荐现在做）

可视化预测结果

目标：

- 把 bbox 和预测画回图像
    
- 自动生成报告图
    
- 输出错误案例图
    

---

## Step 2

接回 Gradio Demo

新增：

```text
Field Extraction Tab
```

---

## Step 3

开始正式写报告

因为你现在已经有：

- metrics
    
- comparison
    
- error analysis
    
- logs
    
- figures
    

报告其实已经可以开始写。

---

## Step 4

做 PPT

重点展示：

- 三模型对比
    
- 可视化结果
    
- 错误案例
    
- Demo