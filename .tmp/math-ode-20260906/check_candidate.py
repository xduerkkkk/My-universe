from pathlib import Path
import json,importlib.util
p=Path('.tmp/math-ode-20260906');m=json.loads((p/'manifest.json').read_text(encoding='utf-8'))
m['target']=(p/'05题型总结-候选.md').as_posix()
(p/'candidate-manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
spec=importlib.util.spec_from_file_location('auditor','C:/Users/kkkkkk/.codex/skills/math-exercise-organizer/scripts/audit_math_summary.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
r=a.audit(p/'05题型总结-候选.md',p/'candidate-manifest.json','concise')
print(json.dumps(r,ensure_ascii=False,indent=2))
try:
 import sympy;print('sympy',sympy.__version__)
except ImportError:print('NO SYMPY')
