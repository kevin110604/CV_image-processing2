# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myui.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 200)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.okButton = QtWidgets.QPushButton(self.centralwidget)
        self.okButton.setGeometry(QtCore.QRect(730, 340, 113, 32))
        self.okButton.setObjectName("okButton")
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setGeometry(QtCore.QRect(850, 340, 113, 32))
        self.cancelButton.setObjectName("cancelButton")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 0, 151, 121))
        self.groupBox.setObjectName("groupBox")
        self.pushButton11 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton11.setGeometry(QtCore.QRect(10, 30, 113, 32))
        self.pushButton11.setObjectName("pushButton11")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(360, 0, 151, 121))
        self.groupBox_3.setObjectName("groupBox_3")
        self.pushButton32 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton32.setGeometry(QtCore.QRect(10, 70, 113, 32))
        self.pushButton32.setObjectName("pushButton32")
        self.pushButton31 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton31.setGeometry(QtCore.QRect(10, 30, 113, 32))
        self.pushButton31.setObjectName("pushButton31")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(530, 0, 151, 121))
        self.groupBox_4.setObjectName("groupBox_4")
        self.pushButton41 = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton41.setGeometry(QtCore.QRect(10, 30, 113, 32))
        self.pushButton41.setObjectName("pushButton41")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(190, 0, 151, 121))
        self.groupBox_2.setObjectName("groupBox_2")
        self.pushButton21 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton21.setGeometry(QtCore.QRect(10, 30, 113, 32))
        self.pushButton21.setObjectName("pushButton21")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 700, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.okButton.setText(_translate("MainWindow", "OK"))
        self.cancelButton.setText(_translate("MainWindow", "Cancel"))
        self.groupBox.setTitle(_translate("MainWindow", "1. Stereo"))
        self.pushButton11.setText(_translate("MainWindow", "1.1"))
        self.groupBox_3.setTitle(_translate("MainWindow", "3. Optical Flow"))
        self.pushButton32.setText(_translate("MainWindow", "3.2"))
        self.pushButton31.setText(_translate("MainWindow", "3.1"))
        self.groupBox_4.setTitle(_translate("MainWindow", "4. AR"))
        self.pushButton41.setText(_translate("MainWindow", "4.1"))
        self.groupBox_2.setTitle(_translate("MainWindow", "2. Background Subtraction"))
        self.pushButton21.setText(_translate("MainWindow", "2.1"))
