import sympy as sp
import sympy.abc as sm


def f2f(fl): #小数转分数
    if type(fl)==type(1.0):
        i=1
        while fl%1!=0:
            fl*=10
            i*=10
        return sp.Rational(fl,i)
    else:
        return fl

def div(a,b): #除法
    a=sp.simplify(f2f(a))
    b=sp.simplify(f2f(b))
    if isinstance(b,int) and isinstance(a,int):
        return sp.Rational(a,b)
    return a/b

def rad2deg(rad):
    return 180*div(rad,sp.pi)

def deg2rad(deg):
    return sp.pi*div(deg,180)

class Point(): #点
    def __init__(self,x,y):
        self.x=f2f(x) #坐标
        self.y=f2f(y)
        self.type='point'
    def __repr__(self):
        return "<Point (%s , %s)>"%(self.x,self.y)
    def __add__(self,other): #把点作为向量求和
        return Point(self.x+other.x,self.y+other.y)
    def __rmul__(self,other): #把点作为向量进行数乘
        return Point(other*self.x,other*self.y)
    def __eq__(self,other): #同点
        if type(self)!=type(other):
            return False
        return self.x==other.x and self.y==other.y
    def clear(self):
        self.x=sp.simplify(self.x)
        self.y=sp.simplify(self.y)
    def dis(self,o):
        if o.type=='point': #点点距离
            return sp.sqrt((self.x-o.x)**2+(self.y-o.y)**2)
        elif o.type=='line': #点线距离
            res=div(sp.Abs(o.A*self.x+o.B*self.y+o.C),sp.sqrt(o.A**2+o.B**2))
            return res
        elif o.type in ('segline','ray'):
            return self.dis(o.par)
    
    def rotate(self,cp,radn): #绕点cp旋转
        x1,x2,y1,y2=self.x,cp.x,self.y,cp.y
        x=(x1-x2)*sp.cos(radn)-(y1-y2)*sp.sin(radn)+x2
        y=(x1-x2)*sp.sin(radn)+(y1-y2)*sp.cos(radn)+y2
        return Point(x,y)

    def on(self,par):
        if par.type=='line': #点是否在线上
            return self.x*par.A+self.y*par.B+par.C==0
        elif par.type=='circle': #点是否在圆上
            return (self.x-par.o.x)**2+(self.y-par.o.y)**2==par.r**2
        elif par.type=='segline': #点是否在线段上
            a=self.on(par.par)
            minx=sp.Min(par.p1.x,par.p2.x)
            maxx=sp.Max(par.p1.x,par.p2.x)
            miny=sp.Min(par.p1.y,par.p2.y)
            maxy=sp.Max(par.p1.y,par.p2.y)
            b=(minx<=self.x<=maxx and miny<=self.y<=maxy)
            return a and b
        elif par.type=='ray': #点是否在射线上
            return self.on(Segline(par.O,par.P)) or par.P.on(Segline(par.O,self))


    def in_(self,par): #点是否在圆内
        if par.type=='circle':
            return self.dis(par.o)<=par.r
            
class Line(): #直线
    def __init__(self,A,B,C):
        self.A=f2f(A)
        self.B=f2f(B)
        self.C=f2f(C)
        self.k=sp.oo
        self.eq=sp.Eq(self.A*sm.x+self.B*sm.y+self.C,0)
        self.type='line'
        if B!=0:
            self.k=div(-self.A,self.B) #斜率
    def __repr__(self):
        return "<Line Ax+By+C=0 A=%s B=%s C=%s>"%(self.A,self.B,self.C)
    def __add__(self,other): #把直线转化为一次函数求和
        A1,A2,B1,B2,C1,C2=self.A,other.A,self.B,other.B,self.C,other.C
        return Line(A1*B2+A2*B1,B1*B2,B1*C2+B2*C1)
    def __eq__(self,other): #同直线***
        if type(other)==type(self):
            return self.A==other.A and self.B==other.B and self.C==other.C
        return False
    def __mul__(self,other): #直线交点
        return intersection(self,other)
    def sort(self):
        self.A=sp.simplify(self.A)
        self.B=sp.simplify(self.B)
        self.C=sp.simplify(self.C)
        self.k=sp.simplify(self.k)
        self.eq=sp.Eq(self.A*sm.x+self.B*sm.y+self.C,0)
    def pointx(self,x): #已知x坐标的直线上的点
        if self.B!=0:
            y=div(-self.A,self.B)*x-div(self.C,self.B)
            return Point(x,y)
        else:
            return None
    def pointy(self,y): #已知y坐标的直线上的点
        if self.A!=0:
            x=div(-self.B,self.A)*y-div(self.C,self.A)
            return Point(x,y)
        else:
            return None

class Segline(): #线段
    def __init__(self,p1,p2):
        self.p1=p1
        self.p2=p2
        self._len=self._par=self._midpoint=self._pbline=None
        self.type='segline'
    def len(self):#线段长度
        if self._len==None:
            self._len=self.p1.dis(self.p2)
        return self._len
    def par(self):#线段所在直线
        if self._par==None:
            self._par=lineonpoints(self.p1,self.p2)
        return self._par
    def midpoint(self):
        if self._midpoint==None:
            self._midpoint=Point(div((self.p1.x+self.p2.x),2),div((self.p1.y+self.p2.y),2)) #中点
        return self._midpoint
    def pbline(self):
        if self._pbline==None:
            self._pbline=vertical(self.midpoint(),self.par())[0] #垂直平分线
        return self._pbline
    
    def __repr__(self):
        return '<segline (%s , %s)(%s , %s) on Ax+By+c=0 A=%s B=%s C=%s>'\
            %(self.p1.x,self.p1.y,self.p2.x,self.p2.y,self.par().A,self.par().B,self.par().C)

class Ray(): #射线
    def __init__(self,O,P):
        self.O=O
        self.P=P
        self._par=None
        self.type='ray'
    def par(self):
        if self._par==None:#射线所在直线
            self._par=lineonpoints(self.O,self.P)
        return self._par
    def __repr__(self):
        return '<Ray OP, O(%s,%s) P(%s,%s)>'%(self.O.x,self.O.y,self.P.x,self.P.y)
    def __eq__(self,other): #同射线
        if type(other)==type(self):
            return (self.P.on(Segline(self.O,other.P)) or other.P.on(Segline(self.O,self.P))) and self.O==other.O
        return False
    def getpoint(self,lenn): #截射线上距端点距离等于lenn的点
        sv=sp.solve([self.par.eq,sp.Eq((sm.x-self.O.x)**2+(sm.y-self.O.y)**2,lenn**2)],[sm.x,sm.y])
        p=Point(sv[0][0],sv[0][1])
        if p.on(self):
            return p
        else:
            return Point(sv[1][0],sv[1][1])

class Circle(): #圆
    def __init__(self,o,r):
        self.o=o #圆心
        self.r=f2f(r) #半径
        self.d=2*r #直径
        self._s=self._c=None
        self.eq=sp.Eq((sm.x-o.x)**2+(sm.y-o.y)**2,r**2) #方程
        self.type='circle'
    def s(self):
        if self._s==None:
            self._s=sp.pi*self.r*self.r #面积
        return self._s
    def c(self):
        if self._c==None:
            self._c=sp.pi*self.d #周长
        return self._c
    def __repr__(self):
        return '<circle (x-a)^2+(y-b)^2=r^2 a=%s b=%s r=%s>'%(self.o.x,self.o.y,self.r)
    def pointx(self,x): #已知x坐标的圆上的点
        y1=sp.sqrt(self.r**2-(x-self.o.x)**2)+self.o.y
        y2=-sp.sqrt(self.r**2-(x-self.o.x)**2)+self.o.y
        return Point(x,y1),Point(x,y2)
    def pointy(self,y): #已知y坐标的圆上的点
        x1=sp.sqrt(self.r**2-(y-self.o.y)**2)+self.o.x
        x2=-sp.sqrt(self.r**2-(y-self.o.y)**2)+self.o.x
        return Point(x1,y),Point(x2,y)

class Angle(): #角
    def __init__(self,A,O,B):
        self.O=O
        self.A=A
        self.B=B
        self.__a,self.__b,self.__c=self.O.dis(self.B),self.O.dis(self.A),self.A.dis(self.B)
        self.__fa,self.__fb,self.__fc=self.__a.evalf(),self.__b.evalf(),self.__c.evalf()
        self._cos=self._sin=self._tan=self._rad=self._degf=self._radf=self._bise=self._cosf=None
    def cos(self):
        if self._cos==None:
            self._cos=div(-self.__c**2+self.__a**2+self.__b**2,2*self.__a*self.__b)  #余弦
        return self._cos
    def sin(self):
        if self._sin==None:
            self._sin=div(self.__c,2*circleonpoints(self.O,self.A,self.B).r) #
        return self._sin
    def cosf(self):
        if self._cosf==None:
            self._cosf=div((-self.__fc.evalf()**2).evalf()+(self.__fa.evalf()**2).evalf()+(self.__fb.evalf()**2).evalf(),2*self.__fa.evalf()*self.__fb.evalf())
        return self._cosf
    def tan(self):
        if self._tan==None:
            self._tan=div(self.sin(),self.cos())
        return self._tan
    def rad(self):
        if self._rad==None:
            self._rad=sp.acos(self.cos())  #弧度精确值
        return self._rad
    def degf(self):
        if self._degf==None:
            self._degf=div(180*self.radf(),sp.pi).evalf()   #角度浮点值
        return self._degf
    def degf2(self):
        dx1,dx2,dy1,dy2=(self.A.x-self.O.x).evalf(),(self.B.x-self.O.x).evalf(),(self.A.y-self.O.y).evalf(),(self.B.y-self.O.y).evalf()
        # k1,k2=div(dy1,dx1),div(dy2,dx2)
        return rad2deg(sp.atan2(dx2,dy2)).evalf()-rad2deg(sp.atan2(dx1,dy1)).evalf()
        # return sp.atan(k2)-sp.atan(k1)
    def radf(self):
        if self._radf==None:
            self._radf=sp.acos(self.cosf())  #弧度浮点值
        return self._radf
    def bise(self):
        if self._bise==None:
            self._bise=Ray(self.O,cutpoint(Segline(self.A,self.B),self.A,self.__c*self.__b/(self.__a+self.__b)))#角平分线
        return self._bise
    def __repr__(self) -> str:
        return '<angle AOB, A(%s,%s) O(%s,%s) B(%s,%s)>'%(self.A.x,self.A.y,self.O.x,self.O.y,self.B.x,self.B.y)

# class Polygon(): #多边形
#     def __init__(self,vers):
#         self.n=len(vers) #边数
#         self.vers=vers #顶点
#         self.edges=[Segline(self.vers[i],self.vers[(i+1)%self.n]) for i in range(0,self.n)] #边
#         self.c=sum([sl.len for sl in self.edges]) #周长
#         self.s=0
#         for i in range(0,self.n):
#             self.s+=self.vers[i].x*self.vers[(i+1)%self.n].y-self.vers[(i+1)%self.n].x*self.vers[i].y
#         self.s=sp.Abs(div(self.s,2)) #面积
#     def __repr__(self):
#         pass


def lineonpoints(p1,p2): #作过点p1、p2的直线
    if p1.x==p2.x:
        A,B,C=1,0,-p1.x
    else:
        A=p2.y-p1.y
        B=p1.x-p2.x
        C=p2.x*p1.y-p1.x*p2.y
    return Line(A,B,C)

def circleonpoints(p1,p2,p3): #作过点p1、p2、p3的圆
    l12=Segline(p1,p2)
    l23=Segline(p2,p3)
    o=intersection(l12.pbline(),l23.pbline())
    if o==[]:
        return None
    r=o[0].dis(p1)
    return Circle(o[0],r)

def intersection(a,b): #求图形a、b的交点
    if a.type==b.type=='line': #直线a、b交点
        try:
            if a.k == b.k:
                return []
            A1,B1,C1,A2,B2,C2=a.A,a.B,a.C,b.A,b.B,b.C
            x=div((C2*B1-C1*B2),(A1*B2-A2*B1))
            y=div((C1*A2-C2*A1),(A1*B2-A2*B1))
            return [Point(x,y)]
        except ZeroDivisionError:
            return []
    else:
        res=sp.solve([a.eq,b.eq],(sm.x,sm.y))
        return [Point(i[0],i[1]) for i in res]

def parallel(p,l): #过点p作直线l的平行线
    c=-l.A*p.x-l.B*p.y
    return Line(l.A,l.B,c)

def vertical(p,l): #过点p作直线l的垂线
    k=-l.B*p.x-l.A*p.y
    res=Line(-l.B,l.A,k)
    return res,intersection(res,l)

def cutpoint(segl,p,lenn): #在线段segl上与端点p距离为lenn的点
    lenn=f2f(lenn)
    if p==segl.p1:
        p1,p2=p,segl.p2
    else:
        p1,p2=p,segl.p1
    return div(1,segl.len())*(lenn*p2+(segl.len()-lenn)*p1)

def tangent(p,cc): #过点p作圆cc的切线(最多2条)
    sl=Segline(cc.o,p)
    cl=Circle(sl.midpoint,div(sl.len,2))
    ps=intersection(cl,cc)
    res=[]
    for ip in ps:
        res.append(lineonpoints(ip,p))
    return res

_o=Point(0,0)
_x=Line(0,1,0)
_y=Line(1,0,0)
_c=Circle(_o,1)


if __name__=='__main__':
    print('--Start Running---\n')

    p1=Point(1,114)
    l1=lineonpoints(p1,_o)
    print(l1)

    print('\n---Finish Running---')
