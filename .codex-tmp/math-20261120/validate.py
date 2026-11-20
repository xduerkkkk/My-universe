from pathlib import Path
import json,re,hashlib,collections
root=Path('.codex-tmp/math-20261120');m=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
base=Path('2.知识库/20.North_star_ZJU/201.数学')
targets=[base/'04真题阶段/02数学做题框架/05级数.md',base/'04真题阶段/06卡片/01数列大题.md',Path(m['target']),Path(m['training'])]
errors=[];warnings=[]
# Resolve short links only within explicitly read sources / outputs / backups, never by scanning the vault.
known=[Path(p) for p in m['sources']]+targets
stemmap=collections.defaultdict(list)
for p in known:
 if p.as_posix() not in stemmap[p.stem]:stemmap[p.stem].append(p.as_posix())
for p in targets:
 t=p.read_text(encoding='utf-8-sig')
 if '\ufffd' in t or '????' in t or re.search(r'\\u[0-9a-fA-F]{4}',t):errors.append('encoding '+str(p))
 if len(re.findall(r'(?m)^# ',t))!=1:errors.append('H1 '+str(p))
 if t.count('$$')%2:errors.append('unbalanced display math '+str(p))
 for raw in re.findall(r'\[\[([^\]]+)\]\]',t):
  link=raw.split('|')[0].rstrip('\\');where,*anchor=link.split('#',1)
  if not where: q=p
  else:
   q=Path(where)
   if not q.exists() and not q.suffix:q=Path(where+'.md')
   if not q.exists() and '/' not in where:
    options=stemmap.get(Path(where).stem,[])
    if len(options)==1:q=Path(options[0])
  if not q.exists():errors.append('broken link '+str(p)+' :: '+link);continue
  if anchor and q.suffix=='.md':
   hs=re.findall(r'(?m)^#{1,6}\s+(.+?)\s*$',q.read_text(encoding='utf-8-sig'))
   if anchor[0] not in hs:errors.append('broken heading '+str(p)+' :: '+link)
 for lno,line in enumerate(t.splitlines(),1):
  if line.startswith('|'):
   for math in re.findall(r'\$([^$]+)\$',line):
    if '|' in math:warnings.append(f'table math pipe {p}:{lno}')
   for raw in re.findall(r'\[\[([^\]]+)\]\]',line):
    if '|' in raw and '\\|' not in raw:warnings.append(f'table wiki pipe {p}:{lno}')
for s,d in m['sources'].items():
 if hashlib.sha256(Path(s).read_bytes()).hexdigest()!=d:errors.append('source changed '+s)
for im in m['images']:
 p=Path(im['path'])
 if not p.exists():errors.append('missing image '+im['image_id'])
 elif hashlib.sha256(p.read_bytes()).hexdigest()!=im['sha256']:errors.append('image changed '+im['image_id'])
 if im['disposition'] not in ['source-linked','reference-only','out-of-scope']:errors.append('no disposition '+im['image_id'])
 if not im.get('coverage'):errors.append('no reason '+im['image_id'])
 if im['disposition']=='source-linked' and not im['card_ids']:errors.append('no cards '+im['image_id'])

# Source image occurrence identity: relative attachment shorthand is matched by the original basename.
actual=collections.Counter()
for source in m['sources']:
 body=Path(source).read_text(encoding='utf-8-sig')
 for raw in re.findall(r'!\[\[([^\]]+)\]\]',body):
  asset=raw.split('|')[0].split('#')[0]
  if Path(asset).suffix.lower() in ['.png','.jpg','.jpeg','.gif','.webp','.bmp','.svg']:
   actual[(source,Path(asset).name)]+=1
recorded=collections.Counter((i['source'],Path(i['path']).name) for i in m['images'])
if actual!=recorded:errors.append('source image occurrence mismatch '+str(actual-recorded)+' '+str(recorded-actual))
for im in m['images']:
 if im['source'] not in m['sources']:errors.append('image source not hashed '+im['image_id'])
 for cid in im['card_ids']:
  rec=next((v for v in m['items'] if v['id']==cid),None)
  if not rec or im['image_id'] not in rec['image_ids']:errors.append('image/card link mismatch '+im['image_id'])

t=Path(m['target']).read_text(encoding='utf-8')
heads=re.findall(r'(?m)^### (G\d+[A-Z]?)｜(.+)$',t);ids=[a for a,b in heads]
if len(ids)!=len(set(ids)):errors.append('duplicate cards')
if set(ids)!={c['id'] for c in m['items']}:errors.append('card coverage mismatch')
for cid,body in re.findall(r'(?ms)^### (G\d+[A-Z]?)｜[^\n]+\n(.*?)(?=^### |^## |\Z)',t):
 steps=re.findall(r'(?m)^(\d+)\. ',body)
 if steps not in [['1','2','3'],['1','2','3','4']]:errors.append('steps '+cid)
 if '**识别**：' not in body or '**易错**：' not in body or '> 原题与解析：' not in body:errors.append('structure '+cid)
 if '[!faq]-' not in body:errors.append('answer not collapsed '+cid)
 if len(body)>1200:warnings.append('long card '+cid+' '+str(len(body)))
tr=Path(m['training']).read_text(encoding='utf-8')
tids=re.findall(r'(?m)^### (T\d+)\s*$',tr)
if len(tids)!=len(ids) or len(tids)!=len(set(tids)):errors.append('training coverage')
for tid,body in re.findall(r'(?ms)^### (T\d+)\s*\n(.*?)(?=^### |^## |\Z)',tr):
 front=body.split('> [!faq]-')[0]
 if re.search(r'\[\[.*?#G\d+',front):errors.append('premature type hint '+tid)
 if '[!faq]-' not in body:errors.append('training no answer '+tid)
# Check pre-edit content remains byte-identical in both backups.
for source,backup in [(base/'04真题阶段/02数学做题框架/05级数.md',base/'04真题阶段/02数学做题框架/05级数-20261120整理前备份.md'),(base/'04真题阶段/06卡片/01数列大题.md',base/'04真题阶段/06卡片/01数列大题-20261120整理前备份.md')]:
 if backup.as_posix() not in m['sources']:errors.append('backup not hash recorded')
ocr=json.loads((root/'ocr-by-image.json').read_text(encoding='utf-8'))
missing=[i['image_id'] for i in m['images'] if i['image_id'] not in ocr]
report={'status':'ok' if not errors else 'failed','cards':len(ids),'first_round':len(m['first_round']),'training':len(tids),'source_files_unchanged_or_original_backed_up':len(m['sources']),'image_occurrences':len(m['images']),'source_linked':sum(i['disposition']=='source-linked' for i in m['images']),'reference_only':sum(i['disposition']=='reference-only' for i in m['images']),'out_of_scope':sum(i['disposition']=='out-of-scope' for i in m['images']),'ocr_missing':missing,'errors':errors,'warnings':warnings}
(root/'validation-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
