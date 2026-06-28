from PySide6.QtCore import QObject, Signal, QTimer

class IMediaSignals(QObject):
    frameReady = Signal(object)
    mediaOpened = Signal()
    mediaFailed = Signal()
    mediaClosed = Signal()
    stopOtherActivities = Signal()

    def __init__(self, device=None, fps=30, parent=None):
        super().__init__(parent)
        self.device = device
        self.fps = fps
        self.frame_processors = []
        self.timer_media = QTimer()
        self.timer_media.setInterval(int(1000 / fps))

    def isActive(self):
        return self.timer_media.isActive()

    def addFrameProcessor(self, func):
        if not hasattr(self, 'frame_processors'):
            self.frame_processors = []
        self.frame_processors.append(func)

    def removeFrameProcessor(self, func):
        if hasattr(self, 'frame_processors') and func in self.frame_processors:
            self.frame_processors.remove(func)

    def setDevice(self, device):
        self.device = device

class ImageSignals(QObject):
    frameReady = Signal(object)
    imageOpened = Signal()
    imageClosed = Signal()
    imageFailed = Signal()
    stopOtherActivities = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.processing = False
        self.path = None
        self.file_name = None

    def isActive(self):
        return self.processing

    def addFrameProcessor(self, func):
        if not hasattr(self, 'frame_processors'):
            self.frame_processors = []
        self.frame_processors.append(func)

    def removeFrameProcessor(self, func):
        if hasattr(self, 'frame_processors') and func in self.frame_processors:
            self.frame_processors.remove(func)

    def setPath(self, path):
        self.path = path

    def stopProcess(self):
        self.processing = False
        self.imageClosed.emit()

    def getFileName(self):
        return self.file_name
