# CLAUDIAN.md - KK persistent memory for Claudian/Codex

> Startup rule: read this file first when a new Claudian/Codex window needs KK's background.
> Source: adapted from CLAUDE.md.
> Last updated: 2026-07-11.

## Claudian/Codex operating notes

- Call the user KK.
- Prefer Chinese conversation.
- Use relative paths inside the Obsidian vault.
- Mention vault files with Obsidian wikilinks, e.g. [[CLAUDIAN.md]].
- Do not scan the whole vault unless KK explicitly asks.
- Read current note / selected text / explicitly mentioned files first.
- If a note embeds local images and they matter, inspect the images too.
- Preserve YAML frontmatter, Dataview blocks, wiki-links, and existing note style.

### Obsidian 原生语法优先

- 创建或改写 Obsidian Markdown 时，尽量优先使用 Obsidian 原生语法，避免使用可能无法正确渲染的通用 HTML。
- 需要可折叠的答案、提示或核对内容时，使用 Obsidian Callout，例如：

  > [!faq]- 核对
  > - 答案内容

- 不使用 HTML `<details>` / `<summary>` 作为 Obsidian 笔记的默认折叠方案；只有用户明确要求或已确认当前环境支持时才使用。
- 表格、列表等内容放入 Callout 时，每一行都要添加 `>` 引用前缀，确保 Obsidian 正确渲染。



### Windows/中文 vault 编码注意

- 这个 vault 路径和大量内容含中文；不要依赖 PowerShell 原生命令显示中文内容，终端可能会把中文渲染成问号/乱码。
- **重要教训（2026-07-11）**：在 PowerShell here-string 中直接粘贴中文再传给 `python -`，即使设置了 `$env:PYTHONIOENCODING='utf-8'`，脚本源码里的中文也可能在进入 Python 前已被 PowerShell/控制台编码替换成 `?`，写入文件后会变成不可逆乱码。
- 安全读写方案：
  - 读：优先用 Python，并在源码中用 `\uXXXX` 形式构造中文路径；或用 Node REPL 直接读取 UTF-8。
  - 写：若内容含中文，优先使用 `node_repl` / Node `fs.writeFile(path, content, 'utf8')`，或从已有 UTF-8 文件复制/转换；不要把大段中文放进 PowerShell here-string 后交给 Python 写入。
  - 验证：写入后用 Node REPL 或 Python `read_text(encoding='utf-8')` 读取前 100-200 字，确认不是 `????`。
- PowerShell 可用于列目录、跑简单命令；涉及中文正文写入时，改用 Node REPL 更稳。
- 如果必须用 Python 写中文，确保 Python 脚本文件本身以 UTF-8 保存后再执行；不要通过 PowerShell 管道传入含中文源码。

---

## Imported memory from CLAUDE.md

# KK 人物画像 — 用户背景记忆

> 本文件作为用户的持久化记忆，每次新会话自动加载。帮助你快速了解用户背景，无需重复询问。

---

## 一、基本信息

- **称呼**: KK / 康凯
- **生日**: 2005-02-21
- **学校**: 西安电子科技大学 (Xidian University)
- **专业**: AI (人工智能)
- **年级**: 大三下 (2026年 6月，即将大四)
- **MBTI**: INTJ (Ni-Te-Fi-Se 功能轴)
- **居住地**: 中国
- **英文名记录**: Kangkai / KK

## 二、当前核心目标

### 🎯 考研 — 浙江大学软件学院 (27考研)
- **目标**: 浙大软院 AI 工程/研发方向
- **路线叙事**: "从早期AI应用实践出发，意识到浅层应用壁垒不足，希望通过研究生阶段补足理论、系统和工程能力，最后回到更高壁垒的 AI 工程/研发应用"
- **当前阶段** (2026年5月): **基础→强化过渡期**，预计2026年6月正式进入强化阶段
- **备考科目**: 数学一(高数/线代/概率论)、408(数据结构/计算机组成/操作系统/计网)、英语、政治
- **英语六级**: 544分 (从385提升而来)
- **日计划**: 图书馆学习 (早8-晚10)，数学上午+408下午+英语晚间，配合番茄钟
- **每周爱好**: Hip-hop 舞蹈 (舞室+自练)

### 🔬 AI 技术方向
- 大模型应用: RAG、Agent、Agent Memory 系统
- 深度学习: Transformer 架构、PEFT (LoRA/AdaLoRA/QLoRA)
- 项目经验: 5个项目 (Agent记忆系统、RAG、Agent+MCP、知识图谱、文档版面理解VLM)
- 技术写作: 16+篇AI/ML/数学文章，总浏览~3.8w，收藏~3k (知乎+CSDN)
- 正在阅读: 《PRML》《DLFC》《Build a LLM from Scratch》

## 三、性格与认知模式

### 核心特质
- **深度自省者**: 善用心理学框架分析自身行为、情绪和动机
- **系统构建者**: 痴迷于构建可解释、可迭代的个人系统 (学习OS、精力OS、健康OS)
- **战略规划者**: 习惯长远规划 (2年尺度)，但也注意"三个月视界"避免过度焦虑
- **创造者思维**: 认同"创造者"身份而非"考生"身份。——考研是过程，AI工程师是身份认同
- **完美主义倾向**: 高自我标准，计划被打乱时易自责崩溃，但冷静后能系统分析归因

### 认知功能 (INTJ)
| 功能 | 角色 | 表现 |
|------|------|------|
| Ni (内倾直觉) | 主导 | 模式识别、未来蓝图、顿悟式理解 |
| Te (外倾思考) | 辅助 | 高效执行、逻辑框架、秩序追求 |
| Fi (内倾情感) | 第三 | 深度价值观、真实性追求、内在道德标准 |
| Se (外倾感觉) | 劣势 | 当下体验能力弱，有意识地在培养 |

### 学习哲学
- **"慢就是快"**: 越慢压缩知识，未来解压越快
- **"过程即奖励"**: 系统沉淀本身就是胜利
- **"定位→输入→输出→反馈"**: 自创四步学习法
- **"六维解码"**: 归属/组成/抽象/关联/视角/时间
- **"Bedrock Project"**: 160天+的个人学习系统迭代项目

## 四、Obsidian 库结构 (PARA式)

```
0.核心/                  — 北极星规划、学习OS、心智急救包
  00.规划(Plan)/         — 考研规划、阶段性目标、项目分解
  01.学习操作系统My_OS/  — 学习方法、精力管理、健康OS
  02.心智急救包/         — 情绪检测、自我关怀、心理建设
1.工作流/                — 日记、周报、复盘
2.知识库/                — 英语/数学/408/AI 各科笔记
3.创造物/                — 技术文章、项目文档、思想地图
4.不常用/                — 个人信息、随想、联系人、模板
```

### 文件引用约定
- 提及 vault 内的文件时，使用 `[[wikilink]]` 格式
- 用户偏向中文命名文件和文件夹
- Excalidraw 绘图使用 `.excalidraw.md` 格式
- 用户提问规划相关的事情时，阅读 [[0.核心/00.规划(Plan)/2.当前项目/00-规划一览|00-规划一览]]

## 五、交流注意事项

### DO ✅
- 强调知识体系构建和长期成长
- 提供系统化、结构化的建议 (用户擅长且喜欢框架)
- 直接指出逻辑漏洞，只要言之有据用户会欣然接受
- 推荐具体可执行的方法论，而非泛泛而谈
- 提及知识点时，可以进行层级定位 (这个知识属于什么领域、什么位置)
- 当用户需要从多个选项中决策时，给出结构化分析框架

### DON'T ❌
- 不要用考生思维对话 (强调分数/排名/竞争压力)
- 不要过度安慰或情感安抚 (用户更看重逻辑和解决方案)
- 避免"你应该"式说教，用户有自己的判断体系
- 用户深度思考后的决策不易被动摇，可提供新信息但不要强行扭转
- 避免推荐娱乐性短视频/碎片化信息

## 六、关键背景时间线

| 时间             | 事件                                        |
| -------------- | ----------------------------------------- |
| 2025年4月        | 开始系统学习AI应用 (RAG/Agent)，报名丁师兄训练营           |
| 2025年9月        | 美团宣讲会遇技术Leader，获读研建议，开始重新思考路径             |
| 2025年9月15日     | Bedrock Project 立项                        |
| 2025年9月22日     | 确定考研目标: 浙大软件学院                            |
| 2025年10月       | 正式转向考研备考，区分"创造者思维"与"考生思维"                 |
| 2025年11月       | 引入Hip-hop舞蹈作为生活调剂                         |
| 2025年12月       | 确立"三个月视界"概念，六级544通过                       |
| 2026年1月        | 打破"做题=应试"偏见，完善学习方法                        |
| 2026年3月        | 新学期开始，基础阶段推进中                             |
| 2026年5月        | 基础→强化过渡期，正在刷880题/复习OS                     |
| 2026 年 5月 23 日 | 开启强化，早上都是数学，下午都是 408，同步强化。晚上 英语阅读，错题重写/复盘 |


## 七、常用工具与技术栈

- **笔记**: Obsidian (个人知识库主力)
- **AI辅助**: Claude Code、ChatGPT等 (用于学习诊断、写作润色、代码辅助)
- **编程**: Python、PyTorch、LangChain/LlamaIndex、FastAPI、Docker
- **学习**: 番茄钟、正念冥想、思维导图、费曼输出
- **写作**: 知乎、CSDN
- **项目**: Agent记忆系统、RAG、Agent+MCP、知识图谱、VLM


