from pathlib import Path
import json,hashlib,re,importlib.util
out=Path('.tmp/math-ode-20260906');base=Path('2.知识库/20.North_star_ZJU/201.数学/01高等数学/06微分方程')
# Tighten image provenance to the actual exercise shown, not every exercise sharing a heading.
m=json.loads((out/'manifest.json').read_text(encoding='utf-8'))
mapping={1:['02-习1','02-习2'],2:['02-习1','02-习2'],15:['02-技1'],16:['02-技2'],36:['04-11a'],37:['04-11b'],38:['04-11b'],39:['04-11c'],42:['04-13a'],43:['04-13b'],48:['04-17a'],49:['04-17b','04-17c']}
solution_only={2,13,15,16,19,29,30,35,38,41,45,51}
for a in m['images']:
 idx=a['inventory_index']
 if idx in mapping:a['card_ids']=mapping[idx]
 a['role']='solution-only' if idx in solution_only else 'question-with-optional-solution'
 a['coverage_note']='通过精确源章节链接保留；同节多题在卡片中另附原图链接以定位。'
 if idx==11:a['coverage_note']+=' 上沿上一题残片缺题干，已登记排除。'
candidate=out/'05题型总结-候选.md';text=candidate.read_text(encoding='utf-8')
text=text.replace('的特解为 $e^{-x}+xe^x$，求通解；这是 03-5 的同题来源。','（$a,b,c$ 为常数）的特解为 $e^{-x}+xe^x$，求通解；这是 03-5 的同题来源。')
# Check text/annotation preservation against original source content: all substantive old prose exists in source notes.
old=(base/'05题型总结.md').read_text(encoding='utf-8'); source_text='\n'.join(Path(p).read_text(encoding='utf-8') for p in m['sources'])
unique=[l for l in old.splitlines() if l.strip() and l.strip() not in source_text and not l.lstrip().startswith(('#','>'))]
print('UNIQUE OLD NONHEADING LINES',unique)
assert not unique,unique
candidate.write_text(text,encoding='utf-8')
backup=base/'备份'/'05题型总结-重构前-20260906-150915.md'
m['backup']=backup.as_posix()
(out/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
cm={**m,'target':candidate.as_posix()};(out/'candidate-manifest.json').write_text(json.dumps(cm,ensure_ascii=False,indent=2),encoding='utf-8')
spec=importlib.util.spec_from_file_location('auditor','C:/Users/kkkkkk/.codex/skills/math-exercise-organizer/scripts/audit_math_summary.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
r=a.audit(candidate,out/'candidate-manifest.json','concise');assert r['status']=='ok',r
# Verify original target has not changed since it was fully read and backed up.
target=base/'05题型总结.md';raw=target.read_bytes()
assert hashlib.sha256(raw).hexdigest()==m['target_before_sha256'],'Target changed externally; do not overwrite'
oldbackup=base/'05题型总结.md.bak-20260906-150915'
assert oldbackup.read_bytes()==raw
backup.parent.mkdir(exist_ok=True)
assert not backup.exists(),'Backup path already exists'
backup.write_bytes(raw)
assert backup.read_bytes()==raw
for p,h in m['sources'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h
for a in m['images']:assert hashlib.sha256(Path(a['path']).read_bytes()).hexdigest()==a['sha256']
target.write_bytes(candidate.read_bytes())
assert target.read_bytes()==candidate.read_bytes()
print('TARGET UPDATED; BACKUP',backup.as_posix())
print('CHARACTERS',len(old),'->',len(text),'REDUCTION',round(100*(1-len(text)/len(old)),1),'%')
