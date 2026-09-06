from pathlib import Path
import json,re,hashlib,importlib.util,copy
w=Path('_temp/math02_organizer'); lp=w/'concise_ledger.json'; m=json.loads(lp.read_text(encoding='utf-8')); t=Path(m['target']); text=t.read_text(encoding='utf-8')
for item in m['items']:
 match=re.search(r'^### '+re.escape(item['id'])+r'｜([^\n]+)\n(.*?)(?=^### |^## |\Z)',text,re.M|re.S)
 item['coverage']=match.group(1)+'；'+re.search(r'\*\*识别\*\*：([^\n]+)',match.group(2)).group(1)
original=json.loads((w/'ledger.json').read_text(encoding='utf-8'))
assert {r['block_id'] for r in m['items']}=={b['id'] for b in original}
lp.write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
spec=importlib.util.spec_from_file_location('audit','C:/Users/kkkkkk/.codex/skills/math-exercise-organizer/scripts/audit_math_summary.py'); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
results={}; report=mod.audit(t,lp); assert report['status']=='ok',report; results['real_note']=report
# Mutate isolated copies only. Original chapter source notes are never written.
f=w/'audit_fixtures'; f.mkdir(exist_ok=True); ft=f/'target.md'; fl=f/'ledger.json'
def run(name,body,manifest,fragment):
 manifest=copy.deepcopy(manifest); manifest['target']=ft.as_posix(); ft.write_text(body,encoding='utf-8'); fl.write_text(json.dumps(manifest,ensure_ascii=False),encoding='utf-8')
 r=mod.audit(ft,fl)
 assert r['status']=='failed' and any(fragment in e for e in r['errors']),(name,r)
 results[name]={'status':'expected rejection','errors':r['errors']}
run('missing_card',re.sub(r'^### 02-1a｜.*?(?=^### )','',text,count=1,flags=re.M|re.S),m,'coverage mismatch')
run('missing_steps',text.replace('1. 按 CDF','按 CDF',1),m,'consecutive steps')
x=copy.deepcopy(m); x['images'].pop(); run('unrecorded_image',text,x,'image coverage mismatch')
x=copy.deepcopy(m); x['items'][0]['source_link']='missing-source.md'; run('broken_source_link',text,x,'source mismatch')
run('encoding_damage',text+'\n????\n',m,'Encoding artifacts')
x=copy.deepcopy(m); src=next(iter(x['sources'])); fake=f/'source.md'; fake.write_bytes(Path(src).read_bytes()+b'\nmutation')
x['sources'][fake.as_posix()]=x['sources'].pop(src)
for it in x['items']:
 if it['source']==src: it['source']=fake.as_posix(); it['source_link']=it['source_link'].replace(src,fake.as_posix())
for im in x['images']:
 if im['source']==src: im['source']=fake.as_posix()
run('source_mutation',text.replace(src,fake.as_posix()),x,'Source hash changed')
# Hashes cover the four untouched source files, independent of the copied fixtures.
for source,h in m['sources'].items(): assert hashlib.sha256(Path(source).read_bytes()).hexdigest()==h
(w/'revision_validation.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v['status'] for k,v in results.items()},ensure_ascii=False,indent=2))
print('Source blocks:',len(original),'covered:',len({r['block_id'] for r in m['items']}))
print('Reduction:',round((1-len(text)/len((w/'revision_backup'/t.name).read_text(encoding='utf-8')))*100,1),'percent')
print(text[:2900])