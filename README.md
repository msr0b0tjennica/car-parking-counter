# Car Parking Space Counter 

This is a simple parking space detection system built using OpenCV in Python. It detects free and occupied parking spots from a video file, webcam, or live RTSP stream using classical image processing techniques — no deep learning required.

## Features

- Detects occupied and free parking spots in real-time
- Supports video files, RTSP streams, and webcam feed
- Green boxes indicate available spots, red boxes indicate occupied spots
- Saves parking spot positions in a pickle file for reuse
- Lightweight and fast (runs on CPU)

## Files

| File                   | Description                                           |
|------------------------|-------------------------------------------------------|
| main.py                | Main detection script                                 |
| ParkingSpacePicker.py  | Used to manually mark the parking spots               |
| CarParkPos             | Pickle file storing the marked spot positions         |
| carPark.mp4            | Sample video file                                     |
| carParkImg.png         | Sample top-down image used for initial marking        |

## How to Run

### 1. Mark Parking Spaces

Run the picker script to manually mark parking slots using the image:

```bash
python ParkingSpacePicker.py
```

- Left-click to add a rectangle  
- Right-click to remove one  
- Press S to save positions to CarParkPos

### 2. Start Detection

Run main.py with a video source of your choice:

- From webcam (default):
```bash
python main.py
```

- From a video file:
```bash
python main.py carPark.mp4
```

- From an RTSP stream:
```bash
python main.py rtsp://username:password@ip_address/stream_path
```

## How It Works

- Applies grayscale, blur, adaptive thresholding, and dilation
- Crops each marked parking spot area and counts non-zero pixels
- If the pixel count is below a threshold, the space is marked as empty
- Results are overlaid on the video frame in real-time

## Requirements

- Python 3.6+
- OpenCV
- Numpy
- cvzone

Install dependencies:

```bash
pip install opencv-python numpy cvzone
```
