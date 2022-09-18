import cv2
import numpy as np
import depthai as dai
from multiprocessing import Process, Queue
# import izmq
import simplejpeg

# sender = izmq.VideoSender(connect_to='tcp://127.0.0.1:5555', REQ_REP=False)
from depth.main_stream_depth import Detector

detector = Detector()
# Optional. If set (True), the ColorCamera is downscaled from 1080p to 720p.
# Otherwise (False), the aligned depth is automatically upscaled to 1080p
downscaleColor = True
fps = 30
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

counter = 15
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
            detected_image = detector.detect(frame)
            cv2.imshow('detected_image', detected_image)
            if cv2.waitKey(1) == ord('q'):
                break
            # buffer = cv2.imencode('.png', frame)[1]
            # # print('send buffer')
            # sender.send_image('oak', buffer)
            # print(f'frame.shape={frame.shape}')
                    # cv2.imshow('frame', frame)
