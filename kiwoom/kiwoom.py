from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from config.error_code import *


class Kiwoom(QAxWidget):
    def __init__(self):
        print('kiwoom')
        super().__init__()

        self.get_ocx_instance()
        self.account_num = None

        #EventLoop
        self.login_event_loop = QEventLoop()
        self.detail_account_info_loop = QEventLoop()
        self.detail_account_mystock_loop = QEventLoop()

        self.event_slots()
        self.signal_login_commConnect()
        self.get_account_info()
        self.detail_account_info()
        self.detail_account_mystock()

    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1") #응용프로그램 제어

    def event_slots(self):
        self.OnEventConnect.connect(self.login_slot) #콜백으로 넘기기고 다시 안 돌아옴
        self.OnReceiveTrData.connect(self.trdata_slot)

    def login_slot(self, error_code):
        error = errors(error_code)
        print(f'error code:{error}')
        self.login_event_loop.exit()

    def signal_login_commConnect(self):
        self.dynamicCall('CommConnect()')
        self.login_event_loop.exec_()

    def get_account_info(self):
        account_list = self.dynamicCall('GetLoginInfo(String)', 'ACCNO')
        self.account_num = account_list.split(';')[0]

        print(f'my account: {self.account_num}')

    def detail_account_info(self):
        self.dynamicCall('SetInputValue(String, String)', '계좌번호', self.account_num)
        self.dynamicCall('SetInputValue(String, String)', '비밀번호', )
        self.dynamicCall('SetInputValue(String, String)', '비밀번호입력매체구분', '00')
        self.dynamicCall('SetInputValue(String, String)', '조회구분', '2')
        self.dynamicCall('CommRqData(String, String, int, String)', '예수금상세현황요청', 'opw00001', '0', '2000')
        self.detail_account_info_loop.exec_()

    def detail_account_mystock(self, sPrevNext = '0'):
        self.dynamicCall('SetInputValue(String, String)', '계좌번호', self.account_num)
        self.dynamicCall('SetInputValue(String, String)', '비밀번호', )
        self.dynamicCall('SetInputValue(String, String)', '비밀번호입력매체구분', '00')
        self.dynamicCall('SetInputValue(String, String)', '조회구분', '2')
        self.dynamicCall('CommRqData(String, String, int, String)', '계좌평가잔고내역요청', 'opw00018', '0', '2000')
        self.detail_account_mystock_loop.exec_()

    def trdata_slot(self, sScrNo, sRQName, sTrCode, sRecordName,  sPrevNext):
        """
        :param sScrNo: 화면번호
        :param sRQName: 사용자 구분명 - 요청할 때 정한 이름
        :param sTrCode: TR코드
        :param sRecordName: 레코드 이름
        :param sPrevNext: 연속조회 유무를 판단하는 값 0: 연속(추가조회)데이터 없음, 2:연속
        :return:
        """

        if sRQName == '예수금상세현황요청':
            deposit = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, 0, '예수금')
            deposit = int(deposit)
            print(f'deposit: {deposit}')

            possible_withdraw = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, 0, '출금가능금액')
            possible_withdraw = int(possible_withdraw)
            print(f'possible withdraw:{possible_withdraw}')
            self.detail_account_info_loop.exit()

        if sRQName == '계좌평가잔고내역요청':
            total_buy_money = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, 0, '총매입금액')
            total_buy_money = int(total_buy_money)
            print(f'total buy money:{total_buy_money}')

            total_profit_rate = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, 0, '총매입금액')
            total_profit_rate = float(total_profit_rate)
            print(f'total profit rate:{total_profit_rate}')
            self.detail_account_mystock_loop.exit()
