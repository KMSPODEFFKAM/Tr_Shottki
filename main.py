import math
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem, QLabel
from PyQt5.QtGui import QFont
import sqlite3
import formul
import parametrs
from UIRS import Ui_MainWindow
from Form2 import Ui_MainWindow2
from Form3 import Ui_MainWindow3


class FirstW(QMainWindow, Ui_MainWindow):
    def __init__(self, number_tr):
        super(FirstW, self).__init__()
        self.uif = Ui_MainWindow()
        self.uif.setupUi(self)
        self.number_tr = number_tr

        self.uif.lineEdit.textChanged.connect(self.calc_teta_pc)
        self.uif.lineEdit_3.textChanged.connect(self.calc_teta_pc)
        self.uif.pushButton.clicked.connect(self.F2show)
        self.uif.pushButton_3.clicked.connect(self.F3show)

        if number_tr == -1:
            self.name = '1. Транзистор не выбран'
            self.uif.lineEdit.setEnabled(False)
            self.uif.lineEdit_2.setEnabled(False)
            self.uif.lineEdit_3.setEnabled(False)
            self.uif.lineEdit_4.setEnabled(False)
            self.uif.pushButton.setEnabled(False)
        else:
            self.name_tr = parametrs.parametrs_tranzitions(number_tr)[1]
            self.name = f"1. Выбран транзистор: {self.name_tr}"
            self.e_si_dop = float(parametrs.parametrs_tranzitions(number_tr)[24])
            self.e_c0 = float(parametrs.parametrs_tranzitions(number_tr)[5])
            self.v = 0.5 * (self.e_si_dop + self.e_c0)
            self.e_ots = float(parametrs.parametrs_tranzitions(number_tr)[3])
            self.rc = float(parametrs.parametrs_tranzitions(number_tr)[13])
            self.ri = float(parametrs.parametrs_tranzitions(number_tr)[14])

        self.uif.label.setText(self.name)

    def F2show(self):
        pc1 = float(self.uif.lineEdit_2.text())
        uip = float(self.uif.lineEdit.text())
        us = float(self.uif.lineEdit_3.text())
        f = float(self.uif.lineEdit_4.text())
        teta = formul.teta_formul(E=self.e_ots, Us=us, Uip=uip)
        pc1max = formul.pc1max(teta=teta, Ec=uip, Ec0=self.e_c0, rc=self.rc, ri=self.ri, Icnas=0.2)

        if us < self.v:
            if pc1 < pc1max:
                self.sw = SecW(uip=uip, pc1=pc1,
                               teta=teta, f=f,
                               e_ots=self.e_ots, rc=self.rc, ri=self.ri, number_tr=self.number_tr)
                self.sw.show()
            else:
                QMessageBox.critical(self, "Ошибка", "Мощность на стоке должна быть меньше максимальной!")
        else:
            QMessageBox.critical(self, "Ошибка", f"Большое напряжение смещение для транзистора {self.name_tr}. "
                                                 f"Необходимо уменьшить напряжение смещения чтобы было меньше {self.v} В")

    def F3show(self):
        '''Переход на третье окно'''
        self.tF = TrW()
        self.tF.show()
        self.close()

    def calc_teta_pc(self):
        try:
            us = float(self.uif.lineEdit_3.text())
            uip = float(self.uif.lineEdit.text())
            e_ots = float(parametrs.parametrs_tranzitions(self.number_tr)[3])
            teta = formul.teta_formul(E=e_ots, Us=us, Uip=uip)
            pc1max = formul.pc1max(teta=teta, Ec=uip, Ec0=self.e_c0, rc=self.rc, ri=self.ri, Icnas=0.2)
            self.uif.label_8.setText(f"{round(teta, 4)}")
            self.uif.label_4.setText(f"<{round(pc1max, 3)} Вт")
        except ValueError:
            self.uif.label_8.setText('teta не определена')
            self.uif.label_4.setText('pc1max не определена')


class SecW(QMainWindow, Ui_MainWindow2):
    def __init__(self, uip, pc1, teta, f, e_ots, rc, ri, number_tr):
        super(SecW, self).__init__()
        self.uis = Ui_MainWindow2()
        self.uis.setupUi(self)

        self.ec0 = float(parametrs.parametrs_tranzitions(number_tr)[5])
        self.ft = float(parametrs.parametrs_tranzitions(number_tr)[7]) * 10 ** 9
        self.czk = float(parametrs.parametrs_tranzitions(number_tr)[8]) * 10 ** -12
        self.csz = float(parametrs.parametrs_tranzitions(number_tr)[9]) * 10 ** -12
        self.csk = float(parametrs.parametrs_tranzitions(number_tr)[10]) * 10 ** -12
        self.re = float(parametrs.parametrs_tranzitions(number_tr)[11])
        self.rkan = float(parametrs.parametrs_tranzitions(number_tr)[12])
        self.Li = float(parametrs.parametrs_tranzitions(number_tr)[15]) * 10 ** -9

        self.ic1 = formul.Ic1(teta=teta, Ec=float(uip), Ec0=self.ec0, rc=rc, ri=ri, Pc1=float(pc1))
        self.uc1 = formul.Uc1gr(teta=teta, Ec=float(uip), Ec0=self.ec0, rc=rc, ri=ri, Ic1=self.ic1)
        self.rek = formul.Rek(Uc1gr=self.uc1, Ic1=self.ic1)
        self.ic0 = formul.Ic0(teta=teta, Ic1=self.ic1)
        self.p0 = formul.P0(Ec=float(uip), Ic0=self.ic0)
        self.q0 = formul.Q0(teta=teta, Ic0=self.ic0, ft=self.ft, Csk=self.csk, Czk=self.czk, Eots=e_ots, Ec=float(uip),
                            rc=rc, ri=ri)
        self.q1 = formul.Q1(Czk=self.czk, ft=self.ft, teta=teta, Eots=e_ots, Ic1=self.ic1, Csk=self.csk, Uc1=self.uc1)
        self.czk1 = formul.Czk1(Czk=self.czk, Q0=self.q0)
        self.csz1 = formul.Csz1(Csz=self.csz, Q0=self.q0)
        self.rkan1 = formul.Rkan1(rkan=self.rkan, Q0=self.q0, Q1=self.q1, Ic1=self.ic1, teta=teta, ft=self.ft)
        self.alfa = formul.alfa(ft=self.ft, teta=teta, Csk=self.csk, Rek=self.rek)
        self.beta = formul.beta(ft=self.ft, teta=teta, Csz1=self.csz1, rkan1=self.rkan1, alfa=self.alfa)
        self.c0 = formul.C0(Csz1=self.csz1, Csk=self.csk, Czk1=self.czk1)
        self.ksi = formul.ksi(Csz1=self.csz1, Czk1=self.czk1, ft=self.ft, teta=teta, C0=self.c0, Rek=self.rek)
        self.roc = formul.roc(ft=self.ft, teta=teta, Li=self.Li, ksi=self.ksi, beta=self.beta, Rek=self.rek, ri=ri,
                              rc=rc)
        self.pn = formul.Pn(Ic1=self.ic1, Rek=self.rek, rc=rc, ri=ri, roc=self.roc, f=float(f) * 10 ** 9, ft=self.ft,
                            teta=teta)
        self.rn = formul.Rn(Rek=self.rek, ri=ri, rc=rc, roc=self.roc, f=float(f) * 10 ** 9, ft=self.ft, teta=teta,
                            ksi=self.ksi, beta=self.beta)
        self.xn = formul.Xn(Rek=self.rek, ri=ri, f=float(f) * 10 ** 9, ft=self.ft, teta=teta, ksi=self.ksi,
                            beta=self.beta, Li=self.Li)
        self.lvh = formul.Lvh(Li=self.Li, ksi=self.ksi)
        self.cvh = formul.Cvh(Czk1=self.czk1, ksi=self.ksi, alfa=self.alfa, ft=self.ft, teta=teta, ri=ri)
        self.rvh = formul.Rvh(re=self.re, ri=ri, rkan1=self.rkan1, ft=self.ft, teta=teta, alfa=self.alfa, ksi=self.ksi,
                              Li=self.Li)
        self.xvh = formul.Xvh(f=float(f) * 10 ** 9, Lvh=self.lvh, Cvh=self.cvh)
        self.ivh = formul.Ivh(ksi=self.ksi, f=float(f) * 10 ** 9, ft=self.ft, teta=teta, Ic1=self.ic1)
        self.pvh = formul.Pvh(Ivh=self.ivh, rvh=self.rvh)
        self.ku = formul.KU(Pn=self.pn, Pvh=self.pvh)
        self.kpd = formul.KPD(Pn=self.pn, Pvh=self.pvh, P0=self.p0)
        self.pras = formul.Pras(Pn=self.pn, Pvh=self.pvh, P0=self.p0)
        self.ez = formul.Ez(Eots=e_ots, Ic1=self.ic1, teta=teta, ft=self.ft, Czk=self.czk)
        self.ez_max = formul.Ezmax(Ez=self.ez, Ic1=self.ic1, ft=self.ft, teta=teta, Czk=self.czk)

        self.n = 3
        self.param_dict = {'Мощность стока': [float(pc1), 'Вт'],
                           'Амплитуда первой гармоники тока стока': [round(self.ic1 * 10 ** 3, self.n), 'мА'],
                           'Первая гормоника напряжения на стоке': [round(self.uc1, self.n), 'В'],
                           'Эквивалентное сопротивление': [round(self.rek, self.n), 'Ом'],
                           'Постоянная сосотовляющая тока на стоке': [round(self.ic0 * 10 ** 3, self.n), 'мА'],
                           'Потребляемая мощность от источника питания': [round(self.p0, self.n), 'Вт'],
                           'Q': [round(self.q0, self.n), ''],
                           'Усредненная по средней гармонике Сзк1 и Ссз1': [
                               f"{round(self.czk1 * 10 ** 12, self.n)} и {round(self.csz1 * 10 ** 12, self.n)}", 'пФ'],
                           'Сопротивление канала по первой гармонике': [round(self.rkan1, self.n), 'Ом'],
                           'Сопротивление обратной связи': [round(self.roc, self.n), 'Ом'],
                           'Выходная мощность': [round(self.pn, self.n), 'Вт'],
                           'Сопротивление нагрузки': [self.rezist_vh(), 'Ом'],
                           'Входная индуктивность': [round(self.lvh * 10 ** 9, self.n), 'нГн'],
                           'Входная емкость': [round(self.cvh * 10 ** 12, self.n), 'пФ'],
                           'Входное сопротивлние': [self.rezist_vih(), 'Ом'],
                           'Амплитуда тока на входе криcталла транзистора': [round(self.ivh * 10 ** 3, self.n), 'мА'],
                           'Мощность на входе': [round(self.pvh, self.n), 'Вт'],
                           'Коэффициент усиления': [round(self.ku, self.n), ''],
                           'КПД': [round(self.kpd, self.n), ''],
                           'Рассеиваемая мощность': [round(self.pras, self.n), 'Вт'],
                           'Напряжение смещения на затворе': [round(self.ez, self.n), 'В'],
                           'Максимальное напряжение на затворе': [round(self.ez_max, self.n), 'В']}

        self.param_name = list(self.param_dict)
        self.param_key = list(self.param_dict.values())

        for i in range(len(self.param_name)):
            self.label = QLabel(f"{i + 1}. {self.param_name[i]}: {self.param_key[i][0]} {self.param_key[i][1]}", self)
            self.label.setGeometry(40, i * 30, 700, 100)
            self.label.setFont(QFont('Arial', 12))

    def rezist_vh(self):
        if self.xn >= 0:
            return f"{round(self.rn, self.n)} + j{round(self.xn, self.n)}"
        else:
            return f"{round(self.rn, self.n)} - j{abs(round(self.xn, self.n))}"

    def rezist_vih(self):
        if self.xvh >= 0:
            return f"{round(self.rvh, self.n)} + j{round(self.xvh, self.n)}"
        else:
            return f"{round(self.rvh, self.n)} - j{abs(round(self.xvh, self.n))}"


class TrW(QMainWindow, Ui_MainWindow3):
    def __init__(self):
        super(TrW, self).__init__()
        self.ui = Ui_MainWindow3()
        self.ui.setupUi(self)
        self.load(self.ui.tableWidget, "tranzitions", "T")
        self.ui.pushButton.setText("Выберите транзистор")

        self.ui.pushButton.hide()

        self.ui.tableWidget.clicked.connect(self.handle_item_clicked)

        self.ui.pushButton.clicked.connect(self.click_button)

    def handle_item_clicked(self):
        self.ui.pushButton.show()
        self.value = self.ui.tableWidget.currentRow()
        self.ui.pushButton.setText('Выбрать транзистор: ' + self.ui.tableWidget.item(self.value, 1).text())

    @staticmethod
    def name_tranzition(id_t, name_db="tranzitions", name_table="T"):
        db = sqlite3.connect(f"{name_db}.db")
        cur = db.cursor()
        sqlstr = f"SELECT * FROM {name_table}"
        name_t = cur.execute(sqlstr).fetchall()[0][id_t]
        return name_t

    def click_button(self):
        self.fw = FirstW(number_tr=self.value + 1)
        self.close()
        self.fw.show()

    def load(self, table, name_db, name_table):
        db = sqlite3.connect(f"{name_db}.db")
        cur = db.cursor()
        sqlstr = f"SELECT * FROM {name_table}"
        name_col = [name[0] for name in cur.execute(sqlstr).description]
        data_db = [name for name in cur.execute(sqlstr).fetchall()]
        table.setRowCount(len(data_db))
        table.setColumnCount(len(data_db[0]))
        table.setHorizontalHeaderLabels(name_col)
        for row in range(len(data_db)):
            for column in range(len(data_db[0])):
                item = QTableWidgetItem(str(data_db[row][column]))
                table.setItem(row, column, item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FirstW(number_tr=-1)
    window.show()
    sys.exit(app.exec_())