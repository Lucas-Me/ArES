# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'splash_screenRwbHDn.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import Qt, QMetaObject, QRect, QCoreApplication
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QFrame, QLabel, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor
from resources import splash_resource

class SplashScreen(QMainWindow):

    def __init__(self):
        # Splash art
        super().__init__()
        #
        self.splash_ui = Ui_SplashScreen()
        self.splash_ui.setupUi(self)

        # FLAGS
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Drop shadow effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.splash_ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        # show
        self.show()


class Ui_SplashScreen(object):
    def setupUi(self, MainWindow):
        self.object_name = u"SplashScreen"
        if not MainWindow.objectName():
            MainWindow.setObjectName(self.object_name)
        MainWindow.resize(292, 270)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.dropShadowFrame = QFrame(self.centralwidget)
        self.dropShadowFrame.setObjectName(u"dropShadowFrame")
        self.dropShadowFrame.setStyleSheet(u"QFrame{\n"
        "background-color: transparent;\n"
        "color:rgb(255, 170, 0);\n"
        "border-radius:30px;\n"
        "}")
        self.dropShadowFrame.setFrameShape(QFrame.StyledPanel)
        self.dropShadowFrame.setFrameShadow(QFrame.Raised)
        self.label_2 = QLabel(self.dropShadowFrame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(9, 9, 256, 236))

        self.verticalLayout.addWidget(self.dropShadowFrame)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate(self.object_name, self.object_name, None))
        self.label_2.setText(QCoreApplication.translate(self.object_name, u"<html><head/><body><p align=\"center\"><img src=\":/Logo/logo.ico\"/></p></body></html>", None))
    # retranslateUi

