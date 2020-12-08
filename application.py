import sys
import sqlite3
from interface import Ui_Application
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QRubberBand, QFileDialog
from PyQt5.QtGui import QImage, QPixmap, QMouseEvent, QColor
from PyQt5.QtCore import Qt, QRect, QSize, QUrl, QSizeF
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem


class ImageView(QGraphicsView):
    def __init__(self, mainWindow):
        super().__init__(mainWindow)
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)

    def mousePressEvent(self, event: QMouseEvent):
        self.startPos = event.pos()
        self.rubberBand.setGeometry(QRect(self.startPos, QSize()))
        self.rubberBand.show()
        super().mousePressEvent(event)
        print(self.startPos)

    def mouseMoveEvent(self, event: QMouseEvent):
        self.rubberBand.setGeometry(QRect(self.startPos, event.pos()))
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        # self.rubberBand.hide()
        # self.scene().addRect(self.startPos.x(), self.startPos.y(), event.pos().x()-self.startPos.x(), event.pos().y()-self.startPos.y())
        super().mouseReleaseEvent(event)
        print(event.pos())


class Application(Ui_Application):
    def __init__(self):
        super().__init__()

    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)
        self.mainWindow = mainWindow
        self.createImageView(mainWindow)

        self.pickDirectory.clicked.connect(self.pickDirectoryClick)
        self.exitButton.clicked.connect(mainWindow.close)
        self.showDataBase.clicked.connect(self.showDataBaseClick)

        self.chooseUser.currentTextChanged.connect(self.onUserChosen)
        self.userData.setTextColor(QColor(0, 0, 0))

    def createImageView(self, mainWindow):
        self.image = QImage(300, 1000, QImage.Format_RGB32)
        self.image.fill(Qt.black)

        self.pixmap = QPixmap.fromImage(self.image)

        self.scene = QGraphicsScene()
        # self.scene.addPixmap(self.pixmap)

        self.graphicsView = ImageView(mainWindow)
        self.graphicsView.setGeometry(QtCore.QRect(20, 20, 681, 401))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setScene(self.scene)

        self.mediaPlayer = QMediaPlayer(mainWindow)
        self.videoItem = QGraphicsVideoItem()
        self.videoSize = self.graphicsView.size()
        print(self.videoSize)
        self.vidSizeF = QSizeF(self.videoSize)
        self.videoItem.setSize(self.vidSizeF)

        self.mediaPlayer.setVideoOutput(self.videoItem)
        self.graphicsView.scene().addItem(self.videoItem)
        self.graphicsView.show()

        # self.scene.setSceneRect(*self.graphicsView.geometry().getRect())
        self.clearScene.clicked.connect(self.clearRubberBandClick)

    def pickDirectoryClick(self):
        aviFile = QFileDialog.getOpenFileName(
            self.mainWindow, "Otwórz plik", "", "Avi files (*.avi)"
        )
        self.mediaPlayer.stop()
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(aviFile[0])))
        self.mediaPlayer.play()

    def clearRubberBandClick(self):
        self.graphicsView.rubberBand.hide()

    def showDataBaseClick(self):
        self.dbFile = QFileDialog.getOpenFileName(
            self.mainWindow, "Otwórz bazę danych", "", "Database files (*.db)"
        )[0]

        with sqlite3.connect(self.dbFile) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            idList = [
                str(row["Id"]) for row in cursor.execute("SELECT Id FROM Ankieta")
            ]
            self.chooseUser.addItems(idList)

    def onUserChosen(self, userId):
        with sqlite3.connect(self.dbFile) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            userData = cursor.execute(
                "SELECT * FROM Ankieta WHERE Id=?", [userId]
            ).fetchall()[0]
            self.userData.setText(
                f"Id: {userData['Id']}\n\
                Płeć: {userData['Plec']}\n\
                Wiek: {userData['Wiek']}\n\
                Województwo zamieszkania: {userData['Wojewodztwo']}\n\
                Jak często marzną dłonie/stopy: {userData['Marzniecie']}\n\
                Jak często bieleją lub sinieją dłonie/stopy: {userData['Sinienie']}\n\
                Jak często bierze zimne kąpiele: {userData['ZimneKapiele']}\n\
                Jak często morsuje: {userData['Morsowanie']}\n\
                Choroby: {userData['Choroby']}\n\
                Przyjmowane leki: {userData['Leki']}\n\
                Temperatura badanego: {userData['TempBadanego']}\n\
                Tetno początkowe badanego: {userData['TetnoPoczatkowe']}\n\
                Ciśnienie początkowe badanego: {userData['CisSkurczPoczatkowe']}/{userData['CisRozkurczPoczatkowe']}\n\
                Temperatura wody przed 1 badaniem: {userData['TempWodyDo1Badania']}\n\
                Tętno po 1 badaniu: {userData['TetnoPo1Badaniu']}\n\
                Ciśnienie po 1 badaniu: {userData['CisSkurczPo1Badaniu']}/{userData['CisRozkurczPo1Badaniu']}\n\
                Temperatura wody przed 2 badaniem: {userData['TempWodyDo2Badania']}\n\
                Tętno po drugim badaniu: {userData['TetnoPo2Badaniu']}\n\
                Ciśnienie po drugim badaniu: {userData['CisSkurczPo2Badaniu']}/{userData['CisRozkurczPo2Badaniu']}"
            )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QDialog()
    ui = Application()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())