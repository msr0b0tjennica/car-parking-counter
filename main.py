import cv2
import pickle
import cvzone
import numpy as np
import sys

# Constants
PARKING_SPOT_WIDTH = 107
PARKING_SPOT_HEIGHT = 48
OCCUPIED_THRESHOLD = 900
GAUSSIAN_BLUR_KERNEL = (3, 3)
ADAPTIVE_THRESH_BLOCK_SIZE = 25
ADAPTIVE_THRESH_CONSTANT = 16

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
    input_source = sys.argv[1] if len(sys.argv) > 1 else 0
    cap = cv2.VideoCapture(input_source)
    
    if not cap.isOpened():
        print("Error: Could not open video source")
        return

    pos_list = load_parking_positions('CarParkPos')
    if not pos_list:
        print("Error: No parking positions loaded")
        return

    while True:
        success, img = cap.read()
        if not success:
            break  # Or handle retries more robustly

        processed_img = process_image_for_detection(img)
        check_parking_space(processed_img, img, pos_list)

        cv2.imshow("Parking Space Detection", img)
        if cv2.waitKey(20) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
