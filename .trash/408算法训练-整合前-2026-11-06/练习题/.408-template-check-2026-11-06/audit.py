from pathlib import Path
import json,re,hashlib
BASE=Path('2.知识库/20.North_star_ZJU/202.计算机知识/05数据结构/08算法题/练习题')
CHECK=BASE/'.408-template-check-2026-11-06'
names=['408新题训练-00树图样稿入口.md','408新题训练-01树与递归.md','408新题训练-02图与遍历.md','408新题训练-设计与校验记录.md']
modified=['算法分类训练-00总入口.md','算法分类训练-公共约定.md']
before=json.loads((CHECK/'before-manifest.json').read_text(encoding='utf-8'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
changed=[];missing=[]
for name,h in before.items():
 p=BASE/name
 if not p.exists():missing.append(name)
 elif digest(p)!=h:changed.append(name)
assert sorted(changed)==sorted(modified),(changed,modified)
assert not missing,missing
# Only inspect the requested exercise directory and its direct parent for short wiki targets.
lookup={}
for p in list(BASE.rglob('*.md'))+list(BASE.parent.glob('*.md')):
 lookup.setdefault(p.stem,[]).append(p)
links=0;callouts=0;errors=[]
for name in names+modified:
 text=(BASE/name).read_text(encoding='utf-8')
 assert '\ufffd' not in text and not re.search(r'[\x00-\x08\x0b-\x1f]',text),name
 assert '????' not in text,name
 callouts+=text.count('> [!faq]-')
 for body in re.findall(r'\[\[([^\]]+)\]\]',text):
  target=body.split('|',1)[0].rstrip('\\')
  filename,sep,anchor=target.partition('#')
  if not filename: p=BASE/name
  else:
   with_ext=filename if filename.endswith('.md') else filename+'.md'
   candidates=[Path(with_ext),BASE/with_ext]
   resolved=[p for p in candidates if p.is_file()]
   if not resolved:resolved=lookup.get(Path(filename).stem,[])
   if len(resolved)!=1:
    errors.append([name,body,'target missing/ambiguous',list(map(str,resolved))]);continue
   p=resolved[0]
  if sep:
   headers=[re.sub(r'^#+\s+','',line).strip() for line in p.read_text(encoding='utf-8').splitlines() if re.match(r'^#+\s+',line)]
   if anchor not in headers:errors.append([name,body,'anchor missing'])
  links+=1
 for line in text.splitlines():
  if line.startswith('|'):
   for body in re.findall(r'\[\[([^\]]+)\]\]',line):
    if re.search(r'(?<!\\)\|',body):errors.append([name,'unescaped table alias',line])
 # Normalize callout prefixes to check fence parity.
 lines=[line[2:] if line.startswith('> ') else '' if line=='>' else line for line in text.splitlines()]
 assert sum(line.startswith('```') for line in lines)%2==0,name
 assert '<details>' not in text and '<summary>' not in text,name
assert not errors,errors
new_cards='\n'.join((BASE/n).read_text(encoding='utf-8') for n in names[1:3])
assert len(re.findall(r'^### N[TG]\d+ ',new_cards,re.M))==8
assert new_cards.count('- [ ]')==16
report={'audited_markdown':len(names+modified),'wikilinks_checked':links,'faq_callouts':callouts,'original_files_hashed':len(before),'original_files_unchanged':len(before)-len(changed),'original_files_changed_only':changed,'missing_original_files':missing,'errors':errors,'new_cards':8,'fresh_checkboxes':16}
(CHECK/'structural-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))