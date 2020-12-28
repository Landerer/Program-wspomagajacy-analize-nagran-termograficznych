import logging
from typing import Tuple

from PyQt5.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsSceneMouseEvent,
    QGraphicsView,
)
from PyQt5.QtGui import (
    QPainter,
    QPen,
    QResizeEvent,
)
from PyQt5.QtCore import QLineF, QRectF, QSizeF, Qt
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem


class VideoScene(QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.videoItem = QGraphicsVideoItem()
        self.videoItem.setPos(0, 0)
        self.videoItem.nativeSizeChanged.connect(self.videoSizeChanged)
        self.addItem(self.videoItem)

        self.rectangle = QGraphicsRectItem()
        self.addItem(self.rectangle)

    def videoSizeChanged(self, size: QSizeF):
        logging.debug("%s", size)
        if not size.isEmpty():
            logging.debug("%s", size)
            self.videoItem.prepareGeometryChange()
            self.videoItem.setSize(size)
            self.setSceneRect(self.videoItem.boundingRect())

    def clearSelection(self) -> None:
        self.rectangle.setRect(QRectF())

    @property
    def selection(self) -> Tuple[int, int, int, int]:
        return self.rectangle.rect().toRect().getCoords()

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.startPos = event.scenePos()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.rectangle.prepareGeometryChange()
        self.rectangle.setRect(QRectF(self.startPos, event.scenePos()).normalized())
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        logging.info("Selection: %s", self.selection)
        return super().mouseReleaseEvent(event)

    def paintGrid(self, painter: QPainter, rect: QRectF, gridSize: int):
        left, top, right, bottom = rect.getCoords()
        x_min = (int(left - 1) // gridSize + 1) * gridSize
        y_min = (int(top - 1) // gridSize + 1) * gridSize
        x_max = (int(right) // gridSize) * gridSize
        y_max = (int(bottom) // gridSize) * gridSize
        # logging.debug(
        #     "x=(%s<=%s..%s<=%s) y=(%s<=%s..%s<=%s)",
        #     *(left, x_min, x_max, right),
        #     *(top, y_min, y_max, bottom)
        # )
        painter.setPen(QPen(Qt.gray, 2))
        painter.drawLines(QLineF(0, top, 0, bottom), QLineF(left, 0, right, 0))
        painter.setPen(QPen(Qt.gray, 1))
        painter.drawLines(
            QLineF(x, top, x, bottom) for x in range(x_min, x_max + 1, gridSize) if x
        )
        painter.drawLines(
            QLineF(left, y, right, y) for y in range(y_min, y_max + 1, gridSize) if y
        )

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        super().drawBackground(painter, rect)
        self.paintGrid(painter, rect, 20)


class VideoView(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        scene = VideoScene(self)
        self.setScene(scene)
        scene.sceneRectChanged.connect(self.sceneRectChanged)

    def scene(self) -> VideoScene:
        return super().scene()

    def _zoomToVideo(self):
        if not self.scene().videoItem.nativeSize().isEmpty():
            self.fitInView(self.scene().videoItem, Qt.KeepAspectRatio)

    def sceneRectChanged(self, rect: QRectF) -> None:
        self._zoomToVideo()

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self._zoomToVideo()