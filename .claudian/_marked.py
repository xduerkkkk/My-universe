from pathlib import Path
import re
b=Path('2.\u77e5\u8bc6\u5e93')/'20.North_star_ZJU'/'202.\u8ba1\u7b97\u673a\u77e5\u8bc6'/'\u6570\u636e\u7ed3\u6784'
for d in ['05\u56fe\u8bba','06\u67e5\u627e']:
 p=b/d/'02\u738b\u9053\u9898.md'; lines=p.read_text(encoding='utf-8').splitlines()
 print('\n###',d,'lines',len(lines))
 for i,l in enumerate(lines,1):
  # exclude image-only lines but keep marker in question header
  clean=re.sub(r'!\[\[[^\]]+\]\]','',l)
  if re.match(r'^\s*\d+\.\s',l) and any(x in clean for x in ['!','?','？']):
   print(i, l)
