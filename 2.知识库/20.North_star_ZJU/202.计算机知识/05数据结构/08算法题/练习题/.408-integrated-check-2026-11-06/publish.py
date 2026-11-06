from pathlib import Path
import json,hashlib,shutil,sys
ROOT=Path('2.知识库/20.North_star_ZJU/202.计算机知识/05数据结构/08算法题')
BASE=ROOT/'练习题';CHECK=BASE/'.408-integrated-check-2026-11-06';STAGE=CHECK/'staged'
TRASH=Path('.trash/408算法训练-整合前-2026-11-06')
keep=[Path('03算法题模板.md')]+[Path('练习题')/name for name in ['算法分类训练-00总入口.md','算法分类训练-01-A数组与线性表.md','算法分类训练-02-L链表.md','算法分类训练-03-T树与递归.md','算法分类训练-04-S栈与队列.md','算法分类训练-05-G图.md','算法分类训练-06-H堆与排序.md','算法分类训练-公共约定.md','算法分类训练-整理与校验记录.md']]
if (CHECK/'published.json').exists():
    raise SystemExit('Already published; refusing a second publish.')
assert len(list(STAGE.rglob('*.md')))==10
before=json.loads((CHECK/'before-manifest.json').read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for rel,h in before.items():assert (ROOT/rel).exists() and sha(ROOT/rel)==h,('source changed since snapshot',rel)
assert not TRASH.exists(),'Archive already exists; refusing to mix backups.'
assert TRASH.resolve().is_relative_to(Path('.trash').resolve())
assert ROOT.resolve().is_relative_to(Path('.').resolve())
move=[]
for p in ROOT.iterdir():
 if p==BASE or p==ROOT/'03算法题模板.md':continue
 move.append(p)
for p in BASE.iterdir():
 if p==CHECK or p.relative_to(ROOT) in keep:continue
 move.append(p)
for p in move:
 # Validate resolved absolute source and destination before any recursive directory move.
 assert p.resolve().is_relative_to(ROOT.resolve()),str(p)
 assert not p.resolve().is_relative_to(CHECK.resolve()),str(p)
 d=TRASH/p.relative_to(ROOT)
 assert d.resolve().is_relative_to(TRASH.resolve()),str(d)
 assert not d.exists(),str(d)
print(json.dumps({'archive':str(TRASH),'rewrite_with_backup':[str(x) for x in keep],'move_roots':[str(p.relative_to(ROOT)) for p in move],'original_files':len(before)},ensure_ascii=False,indent=2))
if '--execute' not in sys.argv:raise SystemExit('Dry run only. Pass --execute after review.')
result=json.loads((CHECK/'test-results.json').read_text(encoding='utf-8'));assert result['exit']==0 and result['strict_core_cards']==48
for rel in keep:
 src=ROOT/rel;dst=TRASH/rel;dst.parent.mkdir(parents=True,exist_ok=True)
 shutil.copy2(src,dst);assert sha(src)==sha(dst)
# All backups exist before replacing active content.
for rel in keep:
 source=STAGE/rel;target=ROOT/rel;assert source.is_file()
 shutil.copy2(source,target);assert sha(source)==sha(target)
for source in move:
 dest=TRASH/source.relative_to(ROOT)
 assert source.resolve().is_relative_to(ROOT.resolve()) and dest.resolve().is_relative_to(TRASH.resolve())
 dest.parent.mkdir(parents=True,exist_ok=True)
 shutil.move(str(source),str(dest))
for rel,h in before.items():assert sha(TRASH/rel)==h,('archive mismatch',rel)
report={'archive':str(TRASH),'archived_original_files':len(before),'moved_roots':len(move),'backed_up_rewritten_notes':len(keep),'active_notes':[str(r) for r in keep]}
(CHECK/'published.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
(TRASH/'archive-manifest.json').write_text(json.dumps(before,ensure_ascii=False,indent=2),encoding='utf-8')
print('PUBLISHED: originals verified byte-for-byte in archive.')