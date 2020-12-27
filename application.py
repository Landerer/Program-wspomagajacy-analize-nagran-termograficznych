import math
import logging
import sys
from textwrap import dedent

import sqlite3

import pyqtgraph as pg
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QRubberBand, QFileDialog, QWidget
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import QRect, QSize, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

from interface import Ui_mainWindow


class RubberBandWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)

    def mousePressEvent(self, event: QMouseEvent):
        self.startPos = event.pos()
        self.rubberBand.setGeometry(QRect(self.startPos, QSize()))
        self.rubberBand.show()
        super().mousePressEvent(event)
        logging.debug(self.startPos)

    def mouseMoveEvent(self, event: QMouseEvent):
        self.rubberBand.setGeometry(QRect(self.startPos, event.pos()).normalized())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
        logging.debug(event.pos())


class Application(Ui_mainWindow):
    def __init__(self):
        super().__init__()

    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)
        self.mainWindow = mainWindow
        self.createVideoView(mainWindow)
        self.createGraphWidget()

        self.pickDirectory.clicked.connect(self.pickVideoClick)
        self.exitApplication.clicked.connect(mainWindow.close)
        self.showDataBase.clicked.connect(self.pickDataBaseClick)
        self.playButton.clicked.connect(self.play_video)
        self.mediaDurationSlider.sliderMoved.connect(self.set_position)

    def createVideoView(self, mainWindow):
        self.rubberBandWidget = RubberBandWidget()
        self.videoLayout.addWidget(self.rubberBandWidget)
        lay = QtWidgets.QVBoxLayout(self.rubberBandWidget)
        lay.setContentsMargins(0, 0, 0, 0)
        self.videoWidget = QVideoWidget()
        lay.addWidget(self.videoWidget)

        self.mediaPlayer = QMediaPlayer(mainWindow)
        self.mediaPlayer.setVideoOutput(self.videoWidget)

        self.clearScene.clicked.connect(self.clearRubberBandClick)
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    def createGraphWidget(self):
        plotWidget = pg.PlotWidget()
        self.graphLayout.addWidget(plotWidget)
        self.plot = plotWidget.getPlotItem().plot([], [])

    def pickVideoClick(self):
        aviFile = QFileDialog.getOpenFileName(
            self.mainWindow, "Otwórz plik", "", "Avi files (*.avi)"
        )[0]

        self.userId = aviFile[-6:-4]
        if aviFile != "":
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(aviFile)))
            self.playButton.setEnabled(True)

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.mediaPlayer.play()

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setText("Pause")

        else:
            self.playButton.setText("Play")

    def position_changed(self, position):
        self.mediaDurationSlider.setValue(position)

    def duration_changed(self, duration):
        logging.debug(duration)
        self.mediaDurationSlider.setRange(0, duration)
        self.displayGraph(duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def clearRubberBandClick(self):
        self.rubberBandWidget.rubberBand.hide()

    def displayGraph(self, videoDuration):
        x = list(range(videoDuration))
        y = [math.sin(x / 1000 * 2 * math.pi) for x in x]
        self.plot.setData(x, y)

    def pickDataBaseClick(self):
        self.dbFile = QFileDialog.getOpenFileName(
            self.mainWindow, "Otwórz bazę danych", "", "Database files (*.db)"
        )[0]

        with sqlite3.connect(self.dbFile) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            idList = [
                str(row["Id"]) for row in cursor.execute("SELECT Id FROM Ankieta")
            ]
            self.displayData()

    def displayData(self):

        with sqlite3.connect(self.dbFile) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            userData = cursor.execute(
                "SELECT * FROM Ankieta WHERE Id=?", [self.userId]
            ).fetchall()[0]
            self.userData.setText(
                dedent(
                    f"""\
                    Id: {userData['Id']}
                    Płeć: {userData['Plec']}
                    Wiek: {userData['Wiek']}
                    Województwo zamieszkania: {userData['Wojewodztwo']}
                    Jak często marzną dłonie/stopy: {userData['Marzniecie']}
                    Jak często bieleją lub sinieją dłonie/stopy: {userData['Sinienie']}
                    Jak często bierze zimne kąpiele: {userData['ZimneKapiele']}
                    Jak często morsuje: {userData['Morsowanie']}
                    Choroby: {userData['Choroby']}
                    Przyjmowane leki: {userData['Leki']}
                    Temperatura badanego: {userData['TempBadanego']} °C
                    Tetno początkowe badanego: {userData['TetnoPoczatkowe']}/min
                    Ciśnienie początkowe badanego: {userData['CisSkurczPoczatkowe']}/{userData['CisRozkurczPoczatkowe']} mmHg
                    Temperatura wody przed pierwszym badaniem: {userData['TempWodyDo1Badania']} °C
                    Tętno po pierwszym badaniu: {userData['TetnoPo1Badaniu']}/min
                    Ciśnienie po pierwszym badaniu: {userData['CisSkurczPo1Badaniu']}/{userData['CisRozkurczPo1Badaniu']} mmHg
                    Temperatura wody przed 2 badaniem: {userData['TempWodyDo2Badania']} °C
                    Tętno po drugim badaniu: {userData['TetnoPo2Badaniu']}/min
                    Ciśnienie po drugim badaniu: {userData['CisSkurczPo2Badaniu']}/{userData['CisRozkurczPo2Badaniu']} mmHg
                    """
                )
            )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)d %(name)s.%(funcName)s] %(message)s",
    )

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QDialog()
    ui = Application()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())