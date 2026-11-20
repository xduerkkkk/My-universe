from pathlib import Path
import json,math
import numpy as np
from scipy.integrate import quad
import sympy as sp
root=Path('.codex-tmp/math-20261120');tests=[]
def check(name,got,expected,tol=1e-9):
 ok=abs(float(got)-float(expected))<=tol*(1+abs(float(expected)))
 tests.append({'name':name,'actual':str(got),'expected':str(expected),'ok':bool(ok)})
x,y,z=sp.symbols('x y z',positive=True)
U=x*y*sp.atan(2*y/x)
P=y*sp.atan(2*y/x)-2*x*y*y/(x*x+4*y*y)
Q=x*sp.atan(2*y/x)+2*x*x*y/(x*x+4*y*y)
check('G65 Ux=P',sp.simplify(sp.diff(U,x)-P),0)
check('G65 Uy=Q',sp.simplify(sp.diff(U,y)-Q),0)
t=sp.symbols('t');check('G66 projection integral',sp.integrate((1-2*t)**2*(1+2*t)+sp.Rational(3,2)*t,(t,0,sp.Rational(1,2))),sp.Rational(19,48))
n=np.ones(3)/np.sqrt(3);u=np.array([1,-1,0])/np.sqrt(2);v=np.cross(n,u);centre=np.ones(3)/2
# u cross v = n; observer at the origin sees this boundary clockwise.
def line(t):
 r=centre+.5*(u*np.cos(t)+v*np.sin(t));d=.5*(-u*np.sin(t)+v*np.cos(t));a,b,c=r
 return np.dot(np.array([2*b*c,2*c-c*c,b*b+2*a*b+3*b]),d)
check('G67 direct line integral',quad(line,0,2*np.pi,epsabs=1e-12)[0],np.sqrt(3)*np.pi/4)
check('G72 direct upper-hemisphere projection',3*(sp.pi/4+sp.pi),15*sp.pi/4)
a=sp.sqrt(3);xx=(-1-a)/2;yy=(-1-a)/4;zz=2+a
check('G78 feasible paraboloid',sp.simplify(zz-xx*xx-4*yy*yy),0)
check('G78 feasible plane',sp.simplify(xx+2*yy+zz),1)
check('G78 gradient norm squared',sp.simplify(4*xx**2+16*yy**2+4*zz**2),4*(9+5*a))
for A,B,C in [(3,0,2),(1,2,2)]:
 check(f'G82 tangent point {A,B,C}',A*A+2*B*B+3*C*C,21)
 check(f'G82 direction orthogonality {A,B,C}',2*A+2*B-3*C,0)
 check(f'G82 line point in plane {A,B,C}',6*A+6*B+sp.Rational(3,2)*C,21)
w=sp.symbols('w');sol=(3*w-1)*sp.exp(3*w)/36
check('G88 ODE residual',sp.simplify(sp.diff(sol,w,3)-2*sp.diff(sol,w,2)-3*sp.diff(sol,w)-sp.exp(3*w)),0)
for order,expected in [(0,-sp.Rational(1,36)),(1,0),(2,sp.Rational(1,4))]:check('G88 initial '+str(order),sp.diff(sol,w,order).subs(w,0),expected)
for N in range(1,6):
 numerical=(2/math.pi)*quad(lambda X:X*X*math.sin(N*X),0,math.pi,epsabs=1e-11)[0]
 expected=-2*math.pi*(-1)**N/N+4*((-1)**N-1)/(math.pi*N**3)
 check('G49 sine coefficient '+str(N),numerical,expected)
check('G106 minimum radius',(1+sp.Rational(1,2))**sp.Rational(3,2)*sp.sqrt(2),3*sp.sqrt(3)/2)
r={'status':'ok' if all(t['ok'] for t in tests) else 'failed','checks':len(tests),'tests':tests}
(root/'math-checks.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(r,ensure_ascii=False,indent=2))
