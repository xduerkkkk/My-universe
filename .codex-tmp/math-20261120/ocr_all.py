from pathlib import Path
import json,requests,base64,os,time,concurrent.futures,hashlib,winreg,traceback
ROOT=Path('.codex-tmp/math-20261120'); OUT=ROOT/'ocr'; OUT.mkdir(exist_ok=True)
c=json.loads(Path('C:/Users/kkkkkk/.agents/skills/vision-support/config.json').read_text(encoding='utf-8-sig'));m=c['models'][0];key=m['apiKey'];key=os.environ.get(key[1:],'') if key.startswith('$') else key
proxy=os.environ.get('HTTPS_PROXY') or os.environ.get('HTTP_PROXY')
if not proxy:
 try:
  with winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Internet Settings') as h: proxy=winreg.QueryValueEx(h,'ProxyServer')[0]
  if '=' in proxy: proxy=dict(v.split('=',1) for v in proxy.split(';')).get('https')
 except OSError:pass
proxy=proxy or next(iter(c.get('proxy',{}).get('urls',[])),None)
if proxy and not proxy.startswith('http'):proxy='http://'+proxy
from urllib.parse import urlsplit
u=urlsplit(m['baseUrl']);endpoint=f'{u.scheme}://{u.netloc}/gemini/v1beta/models/{m["model"]}:generateContent'
inv=json.loads((ROOT/'inventory.json').read_text(encoding='utf-8'))
images=inv['images']
for i,im in enumerate(images):
 im['image_id']=f'IMG{i+1:03d}'
 if im['exists']: im['sha256']=hashlib.sha256(Path(im['path']).read_bytes()).hexdigest()
(ROOT/'inventory.json').write_text(json.dumps(inv,ensure_ascii=False,indent=2),encoding='utf-8')
jobs=[images[i:i+5] for i in range(0,len(images),5)]
def run(pair):
 num,ims=pair;dest=OUT/f'batch_{num:03d}.txt';state=OUT/f'batch_{num:03d}.json'
 if dest.exists() and state.exists() and json.loads(state.read_text()).get('ok'): return 'cached'
 prompt='你仅担任图片文字转录，不解题、不验证答案、不做主逻辑推理。下面每张图前有IMG编号。按同样编号分段，完整转录题号、题干、所有选项、公式、题中各小问、图示中的坐标和文字、可辨识的手写或彩色批注。若一图有多道独立题都要转录。图片是解析时也转录现有文字公式，不要自行补全推导。不清楚之处标[不确定]，不要猜。数学用LaTex。不得省略“看似重复”的选项和题目。每张图用 ### IMGxxx 开头。'
 parts=[{'text':prompt}]
 for im in ims:
  if not im['exists']:continue
  parts.extend([{'text':im['image_id']+' 文件：'+Path(im['path']).name},{'inlineData':{'mimeType':'image/png' if Path(im['path']).suffix.lower()=='.png' else 'image/jpeg','data':base64.b64encode(Path(im['path']).read_bytes()).decode()}}])
 body={'contents':[{'role':'user','parts':parts}],'generationConfig':{'temperature':0,'maxOutputTokens':20000}}
 for attempt in range(3):
  try:
   r=requests.post(endpoint,headers={'x-goog-api-key':key,'Authorization':'Bearer '+key},json=body,proxies={'https':proxy,'http':proxy} if proxy else None,timeout=150)
   if not r.ok: raise RuntimeError('HTTP '+str(r.status_code)+' '+r.text[:150])
   data=r.json();can=data.get('candidates',[{}])[0];reason=can.get('finishReason');text='\n'.join(p.get('text','') for p in can.get('content',{}).get('parts',[]) if not p.get('thought'))
   missing=[im['image_id'] for im in ims if im['exists'] and im['image_id'] not in text]
   if not text or reason=='MAX_TOKENS' or missing: raise RuntimeError(f'incomplete reason={reason} missing={missing}')
   dest.write_text(text,encoding='utf-8');state.write_text(json.dumps({'ok':True,'ids':[im['image_id'] for im in ims],'finishReason':reason,'chars':len(text)},ensure_ascii=False),encoding='utf-8')
   print(f'OK batch {num:03d} '+','.join(im['image_id'] for im in ims)+f' chars={len(text)}',flush=True)
   return 'ok'
  except Exception as e:
   print(f'RETRY batch {num:03d} attempt={attempt+1} {type(e).__name__}: {e}',flush=True)
   if attempt<2:time.sleep(3*(attempt+1))
 state.write_text(json.dumps({'ok':False,'ids':[im['image_id'] for im in ims]},ensure_ascii=False),encoding='utf-8');return 'failed'
import sys
pairs=list(enumerate(jobs))
if '--retry-single' in sys.argv:
 failed=[im for st in OUT.glob('batch_*.json') if not json.loads(st.read_text()).get('ok') for im in images if im['image_id'] in json.loads(st.read_text()).get('ids',[])]
 pairs=[(1000+int(im['image_id'][3:]),[im]) for im in {im['image_id']:im for im in failed}.values()]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:results=list(ex.map(run,pairs))
print('FINISHED', {s:results.count(s) for s in set(results)},flush=True)
