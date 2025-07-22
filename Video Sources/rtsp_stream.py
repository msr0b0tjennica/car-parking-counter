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
        if self.cap is not None:
            return self.cap.read()
        else:
            raise RuntimeError("Video stream not opened. Call open() first.")
           

    def release(self):
        if self.cap is not None:
            self.cap.release()
