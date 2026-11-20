from pathlib import Path
p=Path('.codex-tmp/math-20261120/ocr_all.py')
t=p.read_text(encoding='utf-8-sig')
a=t.index('with concurrent.futures.ThreadPoolExecutor')
t=t[:a]+'''import sys
pairs=list(enumerate(jobs))
if '--retry-single' in sys.argv:
 failed=[im for st in OUT.glob('batch_*.json') if not json.loads(st.read_text()).get('ok') for im in images if im['image_id'] in json.loads(st.read_text()).get('ids',[])]
 pairs=[(1000+int(im['image_id'][3:]),[im]) for im in {im['image_id']:im for im in failed}.values()]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:results=list(ex.map(run,pairs))
print('FINISHED', {s:results.count(s) for s in set(results)},flush=True)
'''
p.write_text(t,encoding='utf-8')
print('PATCHED')
