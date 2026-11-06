from pathlib import Path
import re,json,hashlib
W=Path(__file__).parent
P=W.parent
B=P/'算法分类训练-改写前留档-2026-11-05'
manifest=json.loads((W/'before-manifest.json').read_text(encoding='utf-8'))
files=sorted(P.glob('算法分类训练-*.md'))
report={}
report['backup_files_verified']=0
for name,digest in manifest['changed'].items():
 assert hashlib.sha256((B/('原版-'+name)).read_bytes()).hexdigest()==digest,name
 report['backup_files_verified']+=1
report['untouched_files_verified']=0
for name,digest in manifest['untouched'].items():
 assert hashlib.sha256((P/name).read_bytes()).hexdigest()==digest,name
 report['untouched_files_verified']+=1

def sections(s):
 out={}
 for m in re.finditer(r'^### ([ALTHSG]\d{2}) ([^\n]+)\n(.*?)(?=^## |^### |\Z)',s,re.M|re.S):
  out[m.group(1)]={'title':m.group(2),'checks':re.findall(r'^- \[[ xX]\].*$',m.group(3),re.M),'body':m.group(3)}
 return out
old={};new={};heading_count=0
for f in P.glob('算法分类训练-0[1-6]-*.md'):
 s=f.read_text(encoding='utf-8');prev=(B/('原版-'+f.name)).read_text(encoding='utf-8-sig')
 old.update(sections(prev));new.update(sections(s))
 oldh=set(re.findall(r'^#{2,3} (.+)$',prev,re.M));newh=set(re.findall(r'^#{2,3} (.+)$',s,re.M))
 assert oldh<=newh,(f.name,oldh-newh)
 heading_count+=len(oldh)
 assert not re.search(r'^> ```c\s*$',s,re.M),f.name
 for block in re.findall(r'^> ```cpp\n(.*?)^> ```',s,re.M|re.S):
  assert not re.search(r'\bCAP\b|\bMAXV\b|\bmalloc\b|\bfree\s*\(|std::|vector\s*<',block),f.name
 assert '<details>' not in s and '<summary>' not in s
assert len(old)==72 and len(new)==85,(len(old),len(new))
for qid,c in old.items():
 assert c['title']==new[qid]['title'],qid
 assert c['checks']==new[qid]['checks'],(qid,c['checks'],new[qid]['checks'])
for qid in set(new)-set(old):assert all(line.startswith('- [ ]') for line in new[qid]['checks'])
report['old_numbered_cards_preserved']=len(old)
report['new_gap_transfer_cards']=len(new)-len(old)
report['old_heading_anchors_preserved']=heading_count
report['old_checked_items_preserved']=sum('[x]' in x.lower() for c in old.values() for x in c['checks'])
report['current_complete_cards']=sum('> ```cpp' in c['body'] for c in new.values())
report['archived_optional_cards']=sum('> ```cpp' not in c['body'] for c in new.values())
report['main_cards']=sum('**定位**：主练' in c['body'] for c in new.values())
report['foundation_cards']=sum('**定位**：基础积木' in c['body'] for c in new.values())
report['transfer_cards']=sum('**定位**：迁移选练' in c['body'] for c in new.values())
assert [report[x] for x in ['current_complete_cards','archived_optional_cards','main_cards','foundation_cards','transfer_cards']]==[31,54,19,10,2]

# Bounded link validation: current exercise directory, its algorithm parent,
# backups, and explicitly linked vault-relative files. No vault-wide scan.
short={f.stem:f for f in list(P.glob('*.md'))+list(P.parent.glob('*.md'))}
known={}
def heads(f):
 if f not in known:known[f]=set(re.findall(r'^#{1,6} (.+)$',f.read_text(encoding='utf-8-sig'),re.M))
 return known[f]
checked=0;errors=[]
for f in files:
 s=f.read_text(encoding='utf-8')
 assert '\ufffd' not in s and '????' not in s,f.name
 for raw in re.findall(r'\[\[([^\]]+)\]\]',s):
  dest=raw.split('|',1)[0].rstrip('\\')
  if '#' in dest:ref,anchor=dest.split('#',1)
  else:ref,anchor=dest,''
  if not ref:target=f
  else:
   path=Path(ref if ref.endswith('.md') else ref+'.md')
   candidates=[path,P/path,P.parent/path]
   target=next((q for q in candidates if q.is_file()),None)
   if target is None and '/' not in ref:target=short.get(ref.removesuffix('.md'))
  if target is None:errors.append((f.name,raw,'missing file'));continue
  if anchor and anchor not in heads(target):errors.append((f.name,raw,'missing heading'));continue
  checked+=1
 for line in s.splitlines():
  if line.startswith('|'):
   for link in re.findall(r'\[\[[^\]]+\]\]',line):assert not re.search(r'(?<!\\)\|',link),(f.name,line)
report['links_checked']=checked
report['link_errors']=errors
(W/'structural-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
