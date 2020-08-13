import cv2

from mask_detection.mask_detect import mask_detect

CONFIDENCE = 0.5


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, image = self.video.read()

        # DO WHAT YOU WANT WITH TENSORFLOW / KERAS AND OPENCV

        if ret:
            image = mask_detect(image)

        ret, jpeg = cv2.imencode('.jpg', image)

        return jpeg.tobytes()
