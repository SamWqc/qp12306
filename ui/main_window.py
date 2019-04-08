from PyQt5.Qt import *
from ui.window import login_window
from ui.QueryPane import QueryPane

if __name__ == '__main__':
    import sys
    app=QApplication(sys.argv)

    loginwin=login_window()
    query_pane = QueryPane()

    def success_login_slot(content):
        print(content)
        loginwin.hide()

        query_pane.setWindowTitle(content)
        query_pane.show()


    loginwin.success_login.connect(success_login_slot)

    loginwin.show()

    sys.exit(app.exec_())



