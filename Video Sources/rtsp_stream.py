import cv2
from .base import BaseVideoSource

class RTSPStreamSource(BaseVideoSource):
    def __init__(self, url):
        self.url = url
        self.cap = None

    def open(self):
        self.cap = cv2.VideoCapture(self.url)
        return self.cap.isOpened()

    def read(self):
        return self.cap.read()

    def release(self):
        self.cap.release()
