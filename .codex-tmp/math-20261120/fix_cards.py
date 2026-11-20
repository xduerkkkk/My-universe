from pathlib import Path
p=Path('.codex-tmp/math-20261120/cards.py')
t=p.read_text(encoding='utf-8-sig')
t=t.replace('②④取$a_n=1/n,b_n=1$', '②④取$a_n=1/n^2,b_n=1$')
t=t.replace('$x^2$与$\\sqrt{x}$在区间内部就给出相反的割线位置', '$x^2$与$2x-x^2$就给出相反的割线位置')
t=t.replace('反向若$\\sum a_n$收敛', '反向若$\\sum a_n$收敛')
p.write_text(t,encoding='utf-8')
print('patched math examples')
