from pathlib import Path
p=Path('.codex-tmp/math-20261120/prepare_checks.py')
t=p.read_text(encoding='utf-8-sig')
t=t.replace("ids=['IMG045','IMG073','IMG074','IMG102','IMG092','IMG153']", "ids=['IMG038','IMG039']")
(p.parent/'prepare_found_checks.py').write_text(t,encoding='utf-8')
