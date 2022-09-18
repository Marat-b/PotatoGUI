import array

from PyQt5 import QtCore
from PyQt5.QtCore import QThread
import numpy as np
import cv2
import depthai as dai

from depth.main_stream_depth import Detector


class VideoThread(QThread):
    change_pixmap_signal = QtCore.pyqtSignal(np.ndarray, dict, dict)

    def __init__(self):
        super(VideoThread, self).__init__()
        self._run_flag = True
        self.detector = Detector()

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

        # Connect to device and start pipeline
        with dai.Device(pipeline) as device:

            frameRgb = None
            frameDisp = None

            # Configure windows; trackbar adjusts blending ratio of rgb/depth
            rgbWindowName = "rgb"
            depthWindowName = "depth"

            while True:
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
                if latestPacket["rgb"] is not None and latestPacket["rgb"] is not None:
                    ############# testing ####################
                    # cv2.imshow('frameRgb', frameRgb)
                    # cv2.imshow('frameDisp', frameDisp)
                    # if cv2.waitKey(1) == ord('q'):
                    #     break
                    ############# end testing ###################

                    frame = cv2.merge((frameRgb, frameDisp))

                    image, item_sorted, class_sorted = self.detector.detect(frame)
                    self.change_pixmap_signal.emit(image, item_sorted, class_sorted)


    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False