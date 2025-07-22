import cv2
from .base import BaseVideoSource

class VideoFileSource(BaseVideoSource):
    def __init__(self, filepath):
        self.filepath = filepath
        self.cap = None

    def open(self):
        self.cap = cv2.VideoCapture(self.filepath)
        return self.cap.isOpened()

    def read(self):
        if self.cap is not None:
            return self.cap.read()
        else:
            raise RuntimeError("Video stream not opened. Call open() first.")
           

    def release(self):
        if self.cap is not None:
            self.cap.release()
