from pathlib import Path
import re
b=Path('2.\u77e5\u8bc6\u5e93')/'20.North_star_ZJU'/'202.\u8ba1\u7b97\u673a\u77e5\u8bc6'/'\u6570\u636e\u7ed3\u6784'
p=b/'04\u6811'/'02\u738b\u9053\u9898.md'
lines=p.read_text(encoding='utf-8').splitlines()
starts=[]
for i,l in enumerate(lines):
 if re.match(r'^#\s',l) or re.match(r'^\s*\d+\.\s',l): starts.append(i)
starts.append(len(lines))
section=''
for a,bb in zip(starts,starts[1:]):
 first=lines[a]
 if first.startswith('# '): section=first; continue
 header=first
 marker_header=re.sub(r'!\[\[[^\]]+\]\]','',header)
 if '!' in marker_header or '?' in marker_header or '？' in marker_header:
  print(f'\n--- L{a+1} {section} ---')
  for j in range(a,min(bb,a+45)):
   print(f'{j+1:4}: {lines[j]}')
  if bb-a>45: print(f'... ({bb-a-45} more lines)')
