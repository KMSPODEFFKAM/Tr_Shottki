from formul import *
from parametrs import *

text = {
    "Амплитуда первой гармоники тока стока": [Ic1(teta=120, Ec=7, Ec0=parametrs_tranzitions(1)[5], rc=parametrs_tranzitions(1)[14], ri=parametrs_tranzitions(1)[13], Pc1=.3), "А"],
    "Амплитуда первой гармоники напряжения на стоке": [10, "В"]
}

keysList = list(text.keys())
valueList = list(text.values())