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
        return self.cap.read()

    def release(self):
        self.cap.release()