# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Application(object):
    def setupUi(self, Application):
        Application.setObjectName("Application")
        Application.resize(914, 605)
        self.exitButton = QtWidgets.QPushButton(Application)
        self.exitButton.setGeometry(QtCore.QRect(600, 550, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.exitButton.setFont(font)
        self.exitButton.setObjectName("exitButton")
        self.pickDirectory = QtWidgets.QPushButton(Application)
        self.pickDirectory.setGeometry(QtCore.QRect(600, 20, 291, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pickDirectory.sizePolicy().hasHeightForWidth())
        self.pickDirectory.setSizePolicy(sizePolicy)
        self.pickDirectory.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pickDirectory.setFont(font)
        self.pickDirectory.setObjectName("pickDirectory")
        self.numOfFrame = QtWidgets.QSpinBox(Application)
        self.numOfFrame.setEnabled(True)
        self.numOfFrame.setGeometry(QtCore.QRect(780, 110, 121, 22))
        self.numOfFrame.setObjectName("numOfFrame")
        self.numOfFrameLabel = QtWidgets.QLabel(Application)
        self.numOfFrameLabel.setGeometry(QtCore.QRect(570, 110, 211, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.numOfFrameLabel.setFont(font)
        self.numOfFrameLabel.setObjectName("numOfFrameLabel")
        self.showTemperatureDiagram = QtWidgets.QPushButton(Application)
        self.showTemperatureDiagram.setGeometry(QtCore.QRect(600, 240, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.showTemperatureDiagram.setFont(font)
        self.showTemperatureDiagram.setCheckable(False)
        self.showTemperatureDiagram.setChecked(False)
        self.showTemperatureDiagram.setObjectName("showTemperatureDiagram")
        self.clearScene = QtWidgets.QPushButton(Application)
        self.clearScene.setGeometry(QtCore.QRect(600, 190, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.clearScene.setFont(font)
        self.clearScene.setCheckable(False)
        self.clearScene.setChecked(False)
        self.clearScene.setObjectName("clearScene")
        self.ifShowFrame = QtWidgets.QCheckBox(Application)
        self.ifShowFrame.setGeometry(QtCore.QRect(640, 80, 231, 20))
        self.ifShowFrame.setObjectName("ifShowFrame")
        self.showDataBase = QtWidgets.QPushButton(Application)
        self.showDataBase.setGeometry(QtCore.QRect(600, 370, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.showDataBase.setFont(font)
        self.showDataBase.setCheckable(False)
        self.showDataBase.setChecked(False)
        self.showDataBase.setObjectName("showDataBase")
        self.chooseUser = QtWidgets.QComboBox(Application)
        self.chooseUser.setGeometry(QtCore.QRect(600, 450, 291, 22))
        self.chooseUser.setObjectName("chooseUser")
        self.chooseUserLabel = QtWidgets.QLabel(Application)
        self.chooseUserLabel.setGeometry(QtCore.QRect(600, 430, 161, 16))
        self.chooseUserLabel.setObjectName("chooseUserLabel")
        self.textEdit = QtWidgets.QTextEdit(Application)
        self.textEdit.setEnabled(False)
        self.textEdit.setGeometry(QtCore.QRect(20, 370, 491, 221))
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(Application)
        QtCore.QMetaObject.connectSlotsByName(Application)

    def retranslateUi(self, Application):
        _translate = QtCore.QCoreApplication.translate
        Application.setWindowTitle(_translate("Application", "Oprogramowanie wspomagające diagnozę objawu Raynauda"))
        self.exitButton.setText(_translate("Application", "Wyjdź z programu"))
        self.exitButton.setShortcut(_translate("Application", "Esc"))
        self.pickDirectory.setText(_translate("Application", "Wybierz plik wideo"))
        self.numOfFrameLabel.setText(_translate("Application", "Podaj numer klatki do wyświetlenia:"))
        self.showTemperatureDiagram.setText(_translate("Application", "Wyświetl wykres zmiany temperatury"))
        self.clearScene.setText(_translate("Application", "Wyczyść obraz"))
        self.ifShowFrame.setText(_translate("Application", "Wyświetl konkretną klatkę filmu"))
        self.showDataBase.setText(_translate("Application", "Wyświetl dane z bazy danych"))
        self.chooseUserLabel.setText(_translate("Application", "Wybierz użytkownika"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Application = QtWidgets.QDialog()
    ui = Ui_Application()
    ui.setupUi(Application)
    Application.show()
    sys.exit(app.exec_())
