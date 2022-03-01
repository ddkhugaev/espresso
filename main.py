import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.add_form = AddEditCoffeeForm()
        self.add_data.clicked.connect(self.add_new_data)
        self.table.doubleClicked.connect(self.change_data)
        self.con = sqlite3.connect('coffee.sqlite')
        self.modified = {}
        self.reload()

    def reload(self):
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

    def add_new_data(self):
        self.add_form.show()
        self.add_form.new_data_btn.setEnabled(True)
        self.add_form.change_data_btn.setEnabled(False)

    def change_data(self):
        row = self.sender().currentRow()
        item_id = self.sender().item(row, 0).text()
        cur = self.con.cursor()
        result = cur.execute(f"SELECT * FROM coffee_list WHERE id = {item_id}").fetchall()
        name = result[0][1]
        roast = int(result[0][2])
        ground = int(result[0][3])
        taste = result[0][4]
        price = int(result[0][5])
        volume = int(result[0][6])
        self.add_form.show()
        self.add_form.new_data_btn.setEnabled(False)
        self.add_form.change_data_btn.setEnabled(True)
        self.add_form.change_data(item_id, name, roast, ground, taste, price, volume)


class AddEditCoffeeForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.new_data_btn.clicked.connect(self.new_data)
        self.change_data_btn.clicked.connect(self.confirm_change)

    def new_data(self):
        cur = form.con.cursor()
        name = self.name_edit.text()
        roast = int(self.roast_edit.text())
        ground = self.ground_edit.currentText()
        if ground == 'Да':
            ground = 1
        else:
            ground = 0
        taste = self.taste_edit.text()
        price = int(self.price_edit.text())
        volume = int(self.volume_edit.text())

        if all([name, roast, taste, price, volume]):
            result = cur.execute("""INSERT INTO coffee_list (name, roast, ground, taste, price, volume)
                                    VALUES (?, ?, ?, ?, ?, ?)""",
                                 (name, roast, ground, taste, price, volume))
            form.con.commit()
            self.close()
        else:
            self.error_text.setText('Не все поля заполнены')
        form.reload()

    def change_data(self, item_id, name, roast, ground, taste, price, volume):
        self.item_id = item_id
        self.name_edit.setText(name)
        self.roast_edit.setValue(roast)
        if ground == 1:
            self.ground_edit.setCurrentIndex(0)
        else:
            self.ground_edit.setCurrentIndex(1)
        self.taste_edit.setText(taste)
        self.price_edit.setValue(price)
        self.volume_edit.setValue(volume)

    def confirm_change(self):
        cur = form.con.cursor()
        name = self.name_edit.text()
        roast = int(self.roast_edit.text())
        ground = self.ground_edit.currentText()
        if ground == 'Да':
            ground = 1
        else:
            ground = 0
        taste = self.taste_edit.text()
        price = int(self.price_edit.text())
        volume = int(self.volume_edit.text())
        cur.execute(f"""UPDATE coffee_list
                        SET name = '{name}',
                            roast = {roast},
                            ground = {ground},
                            taste = '{taste}',
                            price = {price},
                            volume = {volume}
                        WHERE id = {self.item_id}""")
        form.con.commit()
        self.close()
        form.reload()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
