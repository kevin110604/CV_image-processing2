import sys
import cv2 as cv
import numpy as np
from myui import Ui_MainWindow    # my own ui
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject, QMutex, QTimer
import time

class AppWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Connection btw events & functions
        self.ui.pushButton11.clicked.connect(self.pushButton11_Click)
        self.ui.pushButton21.clicked.connect(self.pushButton21_Click)
        self.ui.pushButton31.clicked.connect(self.pushButton31_Click)
        self.ui.pushButton32.clicked.connect(self.pushButton32_Click)
        self.ui.pushButton41.clicked.connect(self.pushButton41_Click)
    def pushButton11_Click(self):
        self.popup = AppPopup()
        self.popup.setGeometry(200, 200, 600, 600)
        self.popup.disparity()
        self.popup.showgrayImg()
        self.popup.show()
    def pushButton21_Click(self):
        capture = cv.VideoCapture('input/bgSub.mp4')
        # Check if it's ready to be read
        while not capture.isOpened():
            capture = cv.VideoCapture('input/bgSub.mp4')
            cv.waitKey(1000)
            print('Wait for the header')
        # Current frame
        pos_frame = capture.get(cv.CAP_PROP_POS_FRAMES)
        # Background subtractor object
        backSub = cv.createBackgroundSubtractorMOG2(history=50, varThreshold=190, detectShadows=False)
        while True:
            # Read a frame
            ret, frame = capture.read()
            if ret:
                # Apply subtractor
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
            # End of the video
            if capture.get(cv.CAP_PROP_POS_FRAMES) == capture.get(cv.CAP_PROP_FRAME_COUNT):
                print(capture.get(cv.CAP_PROP_FRAME_COUNT))
                break
        capture.release()
        cv.destroyAllWindows()
    def pushButton31_Click(self):
        capture = cv.VideoCapture('input/featureTracking.mp4')
        while True:
            ret, frame = capture.read()
            # Setup SimpleBlobDetector parameters.
            params = cv.SimpleBlobDetector_Params()
            # Change thresholds
            params.minThreshold = 90
            params.maxThreshold = 120
            # Filter by Area.
            # params.filterByArea = True
            # params.minArea = 50
            # Filter by Circularity
            params.filterByCircularity = True
            params.minCircularity = 0.81
            # Filter by Convexity
            # params.filterByConvexity = True
            # params.minConvexity = 0.9
            # Filter by Inertia
            # params.filterByInertia = True
            # params.minInertiaRatio = 0.01
            detector = cv.SimpleBlobDetector_create(params)
            # Detect blobs.
            keypoints = detector.detect(frame)
            # Draw detected blobs as red circles.
            # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
            img_keypoints = cv.drawKeypoints(frame, keypoints, np.array([]), (0, 0, 255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            # Show keypoints
            cv.imshow('Keypoints', img_keypoints)
            keyboard = cv.waitKey(1)
            if keyboard == 'q' or keyboard == 27:
                break
        capture.release()
        cv.destroyAllWindows()
    def pushButton32_Click(self):
        capture = cv.VideoCapture('input/featureTracking.mp4')
        # Read the first frame
        ret, frame = capture.read()
        # Setup SimpleBlobDetector parameters.
        params = cv.SimpleBlobDetector_Params()
        # Change thresholds
        params.minThreshold = 90
        params.maxThreshold = 120
        # Filter by Area.
        # params.filterByArea = True
        # params.minArea = 50
        # Filter by Circularity
        params.filterByCircularity = True
        params.minCircularity = 0.81
        # Filter by Convexity
        # params.filterByConvexity = True
        # params.minConvexity = 0.9
        # Filter by Inertia
        # params.filterByInertia = True
        # params.minInertiaRatio = 0.01
        detector = cv.SimpleBlobDetector_create(params)
        # Detect blobs.
        keypoints = detector.detect(frame)
        # Turn the point list to np array with shape (n, 1, 2)
        p0 = np.zeros((len(keypoints), 1, 2), dtype='f')
        p0[0, 0, 0] = keypoints[0].pt[0]
        p0[0, 0, 1] = keypoints[0].pt[1]
        p0[1, 0, 0] = keypoints[1].pt[0]
        p0[1, 0, 1] = keypoints[1].pt[1]
        p0[2, 0, 0] = keypoints[2].pt[0]
        p0[2, 0, 1] = keypoints[2].pt[1]
        p0[3, 0, 0] = keypoints[3].pt[0]
        p0[3, 0, 1] = keypoints[3].pt[1]
        p0[4, 0, 0] = keypoints[4].pt[0]
        p0[4, 0, 1] = keypoints[4].pt[1]
        p0[5, 0, 0] = keypoints[5].pt[0]
        p0[5, 0, 1] = keypoints[5].pt[1]
        p0[6, 0, 0] = keypoints[6].pt[0]
        p0[6, 0, 1] = keypoints[6].pt[1]
        # LK params
        lk_params = dict(winSize = (15,15),
                         maxLevel = 2,
                         criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))
        # Create a mask image for drawing purposes
        old_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        mask = np.zeros_like(frame)

        while True:
            # Read a frame
            ret, frame = capture.read()
            if not ret:
                break
            frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            # Calculate optical flow
            p1, st, err = cv.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
            # Select good points
            good_new = p1[st==1]
            good_old = p0[st==1]
            # Draw the tracks
            for i,(new,old) in enumerate(zip(good_new,good_old)):
                a, b = new.ravel()
                c, d = old.ravel()
                mask = cv.line(mask, (a,b), (c,d), (0, 0, 255), 2)
                frame = cv.circle(frame, (a,b), 5, (0, 0, 255), -1)
            img = cv.add(frame, mask)
            # Show the frame
            cv.imshow('Optical flow', img)
            keyboard = cv.waitKey(1)
            if keyboard == 'q' or keyboard == 27:
                break
            # End of the video
            if capture.get(cv.CAP_PROP_POS_FRAMES) == capture.get(cv.CAP_PROP_FRAME_COUNT):
                print(capture.get(cv.CAP_PROP_FRAME_COUNT))
                break
            # Now update the previous frame and previous points
            old_gray = frame_gray.copy()
            p0 = good_new.reshape(-1, 1, 2)
        capture.release()
        cv.destroyAllWindows()
    def pushButton41_Click(self):
        self.popup411 = AppPopup(choice=2)
        self.popup411.setGeometry(100, 100, 500, 500)
        self.popup411.show()

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
            self.label = QtWidgets.QLabel('', self)
            self.timer = QTimer(self)                       # Construct QTimer 
            self.timer.timeout.connect(self.ar)             # Run ar() when timeout
            self.timer.start(500)                           # Start timer every 500 ms
            self.i = 0                                      # Init index
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
        self.img -= self.img.min()
        self.img = np.divide(self.img, self.img.max())
        self.img = np.multiply(self.img, 255)
        self.img = self.img.astype(np.uint8)
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
    def ar(self):
        # Coordinates of the pyramid
        tmp = [[3, 3, -4], [1, 1, 0], [1, 5, 0], [5, 5, 0], [5, 1, 0]]
        coordinates = np.array(tmp, dtype='f')
        # Distortion
        tmp = [[-0.128742, 0.090577, -0.000991, 0.00000278, 0.002292]]
        distortion = np.array(tmp)
        # Intrinsic parameters
        tmp = [[2225.495854,    0,        1025.545958],
               [   0,        2225.184140, 1038.585188], 
               [   0,           0,           1]]
        intrinsic = np.array(tmp)
        # Extrinsic parameters
        extrinsic = []
        tmp = [[-0.971574, -0.018274, 0.236028,  6.812538],
               [ 0.071480, -0.973127, 0.218892,  3.373303],
               [ 0.225685,  0.229541, 0.946771, 16.715723]]
        extrinsic.append(np.array(tmp))
        tmp = [[-0.888479, -0.145309, -0.435303,  3.392550],
               [ 0.071480, -0.980789,  0.181502,  4.361492],
               [-0.453314,  0.130145,  0.881798, 22.159574]]
        extrinsic.append(np.array(tmp))
        tmp = [[-0.523909,  0.223127, 0.822029,  2.687748],
               [ 0.005304, -0.964206, 0.265100,  4.709900],
               [ 0.851757,  0.143249, 0.503973, 12.981476]]
        extrinsic.append(np.array(tmp))
        tmp = [[-0.631086,  0.530130, 0.566296,  1.227818],
               [ 0.132633, -0.645539, 0.752121,  3.480230],
               [ 0.764289,  0.549763, 0.337078, 10.984053]]
        extrinsic.append(np.array(tmp))
        tmp = [[-0.876768, -0.230205,  0.422235,  4.436411],
               [ 0.197082, -0.972869, -0.121175,  0.671774],
               [ 0.438675, -0.023028,  0.898350, 16.240692]]
        extrinsic.append(np.array(tmp))
        # Read the img file
        path = 'input/' + str(self.i+1) + '.bmp'
        img = cv.imread(path, cv.IMREAD_COLOR)
        # Project the pyramid to image plane
        rotation = extrinsic[self.i][:, :3]
        translation = extrinsic[self.i][:, 3]
        points, jacobian = cv.projectPoints(coordinates, rotation, translation, intrinsic, distortion)
        # Draw the base of the pyramid
        cv.line(img, (points[1][0][0], points[1][0][1]), (points[2][0][0], points[2][0][1]), (0, 0, 255), 5)
        cv.line(img, (points[2][0][0], points[2][0][1]), (points[3][0][0], points[3][0][1]), (0, 0, 255), 5)
        cv.line(img, (points[3][0][0], points[3][0][1]), (points[4][0][0], points[4][0][1]), (0, 0, 255), 5)
        cv.line(img, (points[4][0][0], points[4][0][1]), (points[1][0][0], points[1][0][1]), (0, 0, 255), 5)
        # Draw the four sides of the pyramid
        cv.line(img, (points[0][0][0], points[0][0][1]), (points[1][0][0], points[1][0][1]), (0, 0, 255), 5)
        cv.line(img, (points[0][0][0], points[0][0][1]), (points[2][0][0], points[2][0][1]), (0, 0, 255), 5)
        cv.line(img, (points[0][0][0], points[0][0][1]), (points[3][0][0], points[3][0][1]), (0, 0, 255), 5)
        cv.line(img, (points[0][0][0], points[0][0][1]), (points[4][0][0], points[4][0][1]), (0, 0, 255), 5)
        # Resize
        self.img = cv.resize(img, (500, 500))
        # Change opencv's image to Qimage
        height, width, channel = self.img.shape
        bytesPerLine = channel * width
        self.qImg = QImage(self.img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        # Show Qimage
        self.label.setGeometry(0, 0, width, height)
        self.label.setPixmap(QPixmap.fromImage(self.qImg))
        # Increment
        if self.i < 4:
            self.i += 1
        else:
            self.i = 0

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())
