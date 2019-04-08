from PyQt5.Qt import *
from ui.book_win import Ui_Form

class BookPane(QWidget,Ui_Form):
    confirm_signal = pyqtSignal(dict)
    def __init__(self,parent=None,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.setupUi(self)
        self.setAttribute(Qt.WA_StyledBackground,True)

    def confirm(self):
        zw=self.buttonGroup.checkedButton().property('val')
        phone_num=self.phone_num_le.text()
        self.confirm_signal.emit({'zw':zw,'phone_num':phone_num})
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    Query=BookPane()

    Query.show()

    sys.exit(app.exec_())