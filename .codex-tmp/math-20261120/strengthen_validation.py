from pathlib import Path
p=Path('.codex-tmp/math-20261120/validate.py');t=p.read_text(encoding='utf-8-sig')
needle="t=Path(m['target']).read_text(encoding='utf-8')"
insert=r'''
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
'''
t=t.replace(needle,insert+'\n'+needle)
p.write_text(t,encoding='utf-8')
