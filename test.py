import formul
from formul import *

rc = 3
ri = 2.5
teta=120
Ec = 7
Eots = -5.2
ft = 12 * 10 ** 9
Ic0 = 0.076
Csk = 0.04 * 10 ** -12
Czk = 0.6 * 10 ** -12
Uc1 = 5.982
Ic1 = 0.10029
rkan = 10
Rek= 59.649

# верно
q0 = formul.Q0(teta=120, Ic0=Ic0, ft=ft, Csk=Csk, Czk=Czk, Eots=Eots, Ec=Ec, rc=rc, ri=ri)
print(f"q0 {q0}")
# верно
g1 = g1(teta)
print(f"g1 {g1}")
#верно
g0 = g0(180-teta)
print(f"g0 {g0}")
# верно
q1 = Q1(Czk=Czk, ft=ft, teta=teta, Eots=Eots, Ic1=Ic1, Csk=Csk, Uc1=Uc1)
print(f"q1 {q1}")
g2 = g_n(2, 180-teta)
print(f"g2 {g2}")
rkan1 = Rkan1(rkan=rkan, Q0=q0, Q1=q1, Ic1=Ic1, teta=teta, ft=ft)
print(f"rkan1 {rkan1}")
a = alfa(ft=ft, teta=teta, Csk=Csk, Rek=Rek)
print(f"a {a}")
b = beta(ft=ft, teta=teta, Csz1=1.843 * 10 ** -13, rkan1=rkan1, alfa=a)
print(f"b {b}")
c0 = C0(Csz1=1.843 * 10 ** -13, Csk=Csk, Czk1=6.509 * 10 ** -13)
print(f"c0 {c0}")
ksi = ksi(Csz1=1.843 * 10 ** -13, Czk1=6.509 * 10 ** -13, ft=ft, teta=teta, C0=2.357 * 10 ** -13, Rek=Rek)
print(f"ksi {ksi}")
roc = roc(ft=ft, teta=teta, Li=1.5 * 10 ** -10, ksi=ksi, beta=b, Rek=Rek, ri=ri, rc=rc)
print(f"roc {roc}")