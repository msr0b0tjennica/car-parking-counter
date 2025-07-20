from .video_file import VideoFileSource
from .webcam import WebcamSource
from .rtsp_stream import RTSPStreamSource


def create_video_source(input_arg):
    if input_arg is None:
        return WebcamSource()
    elif input_arg.startswith("rtsp://"):
        return RTSPStreamSource(input_arg)
    else:
        return VideoFileSource(input_arg)