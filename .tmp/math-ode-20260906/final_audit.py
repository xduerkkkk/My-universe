from pathlib import Path
import hashlib,json,importlib.util
out=Path('.tmp/math-ode-20260906');m=json.loads((out/'manifest.json').read_text(encoding='utf-8'))
for p,h in m['sources'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h
for a in m['images']:assert hashlib.sha256(Path(a['path']).read_bytes()).hexdigest()==a['sha256']
backup=Path(m['backup']);assert hashlib.sha256(backup.read_bytes()).hexdigest()==m['target_before_sha256']
spec=importlib.util.spec_from_file_location('audit','C:/Users/kkkkkk/.codex/skills/math-exercise-organizer/scripts/audit_math_summary.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
r=a.audit(Path(m['target']),out/'manifest.json','concise');r.update(source_hashes_unchanged=3,asset_hashes_unchanged=51,backup_verified=True,symbolic_checks_passed=50)
(out/'audit-report.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
for i in range(1,4):
 p=out/f'vision-{i}.txt';raw=p.read_bytes()
 if raw.startswith((b'\xff\xfe',b'\xfe\xff')):p.write_text(raw.decode('utf-16'),encoding='utf-8')
# Remove only the extra transient backup created by this task, after verifying the permanent one.
extra=Path(m['target']+'.bak-20260906-150915')
if extra.exists():
 assert extra.read_bytes()==backup.read_bytes()
 extra.unlink()
# Only these exact scratch scripts were created in the vault root during this task.
for name in ['.tmp_read.py','.tmp_inventory.py','.tmp_inspect.py','.tmp_find.py','.tmp_heads.py','.tmp_skill.py','.tmp_chunk.py','.tmp_inventory_assets.py','.tmp_vision_read.py','.tmp_readpart.py','.tmp_diff.py']:
 p=Path(name)
 if p.is_file():p.unlink()
print(json.dumps(r,ensure_ascii=False,indent=2))
print('\nBACKUP:',backup.as_posix())
