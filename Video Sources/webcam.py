import cv2
from .base import BaseVideoSource

class WebcamSource(BaseVideoSource):
    def __init__(self):
        self.cap = None

    def open(self):
        self.cap = cv2.VideoCapture(0)
        return self.cap.isOpened()

    def read(self):
        return self.cap.read()

    def release(self):
        self.cap.release()