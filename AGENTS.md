# AGENTS.md — KK vault startup note

- This vault belongs to KK.
- At the start of a new Codex/Claudian session, if user context is needed, read `CLAUDIAN.md` first.
- If more historical background is needed, read `CLAUDE.md` second.
- Do not scan the whole vault unless the user explicitly asks.
- Use relative paths for vault operations and wikilinks when mentioning vault files in responses.
- On Windows with Chinese vault paths/content, prefer Python UTF-8 reads/writes with `PYTHONIOENCODING=utf-8`; avoid relying on raw PowerShell `Get-Content` output when it appears mojibake.

## 当前阶段与写作要求（2026-11-07）

- KK正在考研最后冲刺。先读 [[CLAUDIAN.md]] 顶部的最新状态；涉及排期、任务取舍时，再读 [[0.核心/00.规划(Plan)/2.当前项目/当前冲刺规划.md|当前冲刺规划]]。旧画像与旧阶段只作历史参考，不把计划日期当作已完成进度。
- **所有新建或改写的笔记，默认先让KK看懂。** 用直接、自然的中文；有结构，但不堆术语和空框架。除非用户明确要求论文等正式文体，不默认写成学术摘要。
- 数学、408等讲解按“题目给了什么 → 第一行写什么 → 为什么这样做 → 接下来怎么算／怎么推 → 检查什么”展开。保留关键衔接，不能只写“条件化、降维、建模”等方法标签。必要术语要用本题解释。
- 可以且应当用考生在考场上能落笔的解题视角；不要把旧画像里的“创造者思维”误解成排斥应试训练，也不要用分数排名制造焦虑。
- **不臃肿，但不能为压缩而跳步。** 少重复、少长铺垫；篇幅先留给KK实际卡住的那一步。即使采用精简卡片模板，也以读懂、能独立动手为准。
- 冲刺阶段复用现有材料和入口，不默认增加题库、统计表或学习系统的维护工作。用户本轮明确要求的整理按需执行，不扩大范围。
