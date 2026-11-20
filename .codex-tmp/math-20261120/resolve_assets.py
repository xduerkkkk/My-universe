from pathlib import Path
import json,hashlib
root=Path('.codex-tmp/math-20261120'); p=root/'inventory.json';inv=json.loads(p.read_text(encoding='utf-8'))
for i in inv['images']:
 if not i['exists']:
  a=Path('_attachments')/Path(i['path']).name
  if a.exists():
   i['path']=a.as_posix();i['exists']=True;i['sha256']=hashlib.sha256(a.read_bytes()).hexdigest()
p.write_text(json.dumps(inv,ensure_ascii=False,indent=2),encoding='utf-8')
t=(root/'ocr_all.py').read_text(encoding='utf-8');t=t[:t.index('import sys\npairs=')]
t+='\nchecks='+repr([i for i in inv['images'] if i['image_id'] in ['IMG038','IMG039']])+"\nwith concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex: results=list(ex.map(run,[(3000+int(im['image_id'][3:]),[im]) for im in checks]))\nprint(results,flush=True)\n"
(root/'ocr_found_assets.py').write_text(t,encoding='utf-8')
print('All assets resolved?',all(i['exists'] for i in inv['images']))
