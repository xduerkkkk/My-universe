from pathlib import Path
import json,re,random,hashlib
ROOT=Path('.codex-tmp/math-20261120');BASE=Path('2.知识库/20.North_star_ZJU/201.数学')
INV=json.loads((ROOT/'inventory.json').read_text(encoding='utf-8'));IMAGES={i['image_id']:i for i in INV['images']}
exec((ROOT/'write_outputs_part.py').read_text(encoding='utf-8-sig'))

# Resolve short vault links in the two method notes, too; table syntax must not split on math/wiki pipes.
def safe_tables(t):
 lines=[]
 for line in t.splitlines():
  if line.startswith('|'):
   def mathfix(m):
    text=m.group(1); count=0
    def pipe(n):
     nonlocal count
     count+=1
     return r'\lvert ' if count%2 else r'\rvert '
    return '$'+re.sub(r'(?<!\\)\|',pipe,text)+'$'
   line=re.sub(r'\$([^$]+)\$',mathfix,line)
   line=re.sub(r'\[\[([^\]|]+)\|[^\]]+\]\]',r'[[\1]]',line)
  lines.append(line)
 return '\n'.join(lines)+'\n'
for path in [TARGET,TRAIN,BASE/'04真题阶段/02数学做题框架/05级数.md',BASE/'04真题阶段/06卡片/01数列大题.md']:
 text=path.read_text(encoding='utf-8-sig')
 path.write_text(safe_tables(full_links(text)),encoding='utf-8')
