# 基本类型
## Point 点
**构造**
```python
P=Point(x,y) #构造一个坐标为(x,y)的点
```
**属性**
```python
P.x #点P的x坐标
P.y #点P的y坐标
```
**方法**
```python
P.clear() #化简P的x和y坐标
P.dis(obj) #求P到obj对象的距离(obj可以为点、直线、线段、射线)
P.rotate(C,rad) #返回点P绕点C旋转rad弧度后的点
P.on(obj) #若点P在对象obj上则返回True，否则返回False(obj可以为直线、圆、线段、射线)
P.in_(obj) #若点P在圆obj内则返回True，否则返回False
P1+P2 #求以原点为起点，以点P1、P2为终点的两向量之和，返回其终点
k*P #求以原点为起点，以点P为终点的向量乘数量k后得到向量的终点
P1==P2 #若点P1点P2重合则返回True，否则返回False
```

## Line 直线
**构造**
```python
l=Line(A,B,C) #构造一条方程为Ax+By+C=0的直线
```
**属性**
```python
l.A #直线标准方程左侧x的系数
l.B #直线标准方程左侧y的系数
l.C #直线标准方程左侧的常数项
l.k #直线的斜率
l.eq #直线的方程(sympy的Equality等式对象)
```
**方法**
```python
l.sort() #将直线的方程各项常数分别化简
l.pointx(x) #返回直线上横坐标为x的点
l.pointy(y) #返回直线上纵坐标为y的点
l1+l2 #把直线转化为一次函数求和
l1*l2 #求两直线交点（相当于intersection(l1,l2)）
```

## Segline 线段
**构造**
```python
sl=Segline(A,B) #构造一条线段，两端点为A、B
```
**属性**
```python
sl.p1 , sl.p2 #线段的两端点
```
**方法**
```python
sl.len() #返回线段的长度
sl.par() #返回线段所在直线
sl.midpoint() #返回线段的中点
sl.pbline() #返回线段垂直平分线
```


## Ray 射线
**构造**
```python
r=Ray(O,P) #构造射线OP（端点为O）
```
**属性**
```python
r.O , r.P #构造射线的两点
```
**方法**
```python
r.par() #返回射线所在的直线
r.getpoint(lenn) #截射线上距端点距离为lenn的点
```
## Circle 圆
**构造**
```python
cc=Circle(o,r) #构造圆o为圆心，r为半径
```
**属性**
```python
cc.o #圆的圆心
cc.r #圆的半径
cc.d #圆的直径
cc.eq #圆的标准方程(sympy的Equality等式对象)
```
**方法**
```python
cc.s() #返回圆的面积
cc.c() #返回圆的周长
cc.pointx(x) #返回圆上横坐标为x的点（两点组成的元组）
cc.pointy(y) #返回圆上纵坐标为y的点（两点组成的元组）
```

## Angle 角
*提示：大量使用角会导致运行时间大大增加，例如解题示例中的题2*

**构造**
```python
a=Angle(A,O,B) #构造角AOB，O为顶点
```
**属性**
```python
a.A ,a.O ,a.B #构造角的三点
```
**方法**
```python
a.cos() #返回角的余弦值
a.cosf() #返回角的余弦值（浮点数）
a.sin() #返回角的正弦值
a.tan() #返回角的正切值
a.rad() #返回角的弧度值
a.radf() #返回角的弧度值（浮点数）
a.degf() #返回角的度数（浮点数）
a.bise() #返回角平分线（射线）
```
---
# 其他函数
```python
lineonpoints(p1,p2) #返回p1,p2两点所连直线
circleonpoints(p1,p2,p3) #返回p1,p2,p3所在圆
intersection(a,b) #返回a,b两对象交点(返回所有交点组成的列表)
parallel(p,l) #返回过点p的直线l的平行线
vertical(p,l) #返回过点p的直线l的垂线和垂足组成的元组
cutpoint(sl,p,lenn) #在线段sl上截点，使点到端点p的距离为lenn（p是sl端点之一）
tangent(p,cc) #返回过点p的圆cc的切线（返回两条切线组成的列表）
```
---
# 常量
```python
_o #原点
_x #x轴
_y #y轴
_c #圆心为原点，半径为1的单位圆
```
---
# 解题示例

```python
#test.py
from symgeo import * #导入模块
```

## 题1
![t1](./hmw.png "t1")
$如图,在\triangle ABC中AB=AC,\angle A=40^\circ,AD=CE,BC=CD$

$求\angle CDE$

(以点A为原点，射线AB为x轴正半轴)
```python
A=_o #点A为原点
B=Point(10,0) #点B(10,0)
C=B.rotate(A,deg2rad(40)) #点B绕A旋转40°记为点C
D=Point(C.x*2-B.x,0)
#使C的x坐标是D和B的x坐标的平均数，根据三线合一可得此时BC=CD
E=cutpoint(Segline(A,C),C,D.x)
#在线段AC上截点E使CE=AD(AD即D的x坐标)
EDC=Angle(E,D,C) #∠EDC
print(EDC.degf()) #以小数输出∠EDC度数
```
运行结果：
```
50.0000000000000
```
*运行时间约 0.1s*

---
## 题2
![t2](./9.png "t2")
$如图,点B,C,D共线,\angle BAC=80^\circ,\angle ABC和\angle ACD的平分线交于点P,连接AP$

$求\angle CAP$

(以点B为原点，射线BD为x轴正半轴)
```python
B=_o #点B为原点
A=Point(1,2) #点A(1,2)
C=intersection(_x,lineonpoints(A,B.rotate(A,deg2rad(80))))[0]
#点B绕A旋转80°得到B',C为直线BB'与x轴的交点
D=Point(100,0) #点D(100,0)
ABC=Angle(A,B,D) #∠ABC
ACD=Angle(A,C,D) #∠ACD
P=intersection(ABC.bise().par(),ACD.bise().par())[0]
#点P是∠ABC和∠ACD角平分线的交点
CAP=Angle(C,A,P) #∠CAP
print(CAP.degf()) #输出∠CAP的度数
```
运行结果：
```
50.0000000000000
```
*运行时间约 5~7s*

