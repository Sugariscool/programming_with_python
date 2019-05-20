"""
Visual Basic课程设计

第一章 基本控件应用
题目1 按揭购房还款计划*
"""
import operator
from functools import reduce

from main_ui import Ui_Dialog as Main_UI
from PyQt5 import QtWidgets,QtCore
from equal_total_ui import Ui_Dialog as Equal_Total_UI
from equal_principal_ui import Ui_Dialog as Equal_Principal_UI

class MainDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        ui = Main_UI()
        ui.setupUi(self)
        self.ui = ui
        self._init_ui()

    def _init_ui(self):
        for i in range(1,30):
            self.ui.cbYears.addItem(str(i))
        self.ui.cbYears.setCurrentIndex(14) # 缺省为15
        self.ui.rbTwo.setChecked(True)
        now = QtCore.QDate.currentDate()

        self.ui.dateStart.setDate(now)

        self.ui.btnExit.clicked.connect(self.close)
        self.ui.btnEqualTotal.clicked.connect(self.calc_equal_total)
        self.ui.btnEqualPrincipal.clicked.connect(self.calc_equal_principal)

    def _calc_equal_total(self,principal,rate,monthes):
        month_rate = rate / 12
        c=(1+month_rate)**monthes
        return (principal*month_rate*c)/(c-1)

    def calc_equal_total(self):
        try:
            gongjijin_principal,shangye_principal, start_month, start_year, principal, years = self._get_params_from_ui()
        except:
            QtWidgets.QMessageBox.warning(self,"警告","请输入合适的贷款额。",QtWidgets.QMessageBox.Close)
            return


        monthes = years * 12
        gongjijin_pay_month = self._calc_equal_total(gongjijin_principal,0.04,monthes)
        shangye_pay_month = self._calc_equal_total(shangye_principal,0.05,monthes)
        pay_month = gongjijin_pay_month + shangye_pay_month
        total_pay = pay_month * monthes

        dialog = QtWidgets.QDialog()
        dialog_ui = Equal_Total_UI()
        dialog_ui.setupUi(dialog)
        dialog_ui.txtEachMonth.setText(f"{pay_month:.2f}")
        dialog_ui.txtTotal.setText(f"{total_pay:.2f}")
        dialog_ui.txtRatio.setText(f"{total_pay/principal*100:.2f}%")
        dialog_ui.pushButton.clicked.connect(dialog.close)
        dialog.show()
        dialog.exec()

    def _get_params_from_ui(self):
        """
        获取用户填写的各项参数
        """
        principal = float(self.ui.txtAmount.text())*10000
        years = int(self.ui.cbYears.currentText())
        if self.ui.rbNone.isChecked():
            num = 0
        elif self.ui.rbOne.isChecked():
            num = 1
        elif self.ui.rbTwo.isChecked():
            num = 2
        elif self.ui.rbThree.isChecked():
            num = 3
        start_year = self.ui.dateStart.date().year()
        start_month = self.ui.dateStart.date().month()
        gongjijin_principal = num * 60000
        gongjijin_principal = min(gongjijin_principal,principal)
        if gongjijin_principal<principal:
            shangye_principal = principal - gongjijin_principal
        else:
            shangye_principal = 0
        return gongjijin_principal,shangye_principal, start_month, start_year, principal, years

    def _calc_equal_principal(self,principal,rate,monthes):
        month_rate = rate / 12
        principal_month = principal / monthes
        pay_month = []
        returned_principal = 0
        for i in range(monthes):
            pay = principal_month + (principal-returned_principal) * month_rate
            returned_principal += principal_month
            pay_month.append(pay)
        return pay_month

    def calc_equal_principal(self):
        try:
            gongjijin_principal, shangye_principal, start_month, start_year, principal, years = self._get_params_from_ui()
        except:
            QtWidgets.QMessageBox.warning(self, "警告", "请输入合适的贷款额。", QtWidgets.QMessageBox.Close)
            return

        monthes = years * 12
        gongjijin_pay_month = self._calc_equal_principal(gongjijin_principal,0.04,monthes)
        shangye_pay_month = self._calc_equal_principal(shangye_principal,0.05,monthes)
        pay_total = 0
        txt_pay_month = ""
        start_date = QtCore.QDate(start_year,start_month,1)
        for i in range(monthes):
            pay_month = gongjijin_pay_month[i]+shangye_pay_month[i]
            new_date = start_date.addMonths(i)
            txt_pay_month += f"{new_date.year()}年{new_date.month():02d}月：{pay_month:.2f}元\n"
            pay_total += pay_month

        def save_pay_month():
            results = QtWidgets.QFileDialog.getSaveFileName(self,"请输入文件名")
            if results is None:
                return
            filename = results[0]
            with open(filename,mode="w",encoding="GBK") as file:
                file.write(txt_pay_month)

        dialog = QtWidgets.QDialog(self)
        dialog_ui = Equal_Principal_UI()
        dialog_ui.setupUi(dialog)
        dialog_ui.txtPayMonth.setPlainText(txt_pay_month)
        dialog_ui.txtPayTotal.setText(f"{pay_total:.2f}")
        dialog_ui.txtPayRatio.setText(f"{pay_total/principal*100:.2f}%")
        dialog_ui.btnSave.clicked.connect(save_pay_month)
        dialog.show()
        dialog.exec()



if __name__ == '__main__':
    app=QtWidgets.QApplication([])
    dialog = MainDialog()
    dialog.show()
    dialog.exec_()






