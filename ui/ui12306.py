# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui12306.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(650, 500)
        Dialog.setMinimumSize(QtCore.QSize(650, 500))
        Dialog.setMaximumSize(QtCore.QSize(650, 500))
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(40, 10, 580, 450))
        self.widget.setMinimumSize(QtCore.QSize(580, 450))
        self.widget.setMaximumSize(QtCore.QSize(580, 450))
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.account = QtWidgets.QLineEdit(self.widget)
        self.account.setMinimumSize(QtCore.QSize(0, 50))
        self.account.setStyleSheet("font: 12pt \"微软雅黑\";")
        self.account.setClearButtonEnabled(True)
        self.account.setObjectName("account")
        self.gridLayout.addWidget(self.account, 0, 0, 1, 2)
        self.refresh = QtWidgets.QPushButton(self.widget)
        self.refresh.setMinimumSize(QtCore.QSize(150, 30))
        self.refresh.setMaximumSize(QtCore.QSize(150, 30))
        self.refresh.setStyleSheet("\n"
"font: 25 11pt \"微软雅黑\";")
        self.refresh.setObjectName("refresh")
        self.gridLayout.addWidget(self.refresh, 2, 0, 1, 1)
        self.pwd = QtWidgets.QLineEdit(self.widget)
        self.pwd.setMinimumSize(QtCore.QSize(0, 50))
        self.pwd.setStyleSheet("font: 12pt \"微软雅黑\";")
        self.pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pwd.setObjectName("pwd")
        self.gridLayout.addWidget(self.pwd, 1, 0, 1, 2)
        self.login_check = QtWidgets.QPushButton(self.widget)
        self.login_check.setEnabled(False)
        self.login_check.setMinimumSize(QtCore.QSize(350, 40))
        self.login_check.setObjectName("login_check")
        self.gridLayout.addWidget(self.login_check, 4, 0, 1, 2)
        self.auto_check = QtWidgets.QPushButton(self.widget)
        self.auto_check.setMinimumSize(QtCore.QSize(0, 30))
        self.auto_check.setStyleSheet("font: 11pt \"微软雅黑\";")
        self.auto_check.setObjectName("auto_check")
        self.gridLayout.addWidget(self.auto_check, 3, 0, 1, 1)
        self.yzm_label = SzLabel(self.widget)
        self.yzm_label.setMinimumSize(QtCore.QSize(293, 190))
        self.yzm_label.setMaximumSize(QtCore.QSize(293, 190))
        self.yzm_label.setStyleSheet("")
        self.yzm_label.setObjectName("yzm_label")
        self.gridLayout.addWidget(self.yzm_label, 2, 1, 2, 1)

        self.retranslateUi(Dialog)
        self.refresh.clicked.connect(Dialog.refresh_yzm)
        self.auto_check.clicked.connect(Dialog.auto_yz)
        self.login_check.clicked.connect(Dialog.login)
        self.account.textChanged['QString'].connect(Dialog.account_enable)
        self.pwd.textChanged['QString'].connect(Dialog.account_enable)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.account.setPlaceholderText(_translate("Dialog", "12306账号"))
        self.refresh.setText(_translate("Dialog", "验证码刷新"))
        self.pwd.setPlaceholderText(_translate("Dialog", "密码"))
        self.login_check.setText(_translate("Dialog", "登录"))
        self.auto_check.setText(_translate("Dialog", "自动填写验证码"))
        self.yzm_label.setText(_translate("Dialog", "TextLabel"))

from Sz_Label import SzLabel
