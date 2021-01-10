import logging
import pathlib
import sys
from textwrap import dedent

import sqlite3
import numpy

import pyqtgraph as pg
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QStyle

from PyQt5.QtCore import QObject, QRect, pyqtSlot as Slot
from PyQt5.QtMultimedia import QMediaPlayer
from pyqtgraph.graphicsItems.TextItem import TextItem

from interface import Ui_mainWindow
from seqplayer import SeqPlayer


class Application(QObject, Ui_mainWindow):
    def __init__(self, mainWindow: QMainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.userId: int = 0
        self.dbFile: str = ""
        self.setupUi()
        mainWindow.show()

    def setupUi(self):
        super().setupUi(self.mainWindow)
        self.createMediaPlayer()
        self.createGraphWidget()

        self.pickDirectory.clicked.connect(self.pickVideoClick)
        self.exitApplication.clicked.connect(self.mainWindow.close)
        self.showDataBase.clicked.connect(self.pickDataBaseClick)
        self.clearScene.clicked.connect(self.graphicsView.scene().clearSelection)

        self.playButton.clicked.connect(self.playButtonClicked)
        self.mediaDurationSlider.sliderMoved.connect(self.mediaPlayer.setPosition)
        self.graphicsView.scene().regionSelected.connect(self.displayGraph)

    def createMediaPlayer(self):
        self.mediaPlayer = SeqPlayer(self.mainWindow)
        self.mediaPlayer.setVideoOutput(self.graphicsView.scene().videoItem)
        self.mediaPlayer.videoAvailableChanged.connect(self.playButton.setEnabled)
        self.mediaPlayer.videoAvailableChanged.connect(
            self.mediaDurationSlider.setEnabled
        )
        self.mediaPlayer.stateChanged.connect(self.mediaPlayerStateChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.positionChanged.connect(self.mediaDurationSlider.setValue)
        self.mediaPlayer.positionChanged.connect(self.displayCurrentTemperature)
        self.mediaPlayerStateChanged(QMediaPlayer.StoppedState)

    def createGraphWidget(self):
        plotWidget = pg.PlotWidget()
        self.graphLayout.addWidget(plotWidget)
        self.plotItem = plotWidget.getPlotItem()
        self.plotItem.showGrid(x=True, y=True)
        self.plotItem.setLabel("left", "Średnia temperatura [°C]")
        self.plotItem.setLabel("bottom", "Czas [s]")
        self.plot = self.plotItem.plot()
        self.plotCurrent = self.plotItem.plot(
            symbol="o", symbolPen=(0, 122, 217), symbolBrush=(0, 122, 217)
        )
        self.currentLabel = TextItem("cell", (255, 255, 255), anchor=(0, 0))

    @Slot()
    def pickVideoClick(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self.mainWindow, "Otwórz plik", "", "SEQ files (*.seq);;IMG files (*.img)"
        )
        if filePath:
            self.videoPath = pathlib.Path(filePath)
            self.userId = self.videoPath.stem[0:2]
            self.mediaPlayer.setFile(self.videoPath)
            self.graphicsView.scene().clearSelection()
            self.displayUserData()
            self.mediaPlayer.play()

    @Slot()
    def playButtonClicked(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    @Slot(int)
    def durationChanged(self, duration: int):
        self.mediaDurationSlider.setMaximum(duration - 1)

    @Slot(QMediaPlayer.State)
    def mediaPlayerStateChanged(self, state: QMediaPlayer.PlayingState):
        if state == QMediaPlayer.PlayingState:
            buttonText = "Pause"
            buttonIcon = QStyle.SP_MediaPause
        else:
            buttonText = "Play"
            buttonIcon = QStyle.SP_MediaPlay

        self.playButton.setText(buttonText)
        self.playButton.setIcon(self.playButton.style().standardIcon(buttonIcon))

    @Slot(int)
    def displayCurrentTemperature(self, position: int):
        temperature = self.values[position]
        self.plotCurrent.setData([position], [temperature])
        self.currentLabel.setPos(position, temperature)
        self.currentLabel.setText(f"{position}, {temperature:.2f}")
        if self.currentLabel not in self.plotItem.items:
            self.plotItem.addItem(self.currentLabel)

    @Slot(QRect)
    def displayGraph(self, selection: QRect):
        reader = self.mediaPlayer.reader()
        if not reader:
            logging.error("Video not available")
        self.values = []
        for frame_number in range(reader.num_frames):
            frame = reader.frame(frame_number)
            temperatures = frame.data
            if not selection.isEmpty():
                temperatures = temperatures[
                    selection.top() : selection.bottom(),
                    selection.left() : selection.right(),
                ]
            self.values.append(numpy.average(temperatures))

        self.plot.setData(self.values)
        self.displayCurrentTemperature(self.mediaPlayer.position())
        self.plotItem.getViewBox().autoRange(padding=0.11)
        self.plotItem.getViewBox().setRange(xRange=(-10, reader.num_frames * 1.12))

    def getSurveyResults(self, userId: int):
        with sqlite3.connect(self.dbFile) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            return cursor.execute(
                "SELECT * FROM Ankieta WHERE Id=?", (userId,)
            ).fetchall()

    @Slot()
    def pickDataBaseClick(self):
        dbFile, _ = QFileDialog.getOpenFileName(
            self.mainWindow, "Otwórz bazę danych", "", "Database files (*.db)"
        )
        if dbFile:
            self.dbFile = dbFile
            self.displayUserData()

    def displayUserData(self):
        if not self.dbFile:
            self.userData.setText("Otwórz plik bazy danych")
        elif not self.userId:
            self.userData.setText("Załaduj plik z obrazem")
        else:
            try:
                surveyResults = self.getSurveyResults(self.userId)
                if surveyResults:
                    self.displaySurveyResults(surveyResults[0])
                else:
                    self.userData.setText(
                        dedent(
                            f"""\
                            Brak pasującego wyniku w bazie danych
                             dla użytkownika o ID "{self.userId}"
                            (dwa pierwsze znaki nazwy pliku wideo)
                            """
                        )
                    )
            except Exception as e:
                self.userData.setText(f"Nie udało się otworzyć bazy danych:\n {e}")

    def displaySurveyResults(self, userData):
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
    mainWindow = QtWidgets.QMainWindow()
    ui = Application(mainWindow)
    sys.exit(app.exec_())