from pathlib import Path
p=Path('0.核心')/'00.规划(Plan)'/'2.当前项目'/'00-数学.md'
for i,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
    if i<=190:
        print(f'{i:04d}: {line}')
