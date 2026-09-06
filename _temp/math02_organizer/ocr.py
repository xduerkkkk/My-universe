from pathlib import Path
import json,requests,os,base64,sys
c=json.loads(Path('C:/Users/kkkkkk/.agents/skills/vision-support/config.json').read_text(encoding='utf-8'));m=c['models'][0];key=m.get('apiKey') or os.environ.get(m.get('apiKeyEnv',''),'');w=Path('_temp/math02_organizer')
prompt='OCR only. For every IMAGE label transcribe the printed question, formulas and handwritten annotations in Chinese. Distinguish independent questions from answer continuations. Do not solve or classify. Mark unreadable text; do not guess. Be concise.'
for n in sys.argv[1:]:
 body={'contents':[{'role':'user','parts':[{'text':prompt},{'inlineData':{'mimeType':'image/jpeg','data':base64.b64encode((w/f'sheet_{n}.jpg').read_bytes()).decode()}}]}],'generationConfig':{'maxOutputTokens':7000,'temperature':0.1}}
 try:
  r=requests.post(m['baseUrl'].rstrip('/')+'/models/gemini-3.6-flash:generateContent',headers={'x-goog-api-key':key,'Authorization':'Bearer '+key},json=body,timeout=120)
  print('SHEET',n,'HTTP',r.status_code,flush=True)
  if r.ok:
   data=r.json();text='\n'.join(p.get('text','') for p in data['candidates'][0]['content']['parts']);(w/f'vision_{n}.txt').write_text(text,encoding='utf-8');(w/f'usage_{n}.json').write_text(json.dumps(data.get('usageMetadata')),encoding='utf-8');print('saved chars',len(text),'finish',data['candidates'][0].get('finishReason'),flush=True)
  else:print(r.text[:150],flush=True)
 except Exception as e:print(type(e).__name__,flush=True)
