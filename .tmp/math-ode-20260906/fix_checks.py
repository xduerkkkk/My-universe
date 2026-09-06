from pathlib import Path
p=Path('.tmp/math-ode-20260906/verify_math.py')
s=p.read_text(encoding='utf-8-sig').replace('(E(x)+E(-x)-x*x-2)/x*x,x,0','(E(x)+E(-x)-x*x-2)/x**2,x,0')
s=s.replace("ode('04-16',s.tan(x),[-(1+s.tan(x)**2)/s.tan(x),1],0)","zero('04-16',s.diff(s.tan(x),x)-1-s.tan(x)**2)")
p.write_text(s,encoding='utf-8')
