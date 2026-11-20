from pathlib import Path
import json,re
root=Path('.codex-tmp/math-20261120');out={}
for p in sorted((root/'ocr').glob('batch_*.txt')):
 for match in re.finditer(r'(?m)^###\s+(IMG\d+)\s*\n',p.read_text(encoding='utf-8')):
  t=p.read_text(encoding='utf-8'); end=re.search(r'(?m)^###\s+IMG\d+',t[match.end():]); text=t[match.end():match.end()+end.start() if end else len(t)].strip()
  out[match.group(1)]={'text':text,'cache':p.as_posix()}
(root/'ocr-by-image.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print('TRANSCRIBED',len(out))
inv=json.loads((root/'inventory.json').read_text(encoding='utf-8'))
print('MISSING',[(i['image_id'],i['path']) for i in inv['images'] if i['image_id'] not in out])
for i in inv['images']:
 if 48<=int(i['image_id'][3:])<=73:
  print('\n'+i['image_id']+' '+i['source'].split('201.数学/')[1]+':\n'+out.get(i['image_id'],{}).get('text','PENDING'))
