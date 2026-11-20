from pathlib import Path
import re,json,hashlib,shutil
base=Path('2.知识库/20.North_star_ZJU/201.数学')
tmp=Path('.codex-tmp/math-20261120');tmp.mkdir(parents=True,exist_ok=True)
paths=[]
for folder in ['04真题阶段/05反复做','04真题阶段/06卡片','05思维课做题记录/卡片']:
 for p in (base/folder).rglob('*.md'):
  if any(s in p.name for s in ['概率','线代','正定','二次型','配方法','条件概率','反例库']): continue
  paths.append(p)
for name in ['04真题阶段/00数学记忆.md','05思维课做题记录/高数1.md','05思维课做题记录/高数变式题.md','04真题阶段/02数学做题框架/03曲线面积分，空间几何.md','04真题阶段/02数学做题框架/05级数.md','04真题阶段/02数学做题框架/01极限函数.md','04真题阶段/02数学做题框架/02导数.md','04真题阶段/02数学做题框架/04多元微分.md']:
 paths.append(base/name)
paths=sorted(set(paths))
inv={'sources':{},'images':[],'source_blocks':[]}
full=[]
for p in paths:
 t=p.read_text(encoding='utf-8-sig'); sp=p.as_posix(); inv['sources'][sp]=hashlib.sha256(p.read_bytes()).hexdigest()
 full.append('\n'+'='*40+'\n'+sp+'\n'+'='*40+'\n'+t)
 heading=''; top=''; count=0
 for ln,line in enumerate(t.splitlines(),1):
  if line.startswith('# '):top=line[2:].strip()
  if line.startswith('#'):heading=line.lstrip('#').strip()
  for embed in re.findall(r'!\[\[([^\]]+)\]\]',line):
   target=embed.split('|')[0].split('#')[0]
   a=Path(target)
   if not a.exists(): a=p.parent/target
   im={'path':a.as_posix(),'source':sp,'line':ln,'heading':heading,'top':top,'exists':a.exists(),'disposition':'pending','card_ids':[]}
   if p.name=='00数学记忆.md' and top in []:pass
   inv['images'].append(im);count+=1
 print(p.relative_to(base).as_posix(),len(t),'chars',count,'embeds')
 for section in re.split(r'(?m)(?=^#{1,6} )',t):
  if section.strip(): inv['source_blocks'].append({'source':sp,'heading':section.splitlines()[0][:180],'text':section})
(tmp/'inventory.json').write_text(json.dumps(inv,ensure_ascii=False,indent=2),encoding='utf-8')
(tmp/'all-source-text.txt').write_text('\n'.join(full),encoding='utf-8')
for name in ['04真题阶段/02数学做题框架/05级数.md','04真题阶段/06卡片/01数列大题.md']:
 p=base/name;dest=p.with_name(p.stem+'-20261120整理前备份.md')
 if dest.exists():
  if dest.read_bytes()!=p.read_bytes(): print('EXISTING BACKUP DIFFERENT:',dest)
 else: shutil.copy2(p,dest)
 print('BACKUP',dest.as_posix())
print('TOTAL',len(paths),'sources',len(inv['images']),'occurrences',len(set(i['path'] for i in inv['images'])),'unique assets')
