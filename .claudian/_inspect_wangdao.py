from pathlib import Path
import re, hashlib
b=Path('2.\u77e5\u8bc6\u5e93')/'20.North_star_ZJU'/'202.\u8ba1\u7b97\u673a\u77e5\u8bc6'/'\u6570\u636e\u7ed3\u6784'
for d in ['04\u6811','05\u56fe\u8bba','06\u67e5\u627e']:
 p=b/d/'02\u738b\u9053\u9898.md'
 text=p.read_text(encoding='utf-8')
 lines=text.splitlines()
 print('\n'+'='*30, d, len(lines), 'lines', '='*30)
 print('sha256',hashlib.sha256(p.read_bytes()).hexdigest())
 for i,line in enumerate(lines,1):
  if re.match(r'^#{1,6}\s',line) or re.search(r'!{1,2}|\?',line) or re.search(r'!\[\[|!\[',line):
   s=line.replace('\t',' ')
   if len(s)>220:s=s[:217]+'...'
   print(f'{i:4}: {s}')
