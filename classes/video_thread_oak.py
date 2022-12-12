import datetime
import os

from PyQt5 import QtCore
from PyQt5.QtCore import QThread
import numpy as np
import cv2
import depthai as dai

from db.services.config_service import ConfigService
from depth.main_stream_depth import Detector


class VideoThread(QThread):
    change_pixmap_signal = QtCore.pyqtSignal(np.ndarray, dict, dict)

    def __init__(self):
        super(VideoThread, self).__init__()
        self._run_flag = True
        self.detector = Detector()
        self.save_video = False
        self.video_path = ConfigService.get_video_path()
        self.video_writer = None
        self.video_writer_detected = None

    def run(self):
        # capture from web cam
        self._run_flag = True
        downscaleColor = True
        fps = 60
        # The disparity is computed at this resolution, then upscaled to RGB resolution
        monoResolution = dai.MonoCameraProperties.SensorResolution.THE_720_P

        # Create pipeline
        pipeline = dai.Pipeline()
        queueNames = []

        # Define sources and outputs
        camRgb = pipeline.create(dai.node.ColorCamera)
        left = pipeline.create(dai.node.MonoCamera)
        right = pipeline.create(dai.node.MonoCamera)
        stereo = pipeline.create(dai.node.StereoDepth)

        rgbOut = pipeline.create(dai.node.XLinkOut)
        disparityOut = pipeline.create(dai.node.XLinkOut)

        rgbOut.setStreamName("rgb")
        queueNames.append("rgb")
        disparityOut.setStreamName("disp")
        queueNames.append("disp")

        # Properties
        camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        camRgb.setFps(fps)
        if downscaleColor:
            camRgb.setIspScale(2, 3)
        # For now, RGB needs fixed focus to properly align with depth.
        # This value was used during calibration
        camRgb.initialControl.setManualFocus(130)

        left.setResolution(monoResolution)
        left.setBoardSocket(dai.CameraBoardSocket.LEFT)
        left.setFps(fps)
        right.setResolution(monoResolution)
        right.setBoardSocket(dai.CameraBoardSocket.RIGHT)
        right.setFps(fps)

        stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
        # LR-check is required for depth alignment
        stereo.setLeftRightCheck(True)
        stereo.setDepthAlign(dai.CameraBoardSocket.RGB)

        # Linking
        camRgb.isp.link(rgbOut.input)
        left.out.link(stereo.left)
        right.out.link(stereo.right)
        stereo.disparity.link(disparityOut.input)

        counter = 1
        count = 0
        # ----------- video writer ________________________________________________________________
        file_name = os.path.join(self.video_path, 'raw_video{}.mp4'.format(self._get_ymd()))
        file_name2 = os.path.join(self.video_path, 'detected_video{}.mp4'.format(self._get_ymd()))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter(
            file_name, fourcc,
            fps, (1280, 720)
        )
        self.video_writer_detected = cv2.VideoWriter(
            file_name2
            , fourcc, fps,
            (1280, 720)
        )

        # Connect to device and start pipeline
        with dai.Device(pipeline) as device:

            frameRgb = None
            frameDisp = None

            # Configure windows; trackbar adjusts blending ratio of rgb/depth
            rgbWindowName = "rgb"
            depthWindowName = "depth"

            while self._run_flag:
                latestPacket = {}
                latestPacket["rgb"] = None
                latestPacket["disp"] = None

                queueEvents = device.getQueueEvents(("rgb", "disp"))
                for queueName in queueEvents:
                    packets = device.getOutputQueue(queueName).tryGetAll()
                    if len(packets) > 0:
                        latestPacket[queueName] = packets[-1]

                if latestPacket["rgb"] is not None:
                    frameRgb = latestPacket["rgb"].getCvFrame()
                    # frameRgb = cv2.rectangle(frameRgb, (100, 100), (150, 150), (0, 0, 255), thickness=2)
                    # frameRgb = cv2.resize(frameRgb, (640, 480))
                    # cv2.imshow(rgbWindowName, frameRgb)

                if latestPacket["disp"] is not None:
                    frameDisp = latestPacket["disp"].getFrame()

                    # crop = frameDisp[100:150, 100:150]
                    # average = np.average(crop)
                    # print(f'frameDisp={average}\n--------------------')
                    # Optional, extend range 0..95 -> 0..255, for a better visualisation

                    # cv2.imshow(depthWindowName, frameDisp)
                if counter >= count:
                    count += 1
                    continue
                count = 0
                # if latestPacket["rgb"] is not None and latestPacket["rgb"] is not None:
                if frameRgb is not None and frameDisp is not None:
                    ############# testing ####################
                    # cv2.imshow('frameRgb', frameRgb)
                    # cv2.imshow('frameDisp', frameDisp)
                    # if cv2.waitKey(1) == ord('q'):
                    #     break
                    ############# end testing ###################

                    frame = cv2.merge((frameRgb, frameDisp))

                    image, item_sorted, class_sorted = self.detector.detect(frame)
                    if self.save_video:
                        self.video_writer.write(frameRgb)
                        self.video_writer_detected.write(image)
                    self.change_pixmap_signal.emit(image, item_sorted, class_sorted)
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