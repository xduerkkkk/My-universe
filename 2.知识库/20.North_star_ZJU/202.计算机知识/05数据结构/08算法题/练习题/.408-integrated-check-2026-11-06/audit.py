from pathlib import Path
import json,re,hashlib,sys
ROOT=Path('2.知识库/20.North_star_ZJU/202.计算机知识/05数据结构/08算法题')
CHECK=ROOT/'练习题/.408-integrated-check-2026-11-06'
SOURCE=ROOT if '--published' in sys.argv else CHECK/'staged'
formal=[SOURCE/'03算法题模板.md']+[SOURCE/'练习题'/n for n in ['算法分类训练-00总入口.md','算法分类训练-01-A数组与线性表.md','算法分类训练-02-L链表.md','算法分类训练-03-T树与递归.md','算法分类训练-04-S栈与队列.md','算法分类训练-05-G图.md','算法分类训练-06-H堆与排序.md','算法分类训练-公共约定.md','算法分类训练-整理与校验记录.md']]
lookup={p.stem:p for p in formal}
errors=[];links=0;faq=0;checkboxes=0;new_cards=0
for p in formal:
 s=p.read_text(encoding='utf-8')
 if '\ufffd' in s or '????' in s or re.search(r'[\x00-\x08\x0b-\x1f]',s):errors.append([p.name,'encoding'])
 faq+=s.count('> [!faq]-');checkboxes+=len(re.findall(r'^- \[ \]',s,re.M));new_cards+=len(re.findall(r'^### [ALTGSH]\d{2} ',s,re.M))
 if re.search(r'^\s*- \[[xX]\]',s,re.M):errors.append([p.name,'unexpected inherited completion'])
 if '<details>' in s or '<summary>' in s:errors.append([p.name,'HTML folding'])
 for target in re.findall(r'\[\[([^\]]+)\]\]',s):
  dest=target.split('|',1)[0].rstrip('\\');file,sep,anchor=dest.partition('#')
  if not file:q=p
  elif '/' in file:
   f=Path(file if file.endswith('.md') else file+'.md')
   if f.is_relative_to(ROOT):q=SOURCE/f.relative_to(ROOT)
   else:q=f
  else:q=lookup.get(file.removesuffix('.md'))
  if q is None or not q.is_file():errors.append([p.name,target,'missing target']);continue
  if q not in formal:errors.append([p.name,target,'outside formal notes']);continue
  if sep:
   hs=[re.sub(r'^#+\s+','',l).strip() for l in q.read_text(encoding='utf-8').splitlines() if re.match(r'^#+\s+',l)]
   if anchor not in hs:errors.append([p.name,target,'missing anchor'])
  links+=1
 lines=s.splitlines();fence=False
 for line in lines:
  if line.startswith('|'):
   for target in re.findall(r'\[\[([^\]]+)\]\]',line):
    if re.search(r'(?<!\\)\|',target):errors.append([p.name,'unescaped table link'])
  normal=line[2:] if line.startswith('> ') else '' if line=='>' else line
  if normal.startswith('```'):fence=not fence
 if fence:errors.append([p.name,'unbalanced code fence'])
assert new_cards==48 and checkboxes==96,(new_cards,checkboxes)
template=(SOURCE/'03算法题模板.md').read_text(encoding='utf-8')
assert len(re.findall(r'^### [ALTGSH]\d ',template,re.M))==24
assert not errors,errors
report={'source':'published' if SOURCE==ROOT else 'staged','formal_notes':len(formal),'cards':new_cards,'template_cards':24,'unchecked_boxes':checkboxes,'wiki_links':links,'faq_callouts':faq,'errors':errors}
if SOURCE==ROOT:
 before=json.loads((CHECK/'before-manifest.json').read_text(encoding='utf-8'));trash=Path('.trash/408算法训练-整合前-2026-11-06')
 mismatches=[]
 for rel,h in before.items():
  f=trash/rel
  if not f.exists() or hashlib.sha256(f.read_bytes()).hexdigest()!=h:mismatches.append(rel)
 assert not mismatches,mismatches
 report['archived_original_files_verified']=len(before)
 active=[p for p in ROOT.rglob('*.md') if CHECK not in p.parents]
 assert set(active)==set(formal),[str(p) for p in set(active)-set(formal)]
 report['active_markdown_only_formal']=True
(CHECK/'structural-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))