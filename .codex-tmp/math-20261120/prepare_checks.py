from pathlib import Path
import json
from PIL import Image
root=Path('.codex-tmp/math-20261120')
inv=json.loads((root/'inventory.json').read_text(encoding='utf-8'))
ids=['IMG045','IMG073','IMG074','IMG102','IMG092','IMG153']
ims=[]
for im in inv['images']:
 if im['image_id'] in ids:
  p=root/(im['image_id']+'-read.png');image=Image.open(im['path']).convert('RGB');image.resize((image.width*2,image.height*2)).save(p)
  ii=dict(im);ii['path']=p.as_posix();ims.append(ii)
t=(root/'ocr_all.py').read_text(encoding='utf-8')
t=t[:t.index('import sys\npairs=')]
t+='\nchecks='+repr(ims)+'\nwith concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:results=list(ex.map(run,[(2000+int(im[\'image_id\'][3:]),[im]) for im in checks]))\nprint(\'CHECKS DONE\',results,flush=True)\n'
(root/'ocr_checks.py').write_text(t,encoding='utf-8')
print('Prepared',len(ims))
