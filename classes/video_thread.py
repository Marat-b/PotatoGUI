import array

from PyQt5 import QtCore
from PyQt5.QtCore import QThread
import numpy as np
import cv2

from main_stream import Detector


class VideoThread(QThread):
    change_pixmap_signal = QtCore.pyqtSignal(np.ndarray, dict, dict)

    def __init__(self):
        super(VideoThread, self).__init__()
        self._run_flag = True
        self.detector = Detector()

    def run(self):
        # capture from web cam
        self._run_flag = True
        self.cap = cv2.VideoCapture(1)
        self.im_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.im_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # self.num_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        print(f'im_width={self.im_width},\nim_height={self.im_height},\nfps={self.fps}')
        while self._run_flag:
            ret, cv_img = self.cap.read()
            if ret:
                # resized_image = cv2.resize(cv_img, (1280, 960))
                image, item_sorted, class_sorted = self.detector.detect(cv_img)
                self.change_pixmap_signal.emit(image, item_sorted, class_sorted)
        # shut down capture system
        self.cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False