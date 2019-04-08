from PyQt5.Qt import *
from ui.query_win import Ui_Form
from API.API_TOOL import APITool
from ui.Book_Pane import BookPane
import re

class QueryPane(QWidget,Ui_Form):
    def __init__(self,parent=None,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.condition={'zw':None,'phone_num':None}
        self.setupUi(self)
        self.setupBookPane()
        self.setupData()

    def resizeEvent(self, evt):
        super().resizeEvent(evt)
        self.widget.resize(self.width(),0.25*self.height())
        self.tickets_tv.resize(self.width(),0.75*self.height())
        self.book_pane.resize(self.width(),self.widget.height()+30)

    def show_bookpane(self):
        animation = QPropertyAnimation(self.book_pane, b'pos',self.book_pane)
        animation.setStartValue(QPoint(0, -200))
        animation.setEndValue(QPoint(0, 0))
        animation.setDuration(1000)
        animation.setEasingCurve(QEasingCurve.OutBounce)
        animation.start(QAbstractAnimation.DeleteWhenStopped)

    def hide_bookpane(self):
        animation = QPropertyAnimation(self.book_pane, b'pos',self.book_pane)
        animation.setEndValue(QPoint(0, -self.widget.height()))
        animation.setStartValue(QPoint(0, 0))
        animation.setDuration(1000)
        animation.setEasingCurve(QEasingCurve.OutBounce)
        animation.start(QAbstractAnimation.DeleteWhenStopped)

    def setupBookPane(self):
        self.book_pane=BookPane(self)

        self.book_pane.confirm_signal.connect(self.book_filter)

        self.book_pane.resize(self.width(), 200)
        self.book_pane.move(0, -200)
        self.book_pane.show()

    ##城市下拉菜单设置
    def setupData(self):
        dic =APITool.get_all_station()
        self.from_station_cb.addItems(dic.keys())
        self.to_station_cb.addItems(dic.keys())

        completer_from=QCompleter(dic.keys())
        completer_to = QCompleter(dic.keys())
        self.from_station_cb.setCompleter(completer_from)
        self.to_station_cb.setCompleter(completer_to)
        def check_station():
            current_from_station=self.from_station_cb.currentText()
            current_to_station = self.to_station_cb.currentText()
            result_from_station=dic.keys().__contains__(current_from_station)
            result_to_station=dic.keys().__contains__(current_to_station)
            if not result_from_station:
                self.from_station_cb.clearEditText()
            pass

            if not result_to_station:
                self.to_station_cb.clearEditText()
            pass
        self.from_station_cb.lineEdit().editingFinished.connect(check_station)
        self.to_station_cb.lineEdit().editingFinished.connect(check_station)
        #设置日期
        self.start_date_de.setDate(QDate.currentDate())
        self.start_date_de.setMinimumDate(QDate.currentDate())

        #设置表格
        model=QStandardItemModel(self.tickets_tv)
        model_headers=['车次','出发站-到达站','出发时间-到达时间','历时','商务座/特等座','一等座','二等座','高级软卧','软卧/一等卧','动卧','硬卧/二等卧','硬座','无座','其他']

        model.setColumnCount(len(model_headers))
        for idex, title in enumerate(model_headers):
            model.setHeaderData(idex,Qt.Horizontal,title)

        self.tickets_tv.setModel(model)

    def query_tk(self):

        result=self.filter_tickets()
        model=self.tickets_tv.model()
        #QStandardItemModel().setItem()
        model.setRowCount(len(result))
        cols= ['train_name',('from_station_name','to_station_name'),('start_time','arrive_time'),'total_time','business_seat','st_seat','sec_seat','advanced_soft_bed','soft_bed','move_bed','hard_bed','hard_seat','no_seat','other_seat']

        for row,train_dic in enumerate(result):
            for col,col_name in enumerate(cols):
                if type(col_name) == str:
                    model.setItem(row,col,QStandardItem(train_dic[col_name]))
                else:
                    tmp="->".join([train_dic[key] for key in col_name])
                    model.setItem(row,col,QStandardItem(tmp))

        self.tickets_tv.setModel(model)

        return result

    def filter_tickets(self):
        print('查询')

        start_date = self.start_date_de.text()

        dic = APITool.get_all_station()
        from_station_code = dic[self.from_station_cb.currentText()]
        to_station_code = dic[self.to_station_cb.currentText()]

        ticket_type_codes = self.buttonGroup.checkedButton().property('q_value')

        result = APITool.ticket_query(start_date, from_station_code, to_station_code, ticket_type_codes,
                                      seat_type=self.condition['zw'])
        while {} in result:
            result.remove({})

        return result

    def book_filter(self,condition):
        self.hide_bookpane()
        self.condition=condition
        #check 手机号码是否正确
        phone_num=condition['phone_num']
        p=re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
        match_phone_num=p.match(phone_num)
        if len(phone_num)!=11 or not match_phone_num:
            print('手机号码输入有误')
            self.book_pane.phone_num_le.clear()
        else:
            print(phone_num)
            result=self.query_tk()
            if len(result)>0:
                 APITool.buy_ticket(result[0])


    def book_tk(self):
        print('抢票')
        self.show_bookpane()
















if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    Query=QueryPane()

    Query.show()

    sys.exit(app.exec_())