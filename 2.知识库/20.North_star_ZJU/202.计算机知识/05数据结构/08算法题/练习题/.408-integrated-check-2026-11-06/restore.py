from pathlib import Path
import argparse,json,hashlib,shutil,datetime
ROOT=Path('2.知识库/20.North_star_ZJU/202.计算机知识/05数据结构/08算法题')
CHECK=ROOT/'练习题/.408-integrated-check-2026-11-06'
TRASH=Path('.trash/408算法训练-整合前-2026-11-06')
manifest=json.loads((CHECK/'before-manifest.json').read_text(encoding='utf-8'))
p=argparse.ArgumentParser(description='List originals or copy one archived file to a new recovery directory. Never overwrites current notes.')
p.add_argument('--list',action='store_true');p.add_argument('--file',help='Exact relative path from --list')
a=p.parse_args()
if a.list or not a.file:
 print('\n'.join(manifest));raise SystemExit(0)
if a.file not in manifest:raise SystemExit('Not in the original manifest.')
src=TRASH/a.file
if not src.resolve().is_relative_to(TRASH.resolve()):raise SystemExit('Unsafe source path.')
if hashlib.sha256(src.read_bytes()).hexdigest()!=manifest[a.file]:raise SystemExit('Archive hash does not match.')
folder=ROOT/('恢复资料-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
dst=folder/a.file
if not dst.resolve().is_relative_to(ROOT.resolve()) or dst.exists():raise SystemExit('Unsafe or existing destination.')
dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
print('Copied archived original to '+str(dst)+'. Current formal notes were not changed.')