import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from UI_Game import Ui_GameWindow


class Game(QtWidgets.QMainWindow, Ui_GameWindow):

    queue_dict = dict()
    queue_array = []
    buttons_array = []
    flag_for_win = True
    flag_for_cell_empty = True

    def __init__(self, client):
        super().__init__()
        self.setupUi(self)

        self.client = client
        print(self.client.__hash__())
        self.client.send("Test".encode("ascii"))

        self.count_for_leave = 0
        self.count_for_restart = 0

        self.buttons_array = [
            self.pushButton, self.pushButton_2, self.pushButton_3, self.pushButton_4,
            self.pushButton_5, self.pushButton_7, self.pushButton_6, self.pushButton_8,
            self.pushButton_9, self.pushButton_11, self.pushButton_10, self.pushButton_12,
            self.pushButton_13, self.pushButton_15, self.pushButton_14, self.pushButton_16,
        ]

        for button in self.buttons_array:
            self.queue_dict[button] = ""

        self.add_functions()

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
        self.surrender_button.setText("Sure?")
        if self.count_for_leave == 2:
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
        self.restart_button.setText("Sure?")
        if self.count_for_restart == 2:
            self.nullify()
            self.restart_button.setText("Restart")
            self.restart_button.setStyleSheet("border: 2px solid #FFFFFF;border-radius: 15px;background: #FFFFFF;color: rgb(113, 113, 118);")
            self.count_for_restart = 0


    def setup_game(self, button: QtWidgets.QPushButton):
        global queue_dict
        global queue_array
        global buttons_array
        global flag_for_cell_empty

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

                self.queue_dict[button] = button.text()
                self.queue_array.append(button)

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
        global queue_array
        global queue_dict
        global flag_for_win
        global flag_for_cell_empty

        self.flag_for_win = True
        self.flag_for_cell_empty = True
        self.count_for_leave = 0
        self.count_for_restart = 0

        self.surrender_button.setText("Leave")
        self.surrender_button.setStyleSheet("border: 2px solid #FFFFFF;border-radius: 15px;background: #FFFFFF;color: rgb(113, 113, 118);")
        self.restart_button.setText("Restart")
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


# if __name__ == "__main__":

#     app = QtWidgets.QApplication(sys.argv)
#     gw = Game()
#     gw.show()
#     sys.exit(app.exec())