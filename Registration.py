import sys
import socket
import threading

from PyQt6 import QtCore, QtGui, QtWidgets
import time

# TODO: отправлять на сервер инфу, что окно закрылось
from PyQt6.QtCore import pyqtSignal, QThread

from UI_Game import Ui_GameWindow
from UI_Registration import Ui_RegistrationView

STARTER = None

class ThreadForFunc(QThread):

    mysignal = QtCore.pyqtSignal(str)

    def __init__(self, parent = None):
        super(ThreadForFunc, self).__init__(parent)

    def run(self):
        while True:
            try:
                message_from_server = client.recv(1024).decode('ascii')
                print(message_from_server)
                if "game_started" in message_from_server:
                    self.mysignal.emit("Start")
                elif "Button" in message_from_server:
                    self.mysignal.emit(message_from_server)
                elif "Restart" in message_from_server:
                    self.mysignal.emit(message_from_server)
                elif "Leave" in message_from_server:
                    self.mysignal.emit("Leave")
                elif "true" in message_from_server:
                    self.mysignal.emit("true")
                elif "false" in message_from_server:
                    self.mysignal.emit("false")
                else:
                    print(1)
            except:
                print("Error!")
                return "error"


class Registration(QtWidgets.QMainWindow, Ui_RegistrationView):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.count = 0

        self.thread = None

        self.create_button.clicked.connect(self.add_functions)


    def add_functions(self):
        if self.nickname_line_edit.text() != "":

            nickname = self.nickname_line_edit.text()
            self.gw = Game(nickname)
            client.send(nickname.encode("ascii"))
            self.gw.nameLabel.setText(f"{nickname}'s")
            self.nickname_line_edit.setStyleSheet("border: 2px solid #FFFFFF;border-radius: 15px;background: #FFFFFF;color: rgb(113, 113, 118);")

            client.send(f"{nickname}:gaming".encode("ascii"))
            self.create_button.setText("Wait for opponent")
            self.create_button.setStyleSheet("width:40px;border-radius: 15px;background: #73AD21;border: 2px solid #FFFFFF; color: #FFFFFF")
            self.create_button.setEnabled(False)

            self.thread = ThreadForFunc()
            self.thread.start()
            self.thread.mysignal.connect(self.handle_signal)

        else:
            self.nickname_line_edit.setStyleSheet("border: 2px solid #FF0000;border-radius: 15px;background: #FFFFFF;color: rgb(113, 113, 118);")

    def handle_signal(self, value:str):
        global buttons_dict

        if value == "Start":
            self.lets_game()
        elif "Button" in value:
            for k, v in self.gw.buttons_dict.items():
                if v == value.split()[0]:
                    self.gw.push_button_to_game(k, value)
                    break
        elif value == "Restart1":
            self.gw.restart_game()
        elif value == "Restart2":
            self.gw.full_restart()
        elif value == "Leave":
            self.gw.leaved()
        elif value == "true":
            self.gw.enable_all()
        elif value == "false":
            self.gw.block_all()


    def lets_game(self):
        self.gw.show()
        self.gw.nullify()
        self.close()

class Game(QtWidgets.QMainWindow, Ui_GameWindow):
    buttons_dict = dict()
    queue_dict = dict()
    queue_array = []
    buttons_array = []
    flag_for_win = True
    flag_for_cell_empty = True

    def __init__(self, nick):
        super().__init__()
        self.setupUi(self)

        self.nickname = nick
        self.my_step = None

        self.count_for_leave = 0
        self.count_for_restart = 0

        self.buttons_array = [
            self.pushButton, self.pushButton_2, self.pushButton_3, self.pushButton_4,
            self.pushButton_5, self.pushButton_7, self.pushButton_6, self.pushButton_8,
            self.pushButton_9, self.pushButton_11, self.pushButton_10, self.pushButton_12,
            self.pushButton_13, self.pushButton_15, self.pushButton_14, self.pushButton_16,
        ]
        count = 0
        for button in self.buttons_array:
            self.queue_dict[button] = ""
            count += 1
            self.buttons_dict[button] = f"Button_{count}"

        self.add_functions()

    def leaved(self):
        self.nullify()
        rw.show()
        self.close()

    def block_all(self):
        for btn in self.buttons_array:
            btn.setEnabled(False)

    def enable_all(self):
        for btn in self.buttons_array:
            btn.setEnabled(True)

    def add_functions(self):
        self.pushButton.clicked.connect(lambda: self.setup_game(self.pushButton))
        self.pushButton_2.clicked.connect(lambda: self.setup_game(self.pushButton_2))
        self.pushButton_3.clicked.connect(lambda: self.setup_game(self.pushButton_3))
        self.pushButton_4.clicked.connect(lambda: self.setup_game(self.pushButton_4))
        self.pushButton_5.clicked.connect(lambda: self.setup_game(self.pushButton_5))
        self.pushButton_6.clicked.connect(lambda: self.setup_game(self.pushButton_6))
        self.pushButton_7.clicked.connect(lambda: self.setup_game(self.pushButton_7))
        self.pushButton_8.clicked.connect(lambda: self.setup_game(self.pushButton_8))
        self.pushButton_9.clicked.connect(lambda: self.setup_game(self.pushButton_9))
        self.pushButton_10.clicked.connect(lambda: self.setup_game(self.pushButton_10))
        self.pushButton_11.clicked.connect(lambda: self.setup_game(self.pushButton_11))
        self.pushButton_12.clicked.connect(lambda: self.setup_game(self.pushButton_12))
        self.pushButton_13.clicked.connect(lambda: self.setup_game(self.pushButton_13))
        self.pushButton_14.clicked.connect(lambda: self.setup_game(self.pushButton_14))
        self.pushButton_15.clicked.connect(lambda: self.setup_game(self.pushButton_15))
        self.pushButton_16.clicked.connect(lambda: self.setup_game(self.pushButton_16))

        self.restart_button.clicked.connect(self.restart_game)
        self.surrender_button.clicked.connect(self.surrender_in_game)


    def surrender_in_game(self):
        self.count_for_leave += 1
        self.surrender_button.setStyleSheet("border-radius: 15px;background: #73AD21;border: 2px solid #FFFFFF; color: #FFFFFF")
        self.surrender_button.setText("Leave?")
        if self.count_for_leave == 2:
            client.send(f"{self.nickname}:leave".encode("ascii"))
            self.moveLabel.setText("conceded")

            if self.nameLabel.text()[-2:] == "'s":
                self.nameLabel.setText(f"{self.nameLabel.text()[0:-2]}")
            else:
                self.nameLabel.setText(f"{self.nameLabel.text()}")
            self.surrender_button.setText("Leave")
            self.surrender_button.setStyleSheet("border: 2px solid #FFFFFF;border-radius: 15px;background: #FFFFFF;color: rgb(113, 113, 118);")
            self.count_for_leave = 0
            self.close()

    def restart_game(self):
        self.count_for_restart += 1
        self.restart_button.setStyleSheet("border-radius: 15px;background: #73AD21;border: 2px solid #FFFFFF; color: #FFFFFF")
        if self.count_for_restart == 1:
            self.restart_button.setText("Restart?")
        if self.count_for_restart == 2:
            client.send("Restart".encode("ascii"))
            self.restart_button.setText("Restart wait")
            self.restart_button.setEnabled(False)


    def full_restart(self):
        self.nullify()
        self.restart_button.setStyleSheet(
            "border: 2px solid #FFFFFF;border-radius: 15px;background: #FFFFFF;color: rgb(113, 113, 118);")
        self.count_for_restart = 0
        for k in self.buttons_dict.keys():
            self.buttons_dict[k] = self.buttons_dict[k].split()[0]


    def setup_game(self, button: QtWidgets.QPushButton):

        if self.nameLabel.text()[-2:] != "'s":
            self.nameLabel.setText(f"{self.nameLabel.text()}'s")

        if len(self.queue_array) != 16:
            if self.queue_dict[button] == "":
                if len(self.queue_array) == 0:
                    button.setStyleSheet("border-radius: 25px;background: rgb(237, 51, 65);border: 2px solid #FFFFFF;")
                    button.setText("X")
                    self.moveLabel.setText("move")
                elif self.queue_array[-1].text() == "X":
                    button.setStyleSheet("border-radius: 25px;background: #73AD21;border: 2px solid #FFFFFF;")
                    button.setText("O")

                    self.moveLabel.setText("move")
                else:
                    button.setStyleSheet("border-radius: 25px;background: rgb(237, 51, 65);border: 2px solid #FFFFFF;")
                    button.setText("X")

                    self.moveLabel.setText("move")

                
                self.buttons_dict[button] = self.buttons_dict[button].split()[0] + " " + button.text()
                self.queue_dict[button] = button.text()
                self.queue_array.append(button)

                client.send(self.buttons_dict[button].encode("ascii"))

                if len(self.queue_array) == 16 and self.flag_for_win:
                    self.nameLabel.setText("Draw")
                    self.moveLabel.setText("")

                else:
                    self.check_win()

            else:
                if self.flag_for_cell_empty:
                    print("Cell is empty")
                else:
                    self.nullify()

    def push_button_to_game(self, button, button_dict_value):
        print("push_to_game", button, button.text(), button_dict_value, self.queue_dict[button])
        if self.queue_dict[button] == "":
            if button_dict_value[-1] == "X":
                button.setStyleSheet("border-radius: 25px;background: rgb(237, 51, 65);border: 2px solid #FFFFFF;")
                button.setText("X")
                self.moveLabel.setText("move")
            elif button_dict_value[-1] == "O":
                button.setStyleSheet("border-radius: 25px;background: #73AD21;border: 2px solid #FFFFFF;")
                button.setText("O")
                self.moveLabel.setText("move")

            self.queue_dict[button] = button.text()
            self.queue_array.append(button)

    def check_win(self):
        global flag_for_win
        global flag_for_cell_empty

        if self.flag_for_win:
            if self.queue_dict[self.pushButton] + self.queue_dict[self.pushButton_2] + self.queue_dict[self.pushButton_3] + self.queue_dict[self.pushButton_4] == "XXXX" \
                    or self.queue_dict[self.pushButton_5] + self.queue_dict[self.pushButton_7] + self.queue_dict[self.pushButton_6] + self.queue_dict[self.pushButton_8] == "XXXX" \
                    or  self.queue_dict[self.pushButton_9] + self.queue_dict[self.pushButton_11] + self.queue_dict[self.pushButton_10] + self.queue_dict[self.pushButton_12] == "XXXX" \
                    or self.queue_dict[self.pushButton_13] + self.queue_dict[self.pushButton_15] + self.queue_dict[self.pushButton_14] + self.queue_dict[self.pushButton_16] == "XXXX" \
                    or self.queue_dict[self.pushButton] + self.queue_dict[self.pushButton_5] + self.queue_dict[self.pushButton_9] + self.queue_dict[self.pushButton_13] == "XXXX" \
                    or  self.queue_dict[self.pushButton_2] + self.queue_dict[self.pushButton_7] + self.queue_dict[self.pushButton_11] + self.queue_dict[self.pushButton_15] == "XXXX" \
                    or  self.queue_dict[self.pushButton_3] + self.queue_dict[self.pushButton_6] + self.queue_dict[self.pushButton_10] + self.queue_dict[self.pushButton_14] == "XXXX" \
                    or  self.queue_dict[self.pushButton_4] + self.queue_dict[self.pushButton_8] + self.queue_dict[self.pushButton_12] + self.queue_dict[self.pushButton_16] == "XXXX" \
                    or  self.queue_dict[self.pushButton] + self.queue_dict[self.pushButton_7] + self.queue_dict[self.pushButton_10] + self.queue_dict[self.pushButton_16] == "XXXX" \
                    or  self.queue_dict[self.pushButton_13] + self.queue_dict[self.pushButton_11] + self.queue_dict[self.pushButton_6] + self.queue_dict[self.pushButton_4] == "XXXX":
                self.nameLabel.setText(f"{self.nameLabel.text()[0:-2]}")
                self.moveLabel.setText("wins 🥳")
                self.flag_for_win = False
                self.flag_for_cell_empty = False
            elif self.queue_dict[self.pushButton] + self.queue_dict[self.pushButton_2] + self.queue_dict[self.pushButton_3] + self.queue_dict[self.pushButton_4] == "OOOO" \
                    or self.queue_dict[self.pushButton_5] + self.queue_dict[self.pushButton_7] + self.queue_dict[self.pushButton_6] + self.queue_dict[self.pushButton_8] == "OOOO" \
                    or  self.queue_dict[self.pushButton_9] + self.queue_dict[self.pushButton_11] + self.queue_dict[self.pushButton_10] + self.queue_dict[self.pushButton_12] == "OOOO" \
                    or self.queue_dict[self.pushButton_13] + self.queue_dict[self.pushButton_15] + self.queue_dict[self.pushButton_14] + self.queue_dict[self.pushButton_16] == "OOOO" \
                    or self.queue_dict[self.pushButton] + self.queue_dict[self.pushButton_5] + self.queue_dict[self.pushButton_9] + self.queue_dict[self.pushButton_13] == "OOOO" \
                    or  self.queue_dict[self.pushButton_2] + self.queue_dict[self.pushButton_7] + self.queue_dict[self.pushButton_11] + self.queue_dict[self.pushButton_15] == "OOOO" \
                    or  self.queue_dict[self.pushButton_3] + self.queue_dict[self.pushButton_6] + self.queue_dict[self.pushButton_10] + self.queue_dict[self.pushButton_14] == "OOOO" \
                    or  self.queue_dict[self.pushButton_4] + self.queue_dict[self.pushButton_8] + self.queue_dict[self.pushButton_12] + self.queue_dict[self.pushButton_16] == "OOOO" \
                    or  self.queue_dict[self.pushButton] + self.queue_dict[self.pushButton_7] + self.queue_dict[self.pushButton_10] + self.queue_dict[self.pushButton_16] == "OOOO" \
                    or  self.queue_dict[self.pushButton_13] + self.queue_dict[self.pushButton_11] + self.queue_dict[self.pushButton_6] + self.queue_dict[self.pushButton_4] == "OOOO":
                self.nameLabel.setText(f"{self.nameLabel.text()[0:-2]}")
                self.moveLabel.setText("wins 🥳")
                self.flag_for_win = False
                self.flag_for_cell_empty = False
        else:
            self.nullify()


    def nullify(self):

        self.flag_for_win = True
        self.flag_for_cell_empty = True
        self.count_for_leave = 0
        self.count_for_restart = 0

        self.surrender_button.setText("Leave")
        self.restart_button.setEnabled(True)
        self.surrender_button.setStyleSheet("border: 2px solid #FFFFFF;border-radius: 15px;background: #FFFFFF;color: rgb(113, 113, 118);")
        self.restart_button.setText("Restart")
        self.restart_button.setEnabled(True)
        self.restart_button.setStyleSheet("border: 2px solid #FFFFFF;border-radius: 15px;background: #FFFFFF;color: rgb(113, 113, 118);")

        for button in self.queue_array:
            button.setStyleSheet("border-radius: 25px;""background: #FFFFFF;""border: 2px solid #FFFFFF;")

        for button in self.queue_dict.keys():
            self.queue_dict[button] = ""

        self.queue_array.clear()
        if self.nameLabel.text()[-2:] == "'s":
            self.nameLabel.setText(f"{self.nameLabel.text()}")
        else:
            self.nameLabel.setText(f"{self.nameLabel.text()}'s")
        self.nameLabel.setStyleSheet("color: #FFFFFF")
        self.moveLabel.setText("move")

        for k in self.buttons_dict.keys():
            self.buttons_dict[k] = self.buttons_dict[k].split()[0]

if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5063))
    app = QtWidgets.QApplication(sys.argv)
    rw = Registration()
    rw.show()
    sys.exit(app.exec())