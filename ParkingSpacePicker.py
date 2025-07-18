import cv2 # type: ignore
import pickle

# Load image
image = cv2.imread('carParkImg.png')  # Make sure the image is named like this
width, height = 107, 48  # Size of each parking space box
positions = []

try:
    with open('CarParkPos', 'rb') as f:
        positions = pickle.load(f)
except:
    positions = []

# Draw rectangles on the image for each parking space
def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        positions.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(positions):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                positions.pop(i)
                break
    with open('CarParkPos', 'wb') as f:
        pickle.dump(positions, f)

while True:
    img = image.copy()
    for pos in positions:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    key = cv2.waitKey(1)

    if key == ord('s'):
        with open('CarParkPos', 'wb') as f:
            pickle.dump(positions, f)
        break

cv2.destroyAllWindows()        