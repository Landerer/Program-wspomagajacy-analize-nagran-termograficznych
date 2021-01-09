import os
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from typing import Optional
from PyQt5.QtCore import QObject, QTimer, pyqtSignal as Signal, pyqtSlot as Slot
from PyQt5.QtGui import QImage
from PyQt5.QtMultimedia import QMediaPlayer, QVideoFrame, QVideoSurfaceFormat
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem

import fnv
import fnv.file
import numpy


class SeqReader:
    @dataclass
    class Frame:
        number: int
        data: numpy.ndarray
        time: Optional[datetime]

    def __init__(self, file_path: os.PathLike) -> None:
        self.file_path = str(file_path)
        self.file_mtime = datetime.fromtimestamp(os.path.getmtime(str(file_path)))
        self.im = fnv.file.ImagerFile(str(file_path))
        self.im.unit = fnv.Unit.TEMPERATURE_FACTORY

    @property
    def num_frames(self) -> int:
        return self.im.num_frames

    @property
    def width(self) -> int:
        return self.im.width

    @property
    def height(self):
        return self.im.height

    @lru_cache(maxsize=910)
    def frame(self, number) -> Frame:
        self.im.get_frame(number)
        frame = numpy.array(self.im.final, copy=True).reshape((self.height, self.width))
        frame_time = None
        for frame_info in self.im.frame_info:
            if frame_info["name"] == "Time":
                frame_time = datetime.strptime(
                    f"{self.file_mtime.year} " + frame_info["value"],
                    "%Y %j:%H:%M:%S.%f",
                )
                break

        return SeqReader.Frame(number, frame, frame_time)


class FrameVisualiser:
    def __init__(self, min: int = 10, max: int = 40) -> None:
        self.min = min
        self.max = max

    def __call__(self, frame: SeqReader.Frame) -> numpy.ndarray:
        return numpy.interp(frame.data, (self.min, self.max), (0, 255)).astype(
            numpy.uint8
        )


class SeqPlayer(QObject):
    FRAMES_PER_SECOND = 15

    videoAvailableChanged = Signal(bool)
    durationChanged = Signal(int)
    positionChanged = Signal(int)
    stateChanged = Signal(QMediaPlayer.State)

    def __init__(
        self, parent: Optional[QObject], visualiser: Optional[FrameVisualiser] = None
    ) -> None:
        super().__init__(parent=parent)
        self.visualiser = visualiser if visualiser else FrameVisualiser()
        self._reader: Optional[SeqReader] = None
        self._videoOutput: Optional[QGraphicsVideoItem] = None
        self._position: int = 0
        self._state: QMediaPlayer.State = QMediaPlayer.StoppedState
        self._timer = QTimer()
        self._timer.setInterval(1000 // self.FRAMES_PER_SECOND)
        self._timer.timeout.connect(self.displayNextFrame)

    def setFile(self, file_path: os.PathLike):
        try:
            self._reader = SeqReader(file_path)
        except:
            self._reader = None
            self.videoAvailableChanged.emit(False)
            raise
        self.videoAvailableChanged.emit(True)
        self.durationChanged.emit(self.duration())
        self.setPosition(0)
        self.displayFrame()

    def reader(self) -> Optional[SeqReader]:
        return self._reader

    def videoOutput(self) -> QGraphicsVideoItem:
        return self._videoOutput

    def setVideoOutput(self, videoOutput: QGraphicsVideoItem) -> None:
        self._videoOutput = videoOutput

    def duration(self) -> int:
        return self._reader.num_frames if self._reader else 0

    def position(self) -> int:
        return self._position

    @Slot(int)
    def setPosition(self, position: int) -> None:
        if self._position != position and position < self.duration():
            self._position = position
            self.displayFrame()
            self.positionChanged.emit(position)

    def state(self) -> QMediaPlayer.State:
        return self._state

    @Slot(QMediaPlayer.State)
    def setState(self, state: QMediaPlayer.State) -> None:
        self._state = state
        self.stateChanged.emit(state)

    def play(self):
        self.setState(QMediaPlayer.PlayingState)
        if self.position() == self.duration() - 1:
            self.setPosition(0)
        self._timer.start()

    def pause(self):
        self.setState(QMediaPlayer.PausedState)
        self._timer.stop()

    def displayNextFrame(self):
        self.setPosition(self.position() + 1)
        self.displayFrame()
        if self.position() == self.duration() - 1:
            self.pause()

    def displayFrame(self) -> None:
        if not self._reader:
            return
        frame = self._reader.frame(self._position)
        pixel_data = self.visualiser(frame)
        img = QImage(
            pixel_data.data,
            self._reader.width,
            self._reader.height,
            QImage.Format_Grayscale8,
        )
        video_surface = self.videoOutput().videoSurface()
        video_surface.start(QVideoSurfaceFormat(img.size(), QVideoFrame.Format_Y8))
        video_surface.present(QVideoFrame(img))