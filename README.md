# Car Parking Space Counter 

This is a simple car parking space detection system built using OpenCV in Python.

## Features
- Detects occupied and free parking spots in a video
- Marks green boxes for available spaces and red for occupied
- Uses only basic image processing (no deep learning)

## Files
- `main.py`: Main detection logic
- `ParkingSpacePicker.py`: Manually mark the parking spaces
- `CarParkPos`: Stores marked positions (pickle file)
- `carPark.mp4` and `carParkImg.png`: Sample video and image

## How to Run
1. Run `ParkingSpacePicker.py` to mark spots
2. Edit the line in `main.py` that opens the video stream:
   ```python
   cap = cv2.VideoCapture("carPark.mp4")  # or use an RTSP stream like: "rtsp://username:password@ip_address/..."
