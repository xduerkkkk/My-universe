import json,base64,os,requests
from pathlib import Path
c=json.loads(Path('C:/Users/kkkkkk/.agents/skills/vision-support/config.json').read_text(encoding='utf-8-sig'))
m=c['models'][0]
key=m['apiKey']
if key.startswith('$'): key=os.environ[key[1:]]
urls=c.get('proxy',{}).get('urls',[])
proxy=os.environ.get('HTTPS_PROXY') or os.environ.get('HTTP_PROXY')
if not proxy:
 import winreg
 try:
  with winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Internet Settings') as h:
   proxy=winreg.QueryValueEx(h,'ProxyServer')[0]
   if '=' in proxy: proxy=dict(v.split('=',1) for v in proxy.split(';')).get('https')
 except OSError: pass
proxy=proxy or (urls[0] if urls else None)
if proxy and not proxy.startswith('http'): proxy='http://'+proxy
from urllib.parse import urlsplit
u=urlsplit(m['baseUrl'])
endpoint=f'{u.scheme}://{u.netloc}/gemini/v1beta/models/{m["model"]}:generateContent'
p=Path('_attachments/image/Pasted image 20261108104111.jpeg')
body={'contents':[{'role':'user','parts':[{'text':'仅转录图片中的题干、选项、公式、批注。不要解题，不要分析。不确定的符号标注不确定。'},{'inlineData':{'mimeType':'image/jpeg','data':base64.b64encode(p.read_bytes()).decode()}}]}],'generationConfig':{'temperature':0,'maxOutputTokens':4096}}
r=requests.post(endpoint,headers={'x-goog-api-key':key,'Authorization':'Bearer '+key},json=body,proxies={'https':proxy,'http':proxy} if proxy else None,timeout=65)
print('HTTP',r.status_code)
if r.ok:
 data=r.json(); text='\n'.join(p.get('text','') for p in data.get('candidates',[{}])[0].get('content',{}).get('parts',[]))
 Path('.codex-tmp/math-20261120/vision-test.txt').write_text(text,encoding='utf-8')
 print(text)
else: print(r.text[:500])
