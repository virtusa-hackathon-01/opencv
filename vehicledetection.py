import cv2
import numpy as np

# Constants (adjust as needed)
MINIMUM_RECTANGLE_WIDTH = 80
MINIMUM_RECTANGLE_HEIGHT = 80
OFFSET_ERROR = 6
COUNTING_LINE_POSITION = 550

# Variables for detection and counting
detected_objects = []
car_count = 0

def get_center(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy

# Open default webcam (use '0' for other cameras)
cap = cv2.VideoCapture("C:\\Users\\welcome\\Downloads\\video.mp4")

# Create background subtractor
background_subtractor = cv2.createBackgroundSubtractorMOG2()

while True:
    ret, frame = cap.read()

    # Process the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 5)
    foreground_mask = background_subtractor.apply(blur)
    dilated = cv2.dilate(foreground_mask, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Find contours
    contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw counting line
    cv2.line(frame, (25, COUNTING_LINE_POSITION), (1200, COUNTING_LINE_POSITION), (255, 127, 0), 3)

    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)

        # Validate contour size
        if w < MINIMUM_RECTANGLE_WIDTH or h < MINIMUM_RECTANGLE_HEIGHT:
            continue

        # Draw rectangle and center
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        center = get_center(x, y, w, h)
        detected_objects.append(center)
        cv2.circle(frame, center, 4, (0, 0, 255), -1)

        # Check for crossing the counting line
        for center_x, center_y in detected_objects:
            if center_y < (COUNTING_LINE_POSITION + OFFSET_ERROR) and center_y > (COUNTING_LINE_POSITION - OFFSET_ERROR):
                car_count += 1
                cv2.line(frame, (25, COUNTING_LINE_POSITION), (1200, COUNTING_LINE_POSITION), (0, 127, 255), 3)
                detected_objects.remove((center_x, center_y))
                print("Car detected: " + str(car_count))

    # Display text and frame
    cv2.putText(frame, "VEHICLE COUNT : " + str(car_count), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    cv2.imshow("Vehicle Detection", frame)

    if cv2.waitKey(1) == 27:  # Exit on ESC
        break

# Release resources
cv2.destroyAllWindows()
cap.release()