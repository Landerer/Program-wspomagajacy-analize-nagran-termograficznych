import sys
import sqlite3
from interface import Ui_Application
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QRubberBand, QFileDialog
from PyQt5.QtGui import QImage, QPixmap, QMouseEvent
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
        
       
        
        
    def createImageView(self, mainWindow):
        self.image = QImage(300, 1000, QImage.Format_RGB32)
        self.image.fill(Qt.black)
        
        self.pixmap = QPixmap.fromImage(self.image)
        
        self.scene = QGraphicsScene()
        # self.scene.addPixmap(self.pixmap)
        
        self.graphicsView = ImageView(mainWindow)
        self.graphicsView.setGeometry(QtCore.QRect(20, 20, 511, 331))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setScene(self.scene)
        
        ###
        self.mediaPlayer = QMediaPlayer(mainWindow)
        self.videoItem = QGraphicsVideoItem()
        self.videoSize = self.graphicsView.size()
        print(self.videoSize) #zwraca PyQt5.QtCore.QSize(511, 331)
        self.vidSizeF = QSizeF(self.videoSize)
        self.videoItem.setSize(self.vidSizeF)
        
        self.mediaPlayer.setVideoOutput(self.videoItem)
        self.graphicsView.scene().addItem(self.videoItem)
        self.graphicsView.show()
        
        ###
        
        # self.scene.setSceneRect(*self.graphicsView.geometry().getRect())
        self.clearScene.clicked.connect(self.clearRubberBandClick)
    

    def pickDirectoryClick(self):
        aviFile = QFileDialog.getOpenFileName(self.mainWindow, 'Otwórz plik', 'c:\\',"Avi files (*.avi)")
        self.mediaPlayer.stop()
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(aviFile[0])))
        self.mediaPlayer.play()
        
        
        
    def clearRubberBandClick(self):
        self.graphicsView.rubberBand.hide()
        
        
          
        # if (video.isOpened()== False): 
        #     print("Error opening video stream or file")
        # while(video.isOpened()):
        #     ret, frame = video.read()
        #     if ret == True:
        #         cv2.imshow('Frame',frame).
        #         if cv2.waitKey(25) & 0xFF == ord('q'):
        #             break
        #     else: 
        #         break

        # video.release()
        # cv2.destroyAllWindows()
        
    
        
        
    def showDataBaseClick(self):
        dbFile = QFileDialog.getOpenFileName(self.mainWindow, 'Otwórz bazę danych', 'c:\\',"Database files (*.db)")
        print(dbFile)
        
        # connection = sqlite3.connect(dbFile[0])
        with sqlite3.connect(dbFile[0]) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
        
            for row in cursor.execute("SELECT * FROM Ankieta"):
                row = dict(zip(row.keys(), row))
                print(row)
                



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QDialog()
    ui = Application()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())