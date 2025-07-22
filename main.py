import cv2
import pickle
import cvzone # type: ignore
import numpy as np
import sys

from tkinter import Tk, filedialog

from config_loader import load_config

config = load_config()

# Parking configuration
PARKING_SPOT_WIDTH     = config["parking"]["spot_width"]
PARKING_SPOT_HEIGHT    = config["parking"]["spot_height"]
OCCUPIED_THRESHOLD     = config["parking"]["occupied_threshold"]

# Preprocessing parameters
GAUSSIAN_BLUR_KERNEL   = tuple(config["preprocessing"]["gaussian_blur_kernel"])
ADAPTIVE_THRESH_BLOCK_SIZE = config["preprocessing"]["adaptive_thresh_block_size"]
ADAPTIVE_THRESH_CONSTANT   = config["preprocessing"]["adaptive_thresh_constant"]

# # Image adjustment
# BRIGHTNESS = config["adjustment"]["brightness"]
# CONTRAST   = config["adjustment"]["contrast"]


def load_parking_positions(filename):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except (FileNotFoundError, pickle.PickleError) as e:
        print(f"Error loading parking positions: {e}")
        return []

def process_image_for_detection(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, GAUSSIAN_BLUR_KERNEL, 1)
    img_thresh = cv2.adaptiveThreshold(
        img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, ADAPTIVE_THRESH_BLOCK_SIZE, ADAPTIVE_THRESH_CONSTANT
    )
    img_median = cv2.medianBlur(img_thresh, 5)
    kernel = np.ones((3, 3), np.uint8)
    return cv2.dilate(img_median, kernel, iterations=1)

def check_parking_space(img_pro, img_display, pos_list):
    space_counter = 0

    for x, y in pos_list:
        img_crop = img_pro[y:y + PARKING_SPOT_HEIGHT, x:x + PARKING_SPOT_WIDTH]
        count = cv2.countNonZero(img_crop)

        if count < OCCUPIED_THRESHOLD:
            color = (0, 255, 0)
            thickness = 3
            space_counter += 1
        else:
            color = (0, 0, 255)
            thickness = 1

        cv2.rectangle(img_display, (x, y), (x + PARKING_SPOT_WIDTH, y + PARKING_SPOT_HEIGHT), color, thickness)

    cvzone.putTextRect(
        img_display, f'Free: {space_counter}/{len(pos_list)}',
        (30, 50), scale=2, thickness=3, offset=20, colorR=(0, 200, 0)
    )


def main():

    # Open a file dialog to select a video file
    Tk().withdraw()  # Hide the root Tk window
    input_source = filedialog.askopenfilename(
    title="Select Video File",
    filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv"), ("All files", "*.*")])

    # If the user cancels, fall back to webcam
    if input_source == "":
        print("No file selected. Using webcam instead.")
        input_source = 0

    video_source = cv2.VideoCapture(input_source)
    
    if not video_source.isOpened():
        print("Error: Could not open video source")
        return
    
    def nothing(x):
        pass
    cv2.namedWindow("Adjustments")
    cv2.createTrackbar("Brightness", "Adjustments", 30, 100, nothing)  # Default: 30
    cv2.createTrackbar("Contrast", "Adjustments", 10, 30, nothing)     # Default: 10 (represents 1.0)

    pos_list = load_parking_positions('CarParkPos')
    if not pos_list:
        print("Error: No parking positions loaded")
        return
    
    previous_frame = None

    while True:
        success, img = video_source.read()
        if not success:
            print("⚠️ Frame failed to load — using previous frame")
            if previous_frame is None:
                print("❌ No previous frame to fall back on. Skipping video.")
                break
            img = previous_frame.copy()
        else:
            previous_frame = img.copy()

        # 🧪Read trackbar values
        brightness = cv2.getTrackbarPos("Brightness", "Adjustments")
        contrast_raw = cv2.getTrackbarPos("Contrast", "Adjustments")
        contrast = contrast_raw / 10.0  # Convert 10 → 1.0, 15 → 1.5, etc.

        # Adjust brightness and contrast
        img = cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)

        processed_img = process_image_for_detection(img)
        check_parking_space(processed_img, img, pos_list)

        cv2.imshow("Parking Space Detection", img)
        if cv2.waitKey(20) == ord('q'):
            break

    video_source.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
