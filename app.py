import sys
import cv2 as cv
from myui import Ui_MainWindow    # my own ui
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject, QMutex
import time

class AppWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Connection btw events & functions
        self.ui.pushButton11.clicked.connect(self.pushButton11_Click)
        self.ui.pushButton21.clicked.connect(self.pushButton21_Click)
    def pushButton11_Click(self):
        self.popup = AppPopup()
        self.popup.setGeometry(200, 200, 600, 600)
        self.popup.disparity()
        self.popup.showgrayImg()
        self.popup.show()
    def pushButton21_Click(self):
        self.popup211 = AppPopup()
        self.popup211.setGeometry(200, 200, 600, 600)
        self.popup211.showVideo()
        self.popup211.show()
        self.popup212 = AppPopup()
        self.popup212.setGeometry(600, 200, 600, 600)
        self.popup212.bgsub()
        self.popup212.show()

class Communicate(QObject):
    signal = pyqtSignal(str)

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    # def __init__(self, frequent=20):
    #     QThread.__init__(self)
    #     self.stopped = False
    #     self.frequent = frequent
    #     self.mutex = QMutex()
    def run(self):
        # with QMutexLocker(self.mutex):
        #     self.stopped = False
        cap = cv.VideoCapture('input/bgSub.mp4')
        while True:
            # if self.stopped:
            #     return
            ret, frame = cap.read()
            if ret:
                rgbImage = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(320, 176, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.changePixmap.emit(p)
                # Sleep
                time.sleep(1 / self.frequent)
    def set_fps(self, fps):
        self.frequent = fps

class Thread2(QThread):
    changePixmap = pyqtSignal(QImage)
    def run(self):
        cap = cv.VideoCapture('input/bgSub.mp4')
        while True:
            ret, frame = cap.read()
            if ret:
                backSub = cv.createBackgroundSubtractorMOG2(history=50, varThreshold=190, detectShadows=False)
                fgMask = backSub.apply(frame)
                cv.rectangle(frame, (10, 2), (100,2), (255,255,255), -1)
                cv.putText(frame, str(cap.get(cv.CAP_PROP_POS_FRAMES)), (15, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
                # Covert to Qimg
                rgbImage = cv.cvtColor(fgMask, cv.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(320, 176, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.changePixmap.emit(p)
                # Sleep
                time.sleep(1 / self.frequent)
    def set_fps(self, fps):
        self.frequent = fps

class AppPopup(QtWidgets.QWidget):
    def __init__(self, choice=0):
        super().__init__()
        self.initUI(choice)
        self.show()
    def initUI(self, choice):
        if choice == 0:
            self.label = QtWidgets.QLabel('', self)
        elif choice == 1:
            self.label = QtWidgets.QLabel('', self)
            self.sl = QtWidgets.QSlider(self)
            self.sl.setGeometry(QtCore.QRect(0, 0, 160, 22))
            self.sl.setMaximum(100)
            self.sl.setProperty('value', 0)
            self.sl.setOrientation(QtCore.Qt.Horizontal)
            self.sl.valueChanged.connect(self.blend) 
        elif choice == 2:
            self.label_pic = []
            self.label = []
            for i in range(10):
                self.label_pic.append(QtWidgets.QLabel('', self))
                self.label.append(QtWidgets.QLabel('', self))
    def showImg(self):
        # Change opencv's image to Qimage
        height, width, channel = self.img.shape
        bytesPerLine = channel * width
        self.qImg = QImage(self.img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        # Show Qimage
        self.label.setGeometry(0, 0, width, height)
        self.label.setPixmap(QPixmap.fromImage(self.qImg))
    def showgrayImg(self):
        # Change opencv's image to Qimage
        height, width = self.img.shape
        self.qImg = QImage(self.img.data, width, height, width, QImage.Format_Grayscale8).rgbSwapped()
        # Show Qimage
        self.label.setGeometry(0, 0, width, height)
        self.label.setPixmap(QPixmap.fromImage(self.qImg))
    def disparity(self):
        imgL = cv.imread('input/imL.png', cv.IMREAD_GRAYSCALE)
        imgR = cv.imread('input/imR.png', cv.IMREAD_GRAYSCALE)
        stereo = cv.StereoBM_create(numDisparities=64, blockSize=9)
        self.img = stereo.compute(imgL, imgR)
    def showVideo(self):
        self.label.setGeometry(0, 0, 320, 176)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.set_fps(40)
        th.start()
    def bgsub(self):
        self.label.setGeometry(0, 0, 320, 176)
        th = Thread2(self)
        th.changePixmap.connect(self.setImage)
        th.set_fps(40)
        th.start()
    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())
