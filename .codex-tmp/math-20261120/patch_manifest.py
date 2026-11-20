from pathlib import Path
import json,re,collections,hashlib
root=Path('.codex-tmp/math-20261120')
p=root/'use-plan.md';t=p.read_text(encoding='utf-8-sig').replace('本页114张卡','本页全部卡片');p.write_text(t,encoding='utf-8')
p=root/'write_outputs_part.py';t=p.read_text(encoding='utf-8-sig')
t=t.replace("ledger={'version':2", "ledger={'version':2")
# Map image provenance to the immutable pre-edit backup where necessary, and retain original location separately.
t=t.replace("(ROOT/'manifest.json').write_text", "for image in ledger['images']:\n image['original_source']=image['source']\n image['source']=CHANGED.get(image['source'],image['source'])\n(ROOT/'manifest.json').write_text")
p.write_text(t,encoding='utf-8')
# Document why the generic auditor needs the scope-aware pass for this mixed-subject consolidation.
(root/'audit-notes.md').write_text('''# 本轮校验口径

- 通用audit_math_summary.py已运行，但不支持本轮明确采用的reference-only/out-of-scope处置、跨源同题图合并，且把本页指向H3卡片的本地链接只按H2目录链接校验，因此其结果不能直接作为本轮通过/失败依据。
- 没有修改技能或审计器来跳过错误。原报告保留在skill-audit-report.json。
- validate.py额外按明确的混合源边界校验：27份源文件SHA-256（两份改写目标用整理前备份核验），214处图像的路径和哈希、每处处置理由、关联卡片、115张卡的3—4步结构、115个盲练入口、36个首轮入口、全部实际文件和各级标题链接、编码及表格中的竖线。
- validation-report.json为本轮范围感知的实际结果。图像转录齐备不等于数学正确性证明；关键公式与结论另经主模型复核和math-checks.json中的独立计算核对。
- 01反函数原例题条件冲突，未替原始题目擅自猜改；G101明确存疑。
''',encoding='utf-8')
print('patched provenance and plan')
