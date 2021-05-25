from PyQt5.QAxContainer import *
from PyQt5.QtCore import *


class Kiwoom(QAxWidget):
    def __init__(self):
        print('kiwoom')
        super().__init__()
        self.get_ocx_instance()
        self.login_event_loop = QEventLoop()
        self.event_slots()
        self.signal_login_commConnect()

    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1") #응용프로그램 제어

    def event_slots(self):
        self.OnEventConnect.connect(self.login_slot)
        self.login_event_loop.exit()

    def login_slot(self, errorCode):
        print(f'errorCode:{errorCode}')

    def signal_login_commConnect(self):
        self.dynamicCall('CommConnect()')
        self.login_event_loop.exec_()