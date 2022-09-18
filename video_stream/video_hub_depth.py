# to start together with video_sender.py
import cv2
from video_stream.video_stream_subscriber_depth import VideoStreamSubscriber


senders = ['127.0.0.1:5555', '127.0.0.1:5556']

receivers = [VideoStreamSubscriber(host) for host in senders]

while True:
    for receiver in receivers:
        # print('before receiver - get frame')
        window_name, frame = receiver.receive()
        # print('after receiver - get frame')
        if frame is not None:
            image = frame.copy()
            image = cv2.resize(image, (640, 360))
            cv2.imshow(window_name, image)
            cv2.waitKey(1)
        # else:
        #     cv2.destroyWindow(window_name)
