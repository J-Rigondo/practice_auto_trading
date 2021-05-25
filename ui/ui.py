from PyQt5.QtWidgets import *
from kiwoom.kiwoom import *
import sys


class UiClass:
    def __init__(self):
        print('ui')
        self.app = QApplication(sys.argv)
        self.kiwoom = Kiwoom()

        self.app.exec_()
