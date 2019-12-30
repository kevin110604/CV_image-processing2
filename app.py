import sys
import cv2 as cv
from myui import Ui_MainWindow    # my own ui
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

# QtGui.QApplication.setLibraryPaths([])

class AppWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Connection btw events & functions
        self.ui.pushButton11.clicked.connect(self.pushButton11_Click)
    def pushButton11_Click(self):
        self.popup = AppPopup()
        self.popup.setGeometry(200, 200, 600, 600)
        self.popup.disparity()
        self.popup.showgrayImg()
        self.popup.show()
    def pushButton21_Click(self):
        capture = cv.VideoCapture('input/bgSub.mp4')
        while True:
            ret, frame = capture.read()
            if frame is None:
                break
            
            backSub = cv.createBackgroundSubtractorKNN()
            fgMask = backSub.apply(frame)
            
            
            cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
            cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
                    cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
            
            
            cv.imshow('Frame', frame)
            cv.imshow('FG Mask', fgMask)
            
            keyboard = cv.waitKey(30)
            if keyboard == 'q' or keyboard == 27:
                break

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

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())
