# 第一遍，全局直觉
## Abstract&Instruction&配图

Qwen-VL 是多模态模型， 
特点是文档解析强，能提取到结构化数据。  理解长视频。  理解图片的颗粒度上比较强。   有空间感。

主要架构是一个vision encoder，和一个qwen2.5的大语言模型decoder
vision encoder是改进过后的VIT

主要技术是window attention MRope
# 第二遍 深入骨架
**你要探索的核心问题是：Qwen-VL是如何实现这些强大能力的？**

## Model Architecture
#### 1. 关于“改进过后的ViT”：它是如何看清世界的？

A key issue arises from the quadratic computational complexity associated with processing images of varying sizes.

这里关键技术就是window attention，将全局的自注意力计算（所有patch互相计算）限制在一个个“窗口”（window）内部，比如在112x112的区域内。这样，计算量就从与整张图的patch总数平方相关，变成了只与窗口内的patch数平方相关，，，作用是降本增效
还有就是**2D RoPE**：-注**入精确的二维空间位置信息。** 原始的ViT用的是1D的可学习位置编码，它只是告诉模型“这是第1个patch”、“这是第2个patch”，但丢失了“这个patch在图片的左上角”这样的二维空间信息。2D RoPE通过旋转编码的方式，能更好地让模型理解每个patch在二维平面上的绝对和相对位置。

- **总结**：两者协同工作。Window Attention让模型能“看得起”高分辨率大图，而2D RoPE则让模型能“看懂”这张大图里每个部分的位置关系。你的总结是正确的，但理解了这个分工后会更清晰

#### 2. 关于“连接”：视觉和语言是如何对话的？

ViT输出的一堆patch特征 -> 每4个相邻的打包一组 -> 组内特征拼接 -> 通过MLP进行压缩和转换 -> 得到维度与文本token一致的、数量更少的视觉token -> 喂给LLM

**这么做的好处是什么？**  
原文也说了：**"reduces computational costs"** 和 **"dynamically compress image feature sequences"**。  
通过“4合1”的操作，视觉token的数量直接减少为原来的1/4。比如原来一张图有1024个patch token，现在只有256个了。喂给LLM的序列长度大大缩短，而LLM的计算量也和序列长度的平方成正比，所以**计算成本大幅下降**。这是一种非常高效的“特征压缩”技巧。


#### 3. **MRope**：这个技术是做什么用的？报告里有没有解释它相比于我们熟知的RoPE（旋转位置编码）有什么优势

- **MRoPE (Multi-modal RoPE)** 的精妙之处在于，它为LLM提供了一套**统一的、能理解多模态输入位置信息**的框架。
    
    - **你的理解“能方便地切换模式”非常形象和准确！** 它就是用一套编码系统来处理不同来源的token。
        
    - **对文本token**：它的时间、高度、宽度ID都一样，退化成了普通的1D RoPE，和处理纯文本的LLM行为一致。
        
    - **对图像token**：它的时间ID不变（因为是静止的），但每个token都有自己独特的高度和宽度ID。这样LLM在处理这些视觉token时，就能“脑补”出它们在原始图片中的空间布局。
        
    - **对视频token**：它的时间ID会随着帧数增加而变化，同时在每一帧内部，高度和宽度ID也各不相同。这让LLM不仅知道一个patch在某一帧的位置，还知道它属于第几帧。
        
- **总结**：MRoPE是一个非常聪明的设计。它让LLM这个原本只能理解一维序列（文本）的模型，现在能“看见”一个带有时间、高度、宽度三个维度的“多维世界”。你关于“对他们都能做到位置信息的注入”的理解是完全正确的。



## Train

### pretrain data
The dataset encompasses a wide variety of multimodal data, such as image captions, interleaved image-text data, optical character recognition (OCR) data, visual knowledge (e.g., celebrity, landmark, flora, and fauna identification), multi-modal academic questions, localization data, document parsing data, video descriptions, video localization, and agent-based interaction data
是在说，有特别多种图片和视频的类型是用cleaning raw web data, synthesizing data, etc.建立的

Our process involves two steps: standard data cleaning (Li et al., 2024e) followed by a four-stage scoring system using an internal evaluation model. The scoring criteria include: (1) text-only quality, (2) image-text relevance, (3) image-text complementarity, and (4) information density balance
对于图文对中，文字的数据，这个需要好好筛选，所以他们特地做了工作


Grounding Data with Absolute Position Coordinates We adopt native resolution training with the aim of achieving a more accurate perception of the world. In contrast, relative coordinates fail to effectively represent the original size and position of objects within images. To address this limitation, Qwen2.5-VL uses coordinate values based on the actual dimensions of the input images during training to represent bounding boxes and points
团队直接在图片里就标注好了位置信息、物体大小等，利用坐标值、边界框。 g bounding boxes and points with referring expressions, leveraging both publicly available datasets and proprietary data 获取数据的方法，仍然是收集公开的和合成的

Specifically, we incorporated a diverse array of elements into the documents, such as tables, charts, equations, natural or synthetic images, music sheets, and chemical formulas. These elements were uniformly formatted in HTML, which integrates layout box information and descriptions of illustrations into HTML tag structures. We also enriched the document layouts according to typical reading sequences and included the coordinates corresponding to each module, such as paragraphs and charts, in the HTML-based ground truth
为了提升理解文档的能力，还收集了文档数据集，做成html以方便注入位置信息


To support a wider range of languages and enhance multilingual capabilities, we have incorporated a large-scale multilingual OCR dataset       文档数据集
For chart-type data, we synthesized 1 million samples using visualization libraries including matplotlib, seaborn, and plotly, encompassing chart categories such as bar charts, relational diagrams, and heatmaps.  图表数据集
Regarding tabular data, we processed 6 million real-world samples through an offline end-to-end table recognition model, subsequently filtering out low-confidence tables, overlapping tables, and tables with insufficient cell density表格数据集

最后，还以fps采样（啥意思） 收集了视频数据，
- **FPS**: Frames Per Second，即“每秒帧数”。视频本质上就是连续播放的图片（帧）。一个30 FPS的视频，每秒包含30张图片。
    
- **采样 (Sampling)**: 如果把视频的每一帧都喂给模型，计算量巨大，而且相邻帧之间的信息高度冗余（比如一个固定镜头，连续1秒的画面可能都差不多）。
    
- **FPS采样**: 指的是**有选择性地提取帧**。比如，一个30 FPS的视频，如果按“1 FPS”来采样，就意味着每秒只从30帧里抽出1帧来给模型看。这是一种在保留视频核心内容的同时，大幅降低数据量和计算成本的必要手段。



For perception, we collect screenshots on mobile, web, and desktop platforms. A synthetic data engine is used to generate screenshot captions and UI element grounding annotations. The caption task helps Qwen2.5-VL understand the graphic interface, while the grounding task helps it align the appearance and function of elements. For decision-making, we first unify the operations across mobile, web, and desktop platforms into a function call format with a shared action spac
还训练了agent能力？ 这个我从未耳闻，agent能力也是能训练的？ 我只能看懂把前端布局让llm训练得能看懂， 如何训练得能decision我是不理解的
1. **Decision-making (决策)**:
    
    - **这是你困惑的核心**：“如何训练得能decision”。
        
    - **关键思想**: **将“决策”和“行动”转化为一个“语言生成”问题。**
        
    - **具体做法**:  
        a. **统一行动空间**: 他们首先定义了一套所有平台（手机、网页、PC）通用的“行动语言”。比如，点击屏幕坐标(250, 500)这个动作，被统一表示成一个**函数调用格式的字符串**，例如 click(x=250, y=500)。输入文字的动作，可以表示为 type(text="你好世界")。  
        b. **构造“行动轨迹”数据**: 训练数据不再是简单的图文对，而是一条完整的“轨迹 (trajectory)”，看起来像这样：  
        
```
[初始状态]: (电脑桌面截图)  
[用户指令]: "打开浏览器访问Google"  
*[模型思考(可选)]**: thought: "要访问Google，我需要先找到并点击Chrome浏览器图标。" (这也是生成的文本)  
*[模型行动1]**: click(icon="chrome.png")  
[新状态]**: (打开了Chrome浏览器的截图)  
[模型思考(可选)]**: thought: "现在我需要点击地址栏并输入google.com。"  
[模型行动2]**: type(element="address_bar", text="google.com")  
 ...以此类推...  
 
        c. **训练目标**: 模型的任务变成了**标准的“下一个词预测”**。给定[状态]和[指令]，模型需要像写文章一样，一个词一个词地生成[思考]和[行动]的字符串。
```
#### pretrain- Training Recipe
分三个阶段 循序渐进、从易到难
1. 仅训练vit  ocr数据 visual knowledge
2. 复杂且推理密集型的数据集，例如交错数据、多任务学习数据集、视觉问答（VQA）、多模态数学、基于代理的任务、视频理解以及纯文本数据集。这些数据集增强了模型在视觉和语言模态之间建立更深层联系的能力
3. 增强模型在较长序列、视频和基于代理数据上的推理能力，同时增加序列长度

### Postraining

在指令数据集构造方面
- 纯文本数据（50%）和多模态数据（50%）均等分布，其中多模态数据包括图像-文本和视频-文本组合。多模态数据的加入使模型能够有效处理复杂输入
- 包括单轮和多轮交互。这些交互通过从单图像输入到多图像序列的多种场景进一步进行上下文化，从而模拟真实的对话动态。查询来源主要来自开源仓库，同时还包括精选购买数据集和在线查询数据的贡献。
- This structured and diverse composition ensures that the SFT phase effectively aligns pre-trained representations with the nuanced demands of downstream multimodal tasks, fostering robust and contextually aware model performance.

在数据集过滤方面
- Domain-Specific Categorization：从之前预训练的模型中，衍生一个模型，专门对数据集进行分类，organizes QA pairs into eight primary domainsdivided into 30 fine-grained subcategories.，意思是分类的精度非常足够，
- Domain-Tailored Filtering：各自领域有各自规则，去过滤
- Rule-Based Filtering：移除重复模式，以防止扭曲模型的训练过程并确保最佳性能。此外，包含不完整、截断或不正确格式化响应的条目，。与问题无关或可能产生有害输出的查询和答案也会被丢弃
- Model-Based Filtering： 这个没见过，意思是用奖励模型，在多个维度上评估多模态问答对。查询根据复杂性和相关性进行评估，仅保留那些具有适当挑战性和上下文相关性的示例。答案根据正确性、完整性、清晰度、与查询的相关性以及帮助性进行评估。
- Rejection Sampling for Enhanced Reasoning： 
	这是一个非常强大、用来**生成高质量“思维链 (Chain-of-Thought, CoT)”** 数据的技术。我们一步步来拆解：
	
	1. **背景**: 对于复杂的推理问题（比如数学题、逻辑题），我们希望模型不仅给出答案，还能给出详细的解题步骤（即“思维链”）。但让模型一步到位生成完美的解题步骤是很难的。
	    
	2. **“采样 (Sampling)” 是什么？**: 对于同一个问题，让模型生成**多个**不同的答案/解题路径。比如，对于“1+1=?”这个问题，模型可能生成：
	    
	    - 答案A: "等于2。因为..."
	        
	    - 答案B: "等于3。因为..."
	        
	    - 答案C: "等于2。详细步骤是..."
	        
	3. **“拒绝 (Rejection)” 是什么？**: 找一个“裁判”来判断这些生成的答案哪个是最好的。这个“裁判”可以是：
	    
	    - **一个强大的外部工具**: 比如对于数学题，可以用一个代码解释器去运行代码，验证结果是否正确。
	        
	    - **一个更高阶的模型**: 用一个能力更强的模型（比如GPT-4）或者一个专门训练的“验证模型 (Verifier)”来给这些答案打分。
	        
	    - **简单规则**: 比如，只保留那些最终答案正确的解题步骤。
	        
	4. **过程**:
	    
	    - **第一步 (Generate)**: 针对一个复杂问题，让模型**生成 N 个**（比如16个）不同的思维链和答案。
	        
	    - **第二步 (Verify & Reject)**: 用“裁判”去检查这N个答案，**拒绝掉所有错误的、不好的答案**。
	        
	    - **第三步 (Select)**: 从所有通过验证的、正确的答案中，**选择最好的一个**（比如步骤最清晰、逻辑最严谨的那个）。
	        
	    - **最终结果**: 得到一个 (问题, 高质量的思维链答案) 的数据对。
	        
	
	**一句话总结**: **Rejection Sampling 就是“广撒网，精挑鱼”。通过让模型自己“刷题”并用裁判来“批改”，自动地、大规模地制造出高质量的、带有完美解题过程的SFT数据。** 
### Recipe
- 在 SFT 阶段，模型在多样化的多模态数据上进行微调，包括图像-文本对、视频和纯文本，数据来源包括通用视觉问答（VQA）、拒绝采样以及专业数据集，如文档和 OCR、定位、视频和与代理相关的任务。
- DPO 阶段专注于图像-文本和纯文本数据，利用偏好数据使模型与人类偏好保持一致，每个样本仅处理一次以确保高效优化
