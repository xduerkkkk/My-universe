from pathlib import Path
import json,re,subprocess,os,tempfile,hashlib,sys
ROOT=Path('2.知识库/20.North_star_ZJU/202.计算机知识/05数据结构/08算法题')
CHECK=ROOT/'练习题/.408-integrated-check-2026-11-06'
STAGE=CHECK/'staged'
SOURCE=ROOT if '--published' in sys.argv else STAGE
manifest=json.loads((CHECK/'cards.json').read_text(encoding='utf-8'))
codes={}
for file in (SOURCE/'练习题').glob('算法分类训练-0[1-6]-*.md'):
 text=file.read_text(encoding='utf-8')
 for part in re.split(r'(?=^### [ALTGSH]\d{2} )',text,flags=re.M):
  m=re.match(r'### ([ALTGSH]\d{2}) ',part)
  if not m:continue
  normalized='\n'.join(l[2:] if l.startswith('> ') else '' if l=='>' else l for l in part.splitlines())
  b=re.findall(r'```cpp\n(.*?)\n```',normalized,re.S)
  assert len(b)==1,(file.name,m.group(1),len(b))
  codes[m.group(1)]=b[0]+'\n'
assert len(codes)==48,len(codes)
for c in manifest:assert codes[c['id']]==c['code'],c['id']
common=(CHECK/'common.hpp').read_text(encoding='utf-8')
bin_dir=Path(tempfile.mkdtemp(prefix='kk408_integrated_'))
(CHECK/'binary-directory.txt').write_text(str(bin_dir),encoding='utf-8')
env=os.environ.copy();env['PATH']=r'E:\MinGW\ucrt64\bin;'+env['PATH']
compiler=r'E:\MinGW\ucrt64\bin\g++.exe'
options=['-std=c++17','-Wall','-Wextra','-Werror','-pedantic','-O2']
strict=[]
for id,code in sorted(codes.items()):
 src=CHECK/(id+'.cpp');src.write_text(common+'\n'+code,encoding='utf-8')
 p=subprocess.run([compiler,*options,'-c',str(src),'-o',str(bin_dir/(id+'.o'))],env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
 strict.append({'id':id,'exit':p.returncode,'output':p.stdout+p.stderr})
 if p.returncode:raise RuntimeError(strict[-1])
(CHECK/'strict-core-results.json').write_text(json.dumps(strict,ensure_ascii=False,indent=2),encoding='utf-8')
parts=[common]
for id,code in sorted(codes.items()):parts.append('namespace '+id+' {\n'+code+'}\n')
parts+=['using namespace '+id+';' for id in sorted(codes)]
parts.append((CHECK/'harness.cpp').read_text(encoding='utf-8'))
src=CHECK/'all-tests.cpp';src.write_text('\n'.join(parts),encoding='utf-8')
exe=bin_dir/'tests.exe'
p=subprocess.run([compiler,*options,str(src),'-o',str(exe)],env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
if p.returncode:raise RuntimeError(p.stdout+p.stderr)
p=subprocess.run([str(exe)],env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
results={'source':'published' if SOURCE==ROOT else 'staged','strict_core_cards':len(strict),'compiler':compiler,'options':options,'seed':20261106,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'code_sha256':{id:hashlib.sha256(c.encode()).hexdigest() for id,c in sorted(codes.items())}}
(CHECK/'test-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in results.items() if k!='code_sha256'},ensure_ascii=False,indent=2))
assert p.returncode==0