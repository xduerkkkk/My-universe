from pathlib import Path
p=Path('.tmp_plans_output.txt')
lines=p.read_text(encoding='utf-8').splitlines()
for a,b in [(1,180),(181,360),(361,540),(541,720),(721,900)]:
    print(f'===== LINES {a}-{b} =====')
    for line in lines[a-1:b]: print(line)
