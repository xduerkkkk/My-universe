from pathlib import Path
import re, json, subprocess, os, tempfile, hashlib
BASE=Path('2.知识库/20.North_star_ZJU/202.计算机知识/05数据结构/08算法题/练习题')
CHECK=BASE/'.408-template-check-2026-11-06'
common_text=(BASE/'算法分类训练-公共约定.md').read_text(encoding='utf-8')
blocks=re.findall(r'```cpp\n(.*?)\n```',common_text,re.S)
common=next(s for s in blocks if 'typedef struct BTNode' in s)
(CHECK/'common.hpp').write_text(common+'\n',encoding='utf-8')
codes={}
for fn in ['408新题训练-01树与递归.md','408新题训练-02图与遍历.md']:
 t=(BASE/fn).read_text(encoding='utf-8')
 for s in re.split(r'(?=^### N[TG]\d+ )',t,flags=re.M):
  m=re.match(r'### (N[TG]\d+) ',s)
  if not m: continue
  normal='\n'.join(l[2:] if l.startswith('> ') else '' if l=='>' else l for l in s.splitlines())
  b=re.findall(r'```cpp\n(.*?)\n```',normal,re.S)
  assert len(b)==1,(fn,m.group(1),len(b))
  codes[m.group(1)]=b[0]+'\n'
expected=json.loads((CHECK/'intended-code.json').read_text(encoding='utf-8'))
assert codes==expected
bin_dir=Path(tempfile.mkdtemp(prefix='kk408_template_'))
(CHECK/'binary-directory.txt').write_text(str(bin_dir),encoding='utf-8')
env=os.environ.copy(); env['PATH']=r'E:\MinGW\ucrt64\bin;'+env['PATH']
compiler=r'E:\MinGW\ucrt64\bin\g++.exe'
options=['-std=c++17','-Wall','-Wextra','-Werror','-pedantic','-O2']
strict=[]
for key,code in codes.items():
 src=CHECK/(key+'.cpp'); src.write_text(common+'\n'+code,encoding='utf-8')
 p=subprocess.run([compiler,*options,'-c',str(src),'-o',str(bin_dir/(key+'.o'))],env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
 strict.append({'id':key,'exit':p.returncode,'output':p.stdout+p.stderr})
 if p.returncode: raise RuntimeError(strict[-1])
(CHECK/'strict-core-results.json').write_text(json.dumps(strict,indent=2),encoding='utf-8')
harness=(CHECK/'harness.cpp').read_text(encoding='utf-8')
combined=common+'\n'+'\n'.join(codes.values())+'\n'+harness
src=CHECK/'all-tests.cpp'; src.write_text(combined,encoding='utf-8')
exe=bin_dir/'tests.exe'
p=subprocess.run([compiler,*options,str(src),'-o',str(exe)],env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
if p.returncode: raise RuntimeError(p.stdout+p.stderr)
p=subprocess.run([str(exe)],env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=120)
result={'compiler':compiler,'options':options,'strict_core_cards':len(strict),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'seed':20261106,'code_sha256':{k:hashlib.sha256(v.encode()).hexdigest() for k,v in codes.items()}}
(CHECK/'test-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
assert p.returncode==0