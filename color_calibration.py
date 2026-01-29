"""
Color Calibration Tool for Invisibility Cloak
Use this to find optimal HSV values for your cloth color
"""

import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)

# Create window with trackbars
cv2.namedWindow('HSV Calibration')
cv2.createTrackbar('H Lower', 'HSV Calibration', 0, 179, nothing)
cv2.createTrackbar('H Upper', 'HSV Calibration', 179, 179, nothing)
cv2.createTrackbar('S Lower', 'HSV Calibration', 120, 255, nothing)
cv2.createTrackbar('S Upper', 'HSV Calibration', 255, 255, nothing)
cv2.createTrackbar('V Lower', 'HSV Calibration', 70, 255, nothing)
cv2.createTrackbar('V Upper', 'HSV Calibration', 255, 255, nothing)

print("🎨 HSV Color Calibration Tool")
print("📌 Instructions:")
print("1. Hold your colored cloth in front of camera")
print("2. Adjust trackbars until cloth is WHITE in mask window")
print("3. Note down the HSV values shown in terminal")
print("4. Press 'q' to quit\n")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Get trackbar values
    h_lower = cv2.getTrackbarPos('H Lower', 'HSV Calibration')
    h_upper = cv2.getTrackbarPos('H Upper', 'HSV Calibration')
    s_lower = cv2.getTrackbarPos('S Lower', 'HSV Calibration')
    s_upper = cv2.getTrackbarPos('S Upper', 'HSV Calibration')
    v_lower = cv2.getTrackbarPos('V Lower', 'HSV Calibration')
    v_upper = cv2.getTrackbarPos('V Upper', 'HSV Calibration')
    
    # Create mask
    lower = np.array([h_lower, s_lower, v_lower])
    upper = np.array([h_upper, s_upper, v_upper])
    mask = cv2.inRange(hsv, lower, upper)
    
    # Apply mask
    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    # Display values on frame
    text = f"HSV: [{h_lower},{s_lower},{v_lower}] - [{h_upper},{s_upper},{v_upper}]"
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    cv2.imshow('Original', frame)
    cv2.imshow('Mask', mask)
    cv2.imshow('Result', result)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(f"\n✅ Final HSV Values:")
        print(f"Lower: [{h_lower}, {s_lower}, {v_lower}]")
        print(f"Upper: [{h_upper}, {s_upper}, {v_upper}]")
        break

cap.release()
cv2.destroyAllWindows()
