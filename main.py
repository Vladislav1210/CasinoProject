import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from random import choice

NUMBER = ['1', '2', '3', '4', '5', '6', '7', '7', '8', '9', '0']  # цифирки

SLOTS_TYPES = ['7', '7', '7', 'bar', 'bar', 'bar', 'bar', 'bar',  # 8
               'b', 'b', 'b', 'b', 'b', 'b', 'g', 'g', 'g', 'g', 'g', 'g', 'g',  # 13
               'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'c', 'c', 'c',  # 11
               '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']  # 18
# 32/50 удачных слотов


TROLL_PHRASES = ['Сегодня не твой день', 'Неудачник', 'Деньги - прощайте',
                 'Банкротство - здравствуй', 'На улице тоже есть чем питаться',
                 'Может в другой раз повезёт', 'Терпи', 'Неповезло(',
                 'Ещё одна неудача', 'Какой же позор!']  # при проигрыше

VICTORY_PHRASES = ['И у нас победитель!', 'Мне кажется ты жульничал',
                   'Кто бы мог поверить?!', 'Jackpot!!!', 'Судьба тебя одарила']  # при выйгрыше

SLOT_PICTURE = {'c': 'Cherry_slot.png', '7': 'Seven_slot.png', 'bar': 'Bar_slot.png', 'b': 'bell_slot.png',
                'g': 'Grape_slot.png', 'l': 'Lemon_slot.png', '.': 'Empty_slot.png'}


class Start_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Casino_project.ui', self)
        self.setFixedSize(651, 761)
        self.pict1.setPixmap(QPixmap('online-casino-slots.png'))
        self.register_button.clicked.connect(self.register_window)
        self.enter_button.clicked.connect(self.enter_window)

    def register_window(self):
        self.rw = Register_Window()
        self.setCentralWidget(self.rw)
        self.rw.show()
        self.sw = Start_Window()
        self.sw.setVisible(False)

    def enter_window(self):
        self.ew = Enter_Window()
        self.setCentralWidget(self.ew)
        self.ew.show()
        self.sw = Start_Window()
        self.sw.setVisible(False)


class Register_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Casino_project2.ui', self)
        self.setFixedSize(651, 761)
        self.pict2.setPixmap(QPixmap('Casino_background.png'))
        self.finish_reg.clicked.connect(self.register_finish)

    def register_finish(self):
        self.flag = True

        self.login = self.register_name.text()
        self.login_error = False
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
        for i in cur.execute("SELECT login from client_data").fetchall():
            if self.login in i:
                self.login_error = True
                break
        if len(self.login) <= 3:
            self.name_error.setText('Логин должен содержать 4 или более символа')
            self.flag = False
        elif ' ' in self.login:
            self.name_error.setText('Логин не должен содержать пробелы')
            self.flag = False
        elif self.login_error:
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


class Enter_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Casino_project3.ui', self)
        self.setFixedSize(651, 761)
        self.pict3.setPixmap(QPixmap('Casino_background.png'))

        self.finish_ent.clicked.connect(self.enter_finish)

    def enter_finish(self):
        self.flag = True
        self.login_check = True

        self.login = self.enter_name.text()
        self.password = self.enter_password.text()

        self.name_error.setText('')
        self.password_error.setText('')

        f = sqlite3.connect('Casino_database.db')
        cur = f.cursor()
        # ошибка логина
        for i in cur.execute("SELECT login from client_data").fetchall():
            if self.login in i:
                self.login_check = False
                break
        if self.login_check:
            self.flag = False
            self.name_error.setText('Такого логина не существует')
        # ошибка пароля
        elif self.password != ''.join(cur.execute(f"""SELECT password from client_data 
        WHERE login = '{self.login}'""").fetchone()):
            self.flag = False
            self.password_error.setText('Неверный пароль')
        f.close()
        if self.flag:
            f = sqlite3.connect('Casino_database.db')
            cur = f.cursor()
            balance = cur.execute(f"""SELECT balance from client_data 
                    WHERE login = '{self.login}'""").fetchone()
            self.mw = Main_Window(self, self.login, int(*balance))
            self.setCentralWidget(self.mw)
            self.mw.show()
            self.ew = Enter_Window()
            self.ew.setVisible(False)



class Main_Window(QMainWindow):
    def __init__(self, *arg):
        super().__init__()
        self.login = arg[1]
        self.balance = arg[2]  # должно быть всегда int
        uic.loadUi('Casino_project4.ui', self)
        self.setFixedSize(651, 761)
        self.pict4.setPixmap(QPixmap('Casino_patern.png'))

        self.login_label.setText(self.login)
        self.balance_label.setText(f'Ваш баланс: {self.balance}')
        self.spin_error.setText('')
        self.troll_label.setText('')
        self.info_label.setText('')
        self.slot1.setPixmap(QPixmap(SLOT_PICTURE['.']))
        self.slot2.setPixmap(QPixmap(SLOT_PICTURE['.']))
        self.slot3.setPixmap(QPixmap(SLOT_PICTURE['.']))

        self.replenish_button.clicked.connect(self.replenish_method)  # Пополнить
        self.withdraw_button.clicked.connect(self.withdraw_method)  # Снять
        self.spin_button.clicked.connect(self.spin)  # spin
        self.exit_button.clicked.connect(self.exit)  # выйти

    def replenish_method(self):
        value, ok_pressed = QInputDialog.getInt(self, 'Пополнение',
                                                'Введите пополняемую сумму', 100, 100, 1000000, 100)
        if ok_pressed:
            f = sqlite3.connect('Casino_database.db')
            cur = f.cursor()
            cur.execute(f"""UPDATE client_data SET balance = balance + {str(value)} WHERE login = '{self.login}'""")
            f.commit()
            self.balance = int(*cur.execute(f"""SELECT balance from client_data 
            where login = '{self.login}'""").fetchone())
            f.close()
            self.balance_label.setText(f'Ваш баланс: {self.balance}')

    def withdraw_method(self):
        f = sqlite3.connect('Casino_database.db')
        cur = f.cursor()
        value, ok_pressed = QInputDialog.getInt(self, 'Снятие', 'Введите снимаемую сумму', 0, 0,
                                                int(*cur.execute(f"""SELECT balance from client_data WHERE login = 
                                                '{self.login}'""").fetchone()), 100)
        if ok_pressed:
            cur.execute(f"""UPDATE client_data SET balance = balance - {str(value)} WHERE login = '{self.login}'""")
            f.commit()
            self.balance = int(*cur.execute(f"""SELECT balance from client_data 
                        where login = '{self.login}'""").fetchone())
            self.balance_label.setText(f'Ваш баланс: {self.balance}')
        f.close()

    def exit(self):
        self.sw = Start_Window()
        self.setCentralWidget(self.sw)
        self.sw.show()
        self.mw = Main_Window(self, None, None)
        self.mw.setVisible(False)

    def spin(self):
        f = sqlite3.connect('Casino_database.db')
        self.spin_error.setText('')
        cur = f.cursor()
        sl1 = choice(SLOTS_TYPES)
        sl2 = choice(SLOTS_TYPES)
        sl3 = choice(SLOTS_TYPES)
        bet = int(self.bet_combobox.currentText())
        # ошибка в случае если ставка превышает баланс
        if bet > self.balance:
            self.spin_error.setText('Не хватает средств')
            self.troll_label.setText('')
            self.info_label.setText('')
            self.slot1.setPixmap(QPixmap(SLOT_PICTURE['.']))
            self.slot2.setPixmap(QPixmap(SLOT_PICTURE['.']))
            self.slot3.setPixmap(QPixmap(SLOT_PICTURE['.']))
            return None
        cherry_count = 0
        for i in (sl1, sl2, sl3):
            if i == 'c':
                cherry_count += 1

        # 7 wins
        if sl1 == sl2 == sl3 == '7':
            result = bet * 1000
            cur.execute(f"""UPDATE client_data SET balance = balance + {str(result)} - {str(bet)} 
            WHERE login = '{self.login}'""")
            f.commit()
            self.balance = int(*cur.execute(f"""SELECT balance from client_data 
                                    where login = '{self.login}'""").fetchone())
            self.balance_label.setText(f'Ваш баланс: {self.balance}')
            self.troll_label.setText(choice(VICTORY_PHRASES))
            self.info_label.setText(f'Вы выйграли: {result}')
        # bar wins
        elif sl1 == sl2 == sl3 == 'bar':
            result = bet * 300
            cur.execute(f"""UPDATE client_data SET balance = balance + {str(result)} - {str(bet)} 
            WHERE login = '{self.login}'""")
            f.commit()
            self.balance = int(*cur.execute(f"""SELECT balance from client_data 
                                    where login = '{self.login}'""").fetchone())
            self.balance_label.setText(f'Ваш баланс: {self.balance}')
            self.troll_label.setText(choice(VICTORY_PHRASES))
            self.info_label.setText(f'Вы выйграли: {result}')
        # bell wins
        elif sl1 == sl2 == sl3 == 'b':
            result = bet * 80
            cur.execute(f"""UPDATE client_data SET balance = balance + {str(result)} - {str(bet)} 
            WHERE login = '{self.login}'""")
            f.commit()
            self.balance = int(*cur.execute(f"""SELECT balance from client_data 
                                    where login = '{self.login}'""").fetchone())
            self.balance_label.setText(f'Ваш баланс: {self.balance}')
            self.troll_label.setText(choice(VICTORY_PHRASES))
            self.info_label.setText(f'Вы выйграли: {result}')
        # grape wins
        elif sl1 == sl2 == sl3 == 'g':
            result = bet * 50
            cur.execute(f"""UPDATE client_data SET balance = balance + {str(result)} - {str(bet)} 
            WHERE login = '{self.login}'""")
            f.commit()
            self.balance = int(*cur.execute(f"""SELECT balance from client_data 
                                    where login = '{self.login}'""").fetchone())
            self.balance_label.setText(f'Ваш баланс: {self.balance}')
            self.troll_label.setText(choice(VICTORY_PHRASES))
            self.info_label.setText(f'Вы выйграли: {result}')
        # lemon wins
        elif sl1 == sl2 == sl3 == 'l':
            result = bet * 25
            cur.execute(f"""UPDATE client_data SET balance = balance + {str(result)} - {str(bet)} 
            WHERE login = '{self.login}'""")
            f.commit()
            self.balance = int(*cur.execute(f"""SELECT balance from client_data 
                                    where login = '{self.login}'""").fetchone())
            self.balance_label.setText(f'Ваш баланс: {self.balance}')
            self.troll_label.setText(choice(VICTORY_PHRASES))
            self.info_label.setText(f'Вы выйграли: {result}')
        # cherry3 wins
        elif cherry_count == 3:
            result = bet * 100
            cur.execute(f"""UPDATE client_data SET balance = balance + {str(result)} - {str(bet)} 
            WHERE login = '{self.login}'""")
            f.commit()
            self.balance = int(*cur.execute(f"""SELECT balance from client_data 
                                    where login = '{self.login}'""").fetchone())
            self.balance_label.setText(f'Ваш баланс: {self.balance}')
            self.troll_label.setText(choice(VICTORY_PHRASES))
            self.info_label.setText(f'Вы выйграли: {result}')
        # cherry2 wins
        elif cherry_count == 2:
            result = bet * 25
            cur.execute(f"""UPDATE client_data SET balance = balance + {str(result)} - {str(bet)} 
            WHERE login = '{self.login}'""")
            f.commit()
            self.balance = int(*cur.execute(f"""SELECT balance from client_data 
                                    where login = '{self.login}'""").fetchone())
            self.balance_label.setText(f'Ваш баланс: {self.balance}')
            self.troll_label.setText(choice(VICTORY_PHRASES))
            self.info_label.setText(f'Вы выйграли: {result}')
        # cherry1 wins
        elif cherry_count == 1:
            result = bet * 2
            cur.execute(f"""UPDATE client_data SET balance = balance + {str(result)} - {str(bet)} 
            WHERE login = '{self.login}'""")
            f.commit()
            self.balance = int(*cur.execute(f"""SELECT balance from client_data 
                                    where login = '{self.login}'""").fetchone())
            self.balance_label.setText(f'Ваш баланс: {self.balance}')
            self.troll_label.setText(choice(VICTORY_PHRASES))
            self.info_label.setText(f'Вы выйграли: {result}')
        else:
            cur.execute(f"""UPDATE client_data SET balance = balance - {str(bet)} 
                        WHERE login = '{self.login}'""")
            f.commit()
            self.balance = int(*cur.execute(f"""SELECT balance from client_data 
                                                where login = '{self.login}'""").fetchone())
            self.balance_label.setText(f'Ваш баланс: {self.balance}')
            self.troll_label.setText(choice(TROLL_PHRASES))
            self.info_label.setText(f'Вы проиграли')
        self.slot1.setPixmap(QPixmap(SLOT_PICTURE[sl1]))
        self.slot2.setPixmap(QPixmap(SLOT_PICTURE[sl2]))
        self.slot3.setPixmap(QPixmap(SLOT_PICTURE[sl3]))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Start_Window()
    ex.show()
    sys.exit(app.exec())

