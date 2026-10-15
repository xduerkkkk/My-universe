from pathlib import Path
import re,json,hashlib,shutil
base=Path('2.知识库/20.North_star_ZJU/201.数学/04真题阶段/02数学做题框架')
tmp=Path('tmp/pdfs/proof-30')
s=(tmp/'vision-transcription.txt').read_text(encoding='utf-8')
s=s[:s.index('[2002')]+(tmp/'vision-page6.txt').read_text(encoding='utf-8').split('[2002',1)[1].join(['[2002',''])
s=re.sub(r'<i>(.*?)</i>',r'\1',s)
s=re.sub(r'^.*(?:dy/公众号|第\s*\d+\s*页).*$', '', s,flags=re.M)
s=re.sub(r'^真题证明做题本\s*$', '', s,flags=re.M)
s=re.sub(r'^.*(?:二星题|三星题).*$', '', s,flags=re.M)
pat=re.compile(r'^\[(\d{4})\s*[–-]\s*([^\]]+)\]\s*(.*)$',re.M)
ms=list(pat.finditer(s)); print('TOTAL',len(ms))
assert len(ms)==32
pages=[1]*5+[2]*5+[3]*5+[4]*6+[5]*5+[6]*6
items=[]
for i,m in enumerate(ms):
 body=s[m.end():ms[i+1].start() if i+1<len(ms) else len(s)].strip()
 body=re.sub(r'\n{3,}','\n\n',body)
 title=f"Q{i+1:02d}｜{m.group(1)} {m.group(2).strip()} {m.group(3).strip()}"
 item={'id':f'Q{i+1:02d}','year':m.group(1),'paper':m.group(2).strip(),'original_title':m.group(0),'heading':title,'page':pages[i],'stars':1 if i<10 else 2 if i<27 else 3,'prompt':body}
 items.append(item)
 print(item['id'],item['page'],m.group(0),len(body))
(tmp/'items.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')
# Keep the external original intact and make Obsidian PDF page links portable.
source=Path('E:/200课内/考研/【无间隙】真题证明做题本 2025-12-4 132911 1.pdf')
copy=base/'09中值定理与证明-真题证明做题本-原始.pdf'
if copy.exists():
 assert copy.read_bytes()==source.read_bytes(), 'Different PDF already exists'
else:
 shutil.copy2(source,copy)
source_note=base/'09中值定理与证明-真题证明做题本-原题文字版.md'
solution_note=base/'09中值定理与证明-真题证明做题本-模板归类与详解.md'
assert not source_note.exists(), 'Target already exists; inspect before editing'
header='''---
主题: 真题证明题完整文字版
题数: 32
页数: 6
状态: 已按原题顺序转录并核校
---

# 真题证明做题本｜原题文字版

> 原书：**亚瑟爱数学《真题证明做题本》**。本文件只转录题目；详细证明见配套笔记。
> 原始 PDF：[[PDF]]
> 模板归类与逐题详解：[[SOL]]

> [!important] 数量以实际题目为准
> 原书标注“一星 10 道、二星 15 道、三星 5 道”，但逐页实际为 **10＋17＋5＝32 道**。本笔记使用 Q01—Q32 连续编号，**没有按错误的标题数量删题**。
> PDF 第 1—6 页的实际题数分别为 **5、5、5、6、5、6**。
> 保留原书年份、卷种、题号、分值及全部小问；删去重复页眉页脚，数学排版转换为 LaTeX。星级是原书编排，不代表本笔记对难度的重新判断。

原书星级说明：
- ★：比较适合学习某个定理的入门题及编者个人认为编写当年可能考类似内容的题。
- ★★：有些难度，但大部分人都能学会。
- ★★★：较难的题，原书建议实在不会可以放弃。

> [!note] 阅读约定与原文边界
> - 含 $\\ln x$ 的题默认取其定义域 $x>0$；2023 数二第 21 题的区间 $[-a,a]$ 按非退化区间理解，即 $a>0$。
> - Q25 的“在 $(a,b)$ 内二阶可导且存在相等的最大值”，详解按**两个函数均在开区间内取得相等的最大值**理解。这一取到位置不可删掉；仅有闭区间最大值相等不够，详解附反例说明。
> - Q32 的极限分子原文是 $f(2x-a)$，不是 $f^2(x-a)$；“极限存在”按有限极限理解。
> - Q11 保留原文 $f'(0)=f'(1)$，即使本题所列两个结论可以在不使用该条件时证明，也不擅自删改。

## 全题清单

| 编号 | 原题 | PDF 页码 | 星级 |
| --- | --- | --- | --- |
'''.replace('PDF',copy.as_posix()).replace('SOL',solution_note.as_posix())
# Avoid replacing the ordinary prose word PDF: repair accidental occurrences.
header=header.replace(copy.as_posix()+' 第','PDF 第').replace('原始 '+copy.as_posix(),'原始 PDF').replace('| '+copy.as_posix()+' 页码','| PDF 页码')
for item in items:
 header+=f"| [[#{item['heading']}|{item['id']}]] | {item['year']} {item['paper']} {item['original_title'].split(']',1)[1].strip()} | {item['page']} | {'★'*item['stars']} |\n"
body=''
for i,item in enumerate(items):
 if i in [0,10,27]:body+='\n## '+{0:'一星题｜10 道',10:'二星题｜实际 17 道（原书标题误标 15 道）',27:'三星题｜5 道'}[i]+'\n'
 body+=f"\n### {item['heading']}\n\n> 原始页面：[[{copy.as_posix()}#page={item['page']}|PDF 第 {item['page']} 页]] · 详细解析：[[{solution_note.as_posix()}#{item['id']}|{item['id']} 详解]]\n\n{item['prompt']}\n"
source_note.write_text(header+body,encoding='utf-8')
print('WRITTEN',source_note)
print(source_note.read_text(encoding='utf-8')[:600])
