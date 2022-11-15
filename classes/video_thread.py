import array
import datetime
import os

from PyQt5 import QtCore
from PyQt5.QtCore import QThread
import numpy as np
import cv2

from config.config import VIDEO_PATH
from main_stream import Detector


class VideoThread(QThread):
    change_pixmap_signal = QtCore.pyqtSignal(np.ndarray, dict, dict)

    def __init__(self):
        super(VideoThread, self).__init__()
        self._run_flag = True
        self.detector = Detector()
        self.save_video = False
        self.video_writer = None
        self.video_writer_detected = None

    def run(self):
        # capture from web cam
        self._run_flag = True
        self.cap = cv2.VideoCapture(1)
        self.im_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.im_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # self.num_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        print(f'im_width={self.im_width},\nim_height={self.im_height},\nfps={self.fps}')
        # ----------- video writer ________________________________________________________________
        file_name = os.path.join(VIDEO_PATH, 'raw_video{}.mp4'.format(self._get_ymd()))
        file_name2 = os.path.join(VIDEO_PATH, 'detected_video{}.mp4'.format(self._get_ymd()))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter(
            file_name, fourcc,
            self.fps, (self.im_width, self.im_height)
            )
        self.video_writer_detected = cv2.VideoWriter(
            file_name2
            , fourcc, self.fps,
            (self.im_width, self.im_height)
            )
        while self._run_flag:
            ret, cv_img = self.cap.read()
            if ret:
                # resized_image = cv2.resize(cv_img, (1280, 960))
                image, item_sorted, class_sorted = self.detector.detect(cv_img)
                if self.save_video:
                    # self.video_writer = cv2.VideoWriter(
                    #     file_name, fourcc, self.fps,
                    #     (self.im_width, self.im_height)
                    #     )
                    # self.video_writer_detected = cv2.VideoWriter(
                    #     file_name2 , fourcc, self.fps,
                    #     (self.im_width, self.im_height)
                    #     )
                    self.video_writer.write(cv_img)
                    self.video_writer_detected.write(image)
                self.change_pixmap_signal.emit(image, item_sorted, class_sorted)
        # shut down capture system
        self.cap.release()
        if self.video_writer is not None:
            self.video_writer.release()
        if self.video_writer_detected is not None:
            self.video_writer_detected.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False

    def start_video(self):
        self.save_video = True

    def stop_video(self):
        self.save_video = False

    def _get_ymd(self):
        now = datetime.datetime.now()
        year = now.year
        month = str(now.month)
        day = str(now.day)
        hour = str(now.hour)
        minute = str(now.minute)
        if len(month) != 2:
            month = '0' + month
        if len(day) != 2:
            day = '0' + day
        if len(hour) != 2:
            hour = '0' + hour
        minute = minute if len(minute) == 2 else '0' + minute
        return '{}{}{}{}{}'.format(year, month, day, hour, minute)
