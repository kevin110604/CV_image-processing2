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
        capture = cv.VideoCapture('input/bgSub.mp4')
        # check if it's ready to be read
        while not capture.isOpened():
            capture = cv.VideoCapture('bgSub.mp4')
            cv.waitKey(1000)
            print('Wait for the header')
        # current frame
        pos_frame = capture.get(cv.CAP_PROP_POS_FRAMES)
        # background subtractor object
        backSub = cv.createBackgroundSubtractorMOG2(history=50, varThreshold=190, detectShadows=False)
        while True:
            # read a frame
            ret, frame = capture.read()
            if ret:
                # apply subtractor
                fgMask = backSub.apply(frame)
                cv.imshow('Origin', frame)
                cv.imshow('Foreground', fgMask)
            else:
                capture.set(cv.CAP_PROP_POS_FRAMES, pos_frame - 1)
                print('frame is not ready')
                cv.waitKey(1000)
            keyboard = cv.waitKey(30)
            if keyboard == 'q' or keyboard == 27:
                break
            # if the end of video, break
            if capture.get(cv.CAP_PROP_POS_FRAMES) == capture.get(cv.CAP_PROP_FRAME_COUNT):
                print(capture.get(cv.CAP_PROP_FRAME_COUNT))
                break
        capture.release()
        cv.destroyAllWindows()

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
                print(frame.shape)
                backSub = cv.createBackgroundSubtractorKNN(history=500, dist2Threshold=400, detectShadows=False)
                frameImage = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                # frameImage = frame
                print(frameImage.shape)
                fgMask = backSub.apply(frameImage)
                print('fgMask', fgMask.shape)
                # Get the frame number and write it on the current frame
                # cv.rectangle(frame, (20, 20), (300,140), (255,255,255), -1)
                # cv.putText(frame, str(cap.get(cv.CAP_PROP_POS_FRAMES)), (150, 150), cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
                # Covert to Qimg
                # frameImage = cv.cvtColor(frame, cv.IMREAD_GRAYSCALE)
                # frameImage = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                # fgImage = cv.cvtColor(fgMask, cv.COLOR_BGR2RGB)
                # fgImage = cv.cvtColor(fgMask, cv.IMREAD_GRAYSCALE)
                fgImage = fgMask
                Img = frameImage - fgImage
                # Img = fgImage
                h, w = Img.shape
                
                bytesPerLine = w
                # convertToQtFormat = QImage(frameImage.data, w, h, bytesPerLine, QImage.Format_RGB888) QImage.Format_Grayscale8
                convertToQtFormat = QImage(Img.data, w, h, bytesPerLine, QImage.Format_Grayscale8)
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
        th.set_fps(60)
        th.start()
    def bgsub(self):
        self.label.setGeometry(0, 0, 320, 176)
        th = Thread2(self)
        th.changePixmap.connect(self.setImage)
        th.set_fps(60)
        th.start()
    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())
