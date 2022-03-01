import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.modified = {}

        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffee_list").fetchall()
        self.table.setRowCount(len(result))
        if result:
            self.table.setColumnCount(len(result[0]))
            self.titles = ['ID', 'Название', 'Обжарка', 'Молотый', 'Вкус', 'Цена', 'Объем']
            self.table.setHorizontalHeaderLabels(self.titles)
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    if j == 3:
                        if val == 1:
                            val = 'Да'
                        else:
                            val = 'Нет'
                    self.table.setItem(i, j, QTableWidgetItem(str(val)))
            self.modified = {}


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
