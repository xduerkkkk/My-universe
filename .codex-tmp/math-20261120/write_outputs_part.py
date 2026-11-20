# The writer uses only reviewed card data. It does not generate additional exercises.
ns={}
exec((ROOT/'cards.py').read_text(encoding='utf-8-sig'),ns)
CARDS=ns['CARDS']
REFBASE=BASE/'05思维课做题记录'
TARGET=REFBASE/'高数薄弱专题-归类.md'
TRAIN=REFBASE/'高数薄弱专题-随机训练.md'
CHANGED={str(BASE/'04真题阶段/02数学做题框架/05级数.md').replace('\\','/'):str(BASE/'04真题阶段/02数学做题框架/05级数-20261120整理前备份.md').replace('\\','/'),str(BASE/'04真题阶段/06卡片/01数列大题.md').replace('\\','/'):str(BASE/'04真题阶段/06卡片/01数列大题-20261120整理前备份.md').replace('\\','/')}
paths=[Path(s) for s in INV['sources']]+[TARGET,TRAIN]+[Path(s) for s in CHANGED.values()]
short={}
for p in paths:short.setdefault(p.stem,[]).append(p.as_posix())
def full_links(t):
 def sub(m):
  raw=m.group(1);link,*alias=raw.split('|',1);base,*anchor=link.split('#',1)
  if not base:return m.group(0)
  if '/' not in base and '\\' not in base:
   found=short.get(Path(base).stem,[])
   if len(found)==1:
    new=found[0]+(('#'+anchor[0]) if anchor else '')
    return '[['+new+'|'+(alias[0] if alias else base)+']]'
  return m.group(0)
 return re.sub(r'\[\[([^\]]+)\]\]',sub,t)
def clean(t):
 t=t.replace('\\prime',"'")
 return full_links(t)
firstconcept=['G01','G03','G04','G05','G06','G08','G10','G11','G12','G13','G14','G16','G17','G94','G95']
firstbig=['G21','G22','G23','G25','G31','G33','G34','G35','G40','G42','G43','G45','G46','G55','G58','G60','G62','G65','G67','G72','G78']
FIRST=firstconcept+firstbig
assert len(FIRST)==36 and len(set(FIRST))==36
byid={c['id']:c for c in CARDS}
assert all(i in byid for i in FIRST)
# Stable interleaving makes the blind page usable without a shuffle script or plugin.
rng=random.Random(20261120)
first=[byid[i] for i in FIRST];rng.shuffle(first)
rest=[c for c in CARDS if c['id'] not in FIRST];rng.shuffle(rest)
ordered=first+rest
for n,c in enumerate(ordered,1):c['tid']=f'T{n:03d}'
# Canonical sources keep the pre-edit text of the two changed targets available and hash-checked.
for c in CARDS:
 c['first_round']=c['id'] in FIRST
 c['source_links']=[]
 for iid in c['images']:
  im=IMAGES[iid];s=CHANGED.get(im['source'],im['source'])
  if s not in c['source_links']:c['source_links'].append(s)
 for rel,heading in c['refs']:
  p=BASE/rel;s=CHANGED.get(p.as_posix(),p.as_posix())
  if not Path(s).exists():raise RuntimeError('missing reference '+s)
  heads=re.findall(r'(?m)^#{1,6}\s+(.+)$',Path(s).read_text(encoding='utf-8-sig'))
  link=s+('#'+heading if heading in heads else '')
  if link not in c['source_links']:c['source_links'].append(link)
 assert c['source_links'],c['id']
 def wl(link):return '[['+link+'|'+Path(link.split('#')[0]).stem+(' · '+link.split('#')[1] if '#' in link else '')+']]'
 c['provenance']='> 原题与解析：'+'；'.join(wl(s) for s in c['source_links'])
 if c['images']:
  c['provenance']+='\n> 题图定位：'+'、'.join('[['+IMAGES[i]['path']+'|'+i+']]' for i in c['images'])
 c['body']='\n\n'.join([c['provenance'],'**识别**：'+c['prompt'],'\n'.join(f'{i}. {step}' for i,step in enumerate(c['steps'],1)),'**易错**：'+c['pitfall'],'> [!faq]- 核对结果\n> '+c['answer'],'> 不提示题型重做：[['+TRAIN.as_posix()+'#'+c['tid']+'|'+c['tid']+']]'+('；首轮代表题。' if c['first_round'] else '；备用或查漏，不要求清空。')])
 c['body']=clean(c['body'])
nav=[]
for cat in dict.fromkeys(c['category'] for c in CARDS):nav.append('- [[#'+cat+'|'+cat+']]')
head=f'''# 高数薄弱专题｜归类

> 配套：[[{TRAIN.as_posix()}|不提示题型的训练页]]。方法总入口：[[{(BASE/'04真题阶段/02数学做题框架/05级数.md').as_posix()}|级数框架]]、[[{(BASE/'04真题阶段/06卡片/01数列大题.md').as_posix()}|数列大题]]、[[{(BASE/'04真题阶段/02数学做题框架/03曲线面积分，空间几何.md').as_posix()}|你自己的线面框架]]。

**不是再加一轮题。** 这里把指定材料中的高数卡点合并成{len(CARDS)}张可查的卡，其中有同题合并，也有一张图拆成几道独立题；大量是你已经做过的。先只做下面的**36张代表卡**，其余留查漏、补第二问和低频复测。不把文件长度当成剩余任务量。

- 查方法看本页；要检验会不会做，去训练页，不先看分类标题。原题、批注、图片不搬家也不改。
- 首轮15张概念卡可以分次做，每次约3张；另外21张是计算、证明或判敛代表题，每次约2张，长题只做1张。题号不代表难度。
- 做错、慢、靠提示的，2—3天后脱离提示再做。不是每张卡都配一个新变式；本次**没有新出训练变式**，复用原题及已存在的变式，并校正其中的错误。
- 标“消灭”的题以低频或备用为主；线面是你本轮重新反馈不稳的部分，所以保留少量旧题短测。没有把旧标记当成已掌握证明。
- 题干已转为文字，原图仍是核对依据；若文字与图有出入，先以图核实并修正对应卡，不把OCR当数学依据。

## 先做这36张，不从头通读

**概念15张**：'''+ '、'.join('[[#'+i+'｜'+byid[i]['title']+'|'+i+']]' for i in firstconcept)+'''

**计算／证明／判敛21张**：'''+ '、'.join('[[#'+i+'｜'+byid[i]['title']+'|'+i+']]' for i in firstbig)+'''

训练页T001—T036就是这些题的固定混排；T037起为备用。概念题不要求长篇证明，但要能说出依据或给出反例；大题需要把关键过程写出来。

## 按卡点查

'''+ '\n'.join(nav)+'''

## 旧材料里的这些话，先不要再背

| 旧说法／旧答案 | 本次处理 |
| --- | --- |
| 原级数收敛，乘上交错号再除n仍必收敛 | 错。见G55的成对反例；旧变式答案A改为D。 |
| 已知两级数收敛且$|a_n|\\le b_n+c_n$、c绝收，a绝收只是b绝收的必要条件 | 漏掉$b_n+c_n\\ge0$且可求和。a、b都必绝收，见G58。 |
| 收敛半径$R\\ge r$就必须逐项满足$|a_n|\\le r^{{-n}}$ | 错。这只是某些题的够用证明法，不是必要条件；界中也可有常数C。 |
| 两个常数夹住积分系数，就得到$C/n$的精确等价 | 只能先得到同阶的上下界；求根值极限可能已足够，不能偷换成等价。 |
| F递减、奇偶子列各有极限，或F只有一个不动点，就说明整列收敛 | 还需证明两个子列极限相同，排除二周期。见数列卡片。 |
| 只要有界就可乘收敛级数，仍收敛 | 必须区分绝收与条件收敛；乱乘符号会破坏相消。 |
| f连续，所以导函数极限就等于该点导数 | 还要给旁边可导、导函数有限极限存在等条件；连续本身不够。 |
| 复合内层穿过极限点，就不能用链式法则 | 这是混淆复合极限与求导。链式法则按内外函数在相应点可导等条件判断，不能这样一刀切。 |
| 只看分母是否有奇数次，就说多元极限“有歧义不考” | 不采用。始终在定义域内按路径与统一估计判断，见G94。 |
| 反函数旧例题给f导数在1为3，另一个恒等式却推出它为1 | 条件冲突。公式可用，具体例题暂不背答案；见G101。 |
| 投影区域$-2\\le y\\le2,0\\le z\\le2-y$是梯形 | 应为三角形，不等式范围不变，见G98。 |

'''
head+='\n'+(ROOT/'use-plan.md').read_text(encoding='utf-8-sig').replace('###EXECPLANPLACEHOLDER\n','')+'\n'
parts=[head]
for cat in dict.fromkeys(c['category'] for c in CARDS):
 parts.append('## '+cat+'\n')
 for c in CARDS:
  if c['category']==cat:parts.append('### '+c['id']+'｜'+c['title']+'\n\n'+c['body']+'\n')
# Account for reference-only images and mixed-subject blocks without pretending they are exercises to redo.
used={i for c in CARDS for i in c['images']}
outs={2,3,4,5,6,7,14,15,16,17,18,79,80,81,82,83,85,87,90,94,95,96,98,100,101,102,103,107,108,110,111,115,121,122,123,124,125,126,128,129,130,131,132,134,135,136,137,138,139,140,142,143,145}
for im in INV['images']:
 iid=im['image_id'];im['source_link']=CHANGED.get(im['source'],im['source']);im['block_id']=iid
 ids=[c['id'] for c in CARDS if iid in c['images']]
 im['card_ids']=ids
 if ids:
  im['disposition']='source-linked';im['coverage']='已转成卡片或与题图合并；'+','.join(ids)
 elif int(iid[3:]) in outs:
  im['disposition']='out-of-scope';im['coverage']='图中为概率或线代，不进入本轮高数训练；原文件、图片保留。'
 else:
  im['disposition']='reference-only';im['coverage']='补充框架、公式、推导或已有卡片的例题；保留原入口，不另扩成首轮训练。'
 im['source_sha256']=INV['sources'][im['source']]
source_table=[]
for source in INV['sources']:
 ims=[i for i in INV['images'] if i['source']==source]
 n=sum(i['disposition']=='source-linked' for i in ims)
 out=sum(i['disposition']=='out-of-scope' for i in ims)
 source_table.append('| [['+CHANGED.get(source,source)+'|'+Path(source).stem+']] | '+str(len(ims))+' | '+str(n)+' | '+('混有概率／线代，只取高数；其余图片和文字留原处。' if out else '无图的文字卡片按方法复用；已有展开例题和推导不重复搬运。')+' |')
parts.append('''## 素材处理说明

- 已读题图转录并结合原批注分类；一图中的独立题（如空间圆3道、根值判敛3道）已拆卡，同题题图与手写解析合并。
- 本轮只新增这两份高数归类／训练，改写级数框架、补数列卡片。概率、线代原文件与总规划不改。
- 两个改写目标的整理前备份可直接打开。其余源文件与全部附件以SHA-256核验未变；逐图处置及转录缓存在任务临时目录，不要求你维护。
- “参考保留”不是漏收：背景框架图、公式表、同题解析、已经有完整方法的示例，不再重复塞进首轮。若原图只有解析片段而没有完整题干，不捏造题目。

| 来源 | 图像处数 | 已关联本页卡片 | 其余怎么处理 |
| --- | ---: | ---: | --- |
'''+ '\n'.join(source_table)+'\n')
TARGET.write_text(clean('\n'.join(parts)),encoding='utf-8')
trainhead=f'''# 高数薄弱专题｜不提示题型训练

> 配套：[[{TARGET.as_posix()}|按卡点查方法]]。全部复用本轮指定材料中的原题与既有变式，未另出新题。**T001—T036是首轮代表题**，顺序已固定打乱；T037起只作备用，不是第二轮必须清空的任务。

- 不先打开归类页。概念题先判断并说依据，大题先写第一行与关键过程，再算结果。
- 每次用原数学时段：可以做3张短概念卡，或1—2张计算／证明卡；长题只做一道也可以。别为赶题号跳过订正。
- 折叠区同时放步骤、答案、原题图和归类链接。只记得结论但说不出条件的，不算做稳。
- 答案记住了不必马上换题：隔2—3天，混到别的题中，再检验自己能否无提示写完整。若已经连续两次无提示做顺，就降低频率，别为了“有得刷”重复抄。
- 旧变式中有两道实质性错答，已经在本页答案中校正；一份反函数例题条件冲突，备用卡只核对公式，不要求你解冲突题。

## 首轮代表题｜T001—T036

'''
tr=[trainhead]
for n,c in enumerate(ordered,1):
 if n==37:tr.append('## 备用与低频复测｜按需抽，不要求清空\n')
 tr.append('### '+c['tid']+'\n\n'+clean(c['prompt'])+'\n\n> [!faq]- 做完再核对\n'+ '\n'.join('> '+str(i)+'. '+clean(s) for i,s in enumerate(c['steps'],1))+'\n>\n> **结果**：'+clean(c['answer'])+'\n>\n> **这题易错**：'+clean(c['pitfall'])+'\n>\n> 卡点与方法：[['+TARGET.as_posix()+'#'+c['id']+'｜'+c['title']+'|'+c['id']+']]\n> '+c['provenance'].replace('\n> ','\n> ').lstrip('> ')+'\n')
TRAIN.write_text(clean('\n'.join(tr)),encoding='utf-8')
ledger={'version':2,'mode':'concise','target':TARGET.as_posix(),'training':TRAIN.as_posix(),'sources':{CHANGED.get(s,s):h for s,h in INV['sources'].items()},'items':[],'images':INV['images'],'first_round':FIRST,'source_blocks':INV['source_blocks'],'scope_policy':'仅高数；混合源中的概率线代明确排除；方法背景图与重复解析参考保留；伴随图可跨源关联同卡。'}
for c in CARDS:
 ledger['items'].append({'id':c['id'],'block_id':c['images'][0] if c['images'] else c['source_links'][0], 'source':c['source_links'][0].split('#')[0],'source_link':c['source_links'][0],'source_links':c['source_links'],'category':c['category'],'coverage':c['prompt'],'image_ids':c['images'],'first_round':c['first_round'],'training_id':c['tid']})
for image in ledger['images']:
 image['original_source']=image['source']
 image['source']=CHANGED.get(image['source'],image['source'])
(ROOT/'manifest.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'cards-reviewed.json').write_text(json.dumps(CARDS,ensure_ascii=False,indent=2),encoding='utf-8')
print('WROTE',len(CARDS),'cards;',len(FIRST),'first-round;',len(ordered),'training entries')
print('reference-only images',sum(i['disposition']=='reference-only' for i in INV['images']),'out-of-scope',sum(i['disposition']=='out-of-scope' for i in INV['images']))
print('TARGET CHARS',len(TARGET.read_text(encoding='utf-8')),'TRAIN CHARS',len(TRAIN.read_text(encoding='utf-8')))
