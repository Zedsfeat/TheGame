import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from UI_Registration import Ui_RegistrationView
from Game import Game


class Registration(QtWidgets.QMainWindow, Ui_RegistrationView):

    def __init__(self):
        super().__init__()
        self.setupUi(self)  

        self.gw = Game()
        self.count = 0

        self.create_button.clicked.connect(self.add_functions)

    def add_functions(self):
    	if self.nickname_line_edit.text() != "":
    		self.gw.nameLabel.setText(f"{self.nickname_line_edit.text()}'s")
    		self.nickname_line_edit.setStyleSheet("border: 2px solid #FFFFFF;border-radius: 15px;background: #FFFFFF;color: rgb(113, 113, 118);")
    		self.create_button.setText("Game created")
    		self.create_button.setStyleSheet("border-radius: 15px;background: #73AD21;border: 2px solid #FFFFFF; color: #FFFFFF")

    		self.count += 1
    		if self.count == 2:
    			self.gw.show()
    			self.gw.nullify()
    			self.count = 0
    			self.create_button.setStyleSheet("border: 2px solid #FFFFFF;border-radius: 15px;background: #FFFFFF;color: rgb(113, 113, 118);")
    			self.create_button.setText("Create game")
    	else:
    		self.nickname_line_edit.setStyleSheet("border: 2px solid #FF0000;border-radius: 15px;background: #FFFFFF;color: rgb(113, 113, 118);")

if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    rw = Registration()
    rw.show()
    sys.exit(app.exec())