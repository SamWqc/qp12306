from PyQt5.Qt import *
from ui.ui12306 import Ui_Dialog
from API.API_TOOL import APITool

class download_yzm_thread(QThread):
    get_yzm_url_signal = pyqtSignal(str)
    def run(self):
        url = APITool.download_check()
        self.get_yzm_url_signal.emit(url)





class login_window(QWidget,Ui_Dialog):

    success_login = pyqtSignal(str)


    def __init__(self,parent=None,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.setupUi(self)
        self.refresh_yzm()


    def refresh_yzm(self):
        print('刷新验证码')
        thread=download_yzm_thread(self)
        def parse_yzm_url(url):
            url = 'D:/qp/' + url
            check_pixmap = QPixmap(url)
            self.yzm_label.setPixmap(check_pixmap)
            self.yzm_label.clear_points()
        thread.get_yzm_url_signal.connect(parse_yzm_url)
        thread.start()
        print('继续主线程')


    def auto_yz(self):
        print('自动验证')
        print('此功能未开启，请手动输入验证码')

    def login(self):
        yzm=self.yzm_label.get_result()
        print(yzm)
        if APITool.check_yzm(yzm):
            account=self.account.text()
            pwd=self.pwd.text()
            login_result=APITool.login_check(account,pwd)
            login_code = login_result[0]
            hello=login_result[1]

            self.success_login.emit(hello)
            if login_code!=0:
                print('密码错误或用户名有误')
                self.refresh_yzm()
        else:
            print('验证码错误')
            self.refresh_yzm()

    def account_enable(self):
        account=self.account.text()
        pwd=self.pwd.text()
        if len(account)==0 or len(pwd)==0:
            self.login_check.setEnabled(False)
        else:
            self.login_check.setEnabled(True)

















if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    login=login_window()

    login.show()


    sys.exit(app.exec_())