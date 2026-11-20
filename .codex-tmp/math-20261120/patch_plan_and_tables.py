from pathlib import Path
p=Path('.codex-tmp/math-20261120/write_outputs_part.py')
t=p.read_text(encoding='utf-8-sig')
t=t.replace("parts=[head]", "head+='\\n'+(ROOT/'use-plan.md').read_text(encoding='utf-8-sig').replace('###EXECPLANPLACEHOLDER\\n','')+'\\n'\nparts=[head]")
p.write_text(t,encoding='utf-8')
# Add normalization once so repeated renders keep table syntax safe.
p=Path('.codex-tmp/math-20261120/write_outputs.py')
t=p.read_text(encoding='utf-8-sig')
t+='''
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
     return r'\\lvert ' if count%2 else r'\\rvert '
    return '$'+re.sub(r'(?<!\\\\)\\|',pipe,text)+'$'
   line=re.sub(r'\\$([^$]+)\\$',mathfix,line)
   line=re.sub(r'\\[\\[([^\\]|]+)\\|[^\\]]+\\]\\]',r'[[\\1]]',line)
  lines.append(line)
 return '\\n'.join(lines)+'\\n'
for path in [TARGET,TRAIN,BASE/'04真题阶段/02数学做题框架/05级数.md',BASE/'04真题阶段/06卡片/01数列大题.md']:
 text=path.read_text(encoding='utf-8-sig')
 path.write_text(safe_tables(full_links(text)),encoding='utf-8')
'''
p.write_text(t,encoding='utf-8')
