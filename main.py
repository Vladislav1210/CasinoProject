import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5 import uic

NUMBER = ['1', '2', '3', '4', '5', '6', '7', '7', '8', '9', '0']
SLOTS_TYPES = ['']


class Start_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Casino_project.ui', self)
        self.setFixedSize(651, 761)
        self.pict1.setPixmap(QPixmap('online-casino-slots.png'))
        self.register_button.clicked.connect(self.register_window)

    def register_window(self):
        self.rw = Register_Window()
        self.setCentralWidget(self.rw)
        self.rw.show()
        self.sw = Start_Window()
        self.sw.setVisible(False)


class Register_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Casino_project2.ui', self)
        self.setFixedSize(651, 761)
        self.pict2.setPixmap(QPixmap('White_Casino_background.png'))
        self.finish_reg.clicked.connect(self.register_finish)

    def register_finish(self):
        self.flag = True

        self.login = self.register_name.text()
        self.password = self.register_password.text()
        self.card = self.register_card_number.text()
        self.card_check = True
        self.card_check2 = True
        self.cvv = self.register_cvv_card.text()
        self.cvv_check = True
        self.cvv_check2 = True

        self.name_error.setText('')
        self.password_error.setText('')
        self.card_error.setText('')
        self.cvv_error.setText('')

        #  Ошибка логина
        f = sqlite3.connect('Casino_database.db')
        cur = f.cursor()
        if len(self.login) <= 3:
            self.name_error.setText('Логин должен содержать 4 или более символа')
            self.flag = False
        elif ' ' in self.login:
            self.name_error.setText('Логин не должен содержать пробелы')
            self.flag = False
        elif self.login in cur.execute("SELECT login from client_data").fetchone():
            self.name_error.setText('Данный логин уже существует')
            self.flag = False
        f.close()

        #  Ошибка пароля
        if len(self.password) < 4:
            self.password_error.setText('Пароль слишком маленький')
            self.flag = False
        elif ' ' in self.password:
            self.password_error.setText('Пароль не должен содержать пробелы')
            self.flag = False

        #  Ошибка карты - не 19 символов
        if len(self.card) != 19:
            self.flag = False
            self.card_error.setText('Номер карты должен содержать 19 символов включая пробелы')

        # Ошибка карты - неправильный порядок символов
        for i in range(len(self.card)):
            if self.card[i] != ' ' and (i + 1) % 5 == 0:
                self.flag = False
                self.card_check = False
                break
            if self.card[i] not in NUMBER and (i + 1) % 5 != 0:
                self.flag = False
                self.card_check = False
                break
        if self.card_check is False and self.card_check2:
            self.card_error.setText('Номер карты должен содержать только цифры и пробелы в нужных местах')

        #  ошибка cvv - не 3 символа
        if len(self.cvv) != 3:
            self.cvv_check2 = False
            self.flag = False
            self.cvv_error.setText('CVV карты должен сожержать ровно 3 цифры')
        #  онибка cvv - присутствие не цифр
        for i in self.cvv:
            if i not in NUMBER:
                self.flag = False
                self.cvv_check = False
        if self.cvv_check is False and self.cvv_check2:
            self.cvv_error.setText('CVV карты должен содержать только цифры')
        if self.flag:
            f = sqlite3.connect('Casino_database.db')
            cur = f.cursor()
            cur.execute(f"""INSERT INTO client_data(login,password,balance) VALUES('{self.login}', '{self.password}', 
            {0})""")
            f.commit()
            f.close()
            self.mw = Main_Window(self, self.login, 0)
            self.setCentralWidget(self.mw)
            self.mw.show()
            self.rw = Register_Window()
            self.rw.setVisible(False)


class Main_Window(QMainWindow):
    def __init__(self, *arg):
        super().__init__()
        self.login = arg[1]
        self.balance = arg[2]
        uic.loadUi('Casino_project4.ui', self)
        self.setFixedSize(651, 761)
        self.pict4.setPixmap(QPixmap('Casino_patern.png'))
        self.login_label.setText(self.login)
        self.balance_label.setText(f'Ваш баланс: {self.balance}')




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Start_Window()
    ex.show()
    sys.exit(app.exec())

