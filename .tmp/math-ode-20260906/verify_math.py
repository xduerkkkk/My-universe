from pathlib import Path
import json,hashlib,re
import sympy as s
x,y=s.symbols('x y', real=True); C,C1,C2=s.symbols('C C1 C2');checks=[]
def zero(name,expr):
 z=s.simplify(s.expand(expr));assert z==0,(name,z);checks.append(name)
def ode(name,f,coeff,rhs,ics=()):
 zero(name,sum(c*s.diff(f,x,i) for i,c in enumerate(coeff))-rhs)
 for order,at,value in ics:zero(name+' initial '+str(order),s.diff(f,x,order).subs(x,at)-value)
E=s.exp; sin=s.sin;cos=s.cos;ln=s.log
ode('02-习2',E(3*x)-E(x)-x*E(2*x),[3,-4,1],x*E(2*x),[(0,0,0),(1,0,1)])
# The source-derived equation has forcing x*exp(2x), since P(2)=-1 and y_p=-x*exp(2x).
ode('02-习6',C1/x**2+C2,[0,3,x],0)
ode('02-习8 positive branch',C1*x**2+C2/x+x**2*ln(x)/3,[-2,0,x*x],x*x)
ode('03-4',((x+1)*E(-x)+(x-1)*E(x))/4,[1,2,1],x*E(x),[(0,0,0),(1,0,0)])
ode('03-5',C1*E(-x)+C2*E(x)+x*E(x),[-1,0,1],2*E(x))
ode('02-技1',(x**4/2-2*x*x+C1*x+C2)*E(x),[1,-2,1],(6*x*x-4)*E(x))
ode('02-技2',cos(x)+sin(x),[5,4,1],8*cos(x))
ode('04-3',C1/x**3+C2+x**3,[0,4/x,1],18*x)
ode('04-6',(sin(x)-1)/(x*x-1),[2*x,x*x-1],cos(x),[(0,0,1)])
ode('04-8',E(x)+E(-x)-x*x-2,[-1,0,1],x*x)
zero('04-8 high order',s.limit((E(x)+E(-x)-x*x-2)/x**2,x,0))
ode('04-9',C1*cos(x)+C2*sin(x)+x+x*sin(x)/2,[1,0,1],x+cos(x))
ode('04-10',1-cos(x)+sin(x),[1,0,1],1,[(0,0,0),(1,0,1)])
ode('04-11a',x**3/12+C1/x+C2,[0,2/x,1],x)
f=(C1*cos(2*x)+C2*sin(2*x)+E(x)/5)/cos(x)
zero('04-11b',s.trigsimp(cos(x)*s.diff(f,x,2)-2*sin(x)*s.diff(f,x)+3*cos(x)*f-E(x)))
ode('04-12',C1*E(x)+C2*(2*x+1),[2,-(2*x+1),2*x-1],0)
u=-(2*x+1)*E(-x);zero('04-12 u(-1)',u.subs(x,-1)-E(1));zero('04-12 u(0)',u.subs(x,0)+1)
for i,f in enumerate([x*E(x)+E(2*x),x*E(x)+E(x),x*E(x)+E(2*x)-E(x)]):ode('04-13a solution '+str(i),f,[2,-3,1],-E(x))
for i,f in enumerate([1,E(-x),2*E(-x)]):ode('04-13b solution '+str(i),s.sympify(f),[0,1,1],0)
for i,f in enumerate([E(x),x+E(x),x*x+E(x)]):ode('04-14 solution '+str(i),f,[2,-2*x,x*x],(x*x-2*x+2)*E(x))
ode('04-15',s.pi*E(s.atan(x)),[-1/(1+x*x),1],0,[(0,0,s.pi)])
zero('04-16',s.diff(s.tan(x),x)-1-s.tan(x)**2)
# Verify transformed linear forms, domains are checked in prose rather than simplified away.
u=(sin(x)-cos(x))/2+C*E(-x);ode('02-习5 u',u,[1,1],sin(x))
u=x+C*E(-x);ode('02-千6 u',u,[1,1],x+1)
f=x*x/4-ln(x)/2;ode('02-千11',f,[-4,2*x],2*ln(x)-1,[(0,1,s.Rational(1,4))]);zero('02-千11 average',s.integrate(f,(x,1,s.E))/(s.E-1)-(s.E**3-7)/(12*(s.E-1)))
f=y**3/2+C*y**3*E(1/y**2);zero('02-千4 reverse',s.diff(f,y)+(2/y**3-3/y)*f-1)
f=y*y+2*y*ln(y)-1+C*y;zero('04-7a reverse positive',s.diff(f,y)-f/y-(y+1)**2/y)
f=y**4*ln(y)/3-y**4/9+C*y;zero('04-7b reverse',s.diff(f,y)-f/y-y**3*ln(y))
f=C*(E(x)+cos(x)-sin(x)-2);ode('02-习11',f,[0,-1,1,-1,1],0);zero('02-习11 third order',s.limit(f/x**3,x,0)-C/3)
f=(1+4*s.pi*x*x)*E(4*s.pi*x*x);ode('02-习10',f,[-8*s.pi*x,1],8*s.pi*x*E(4*s.pi*x*x),[(0,0,1)])
zero('02-千5 limit',s.limit(x*ln(s.tan(x)-x),x,0,dir='+'))
print('SYMBOLIC CHECKS PASSED',len(checks))
Path('.tmp/math-ode-20260906/math-checks.json').write_text(json.dumps(dict(status='ok',checks=checks,note='符号代回、初值及部分极限；概念证明与定义域另行人工检查。'),ensure_ascii=False,indent=2),encoding='utf-8')
