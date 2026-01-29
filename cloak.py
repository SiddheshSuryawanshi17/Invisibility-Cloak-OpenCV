import cv2
import numpy as np
import time
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser(description='Invisibility Cloak with OpenCV')
parser.add_argument('--color', type=str, default='red', choices=['red', 'blue', 'green'],
                    help='Color of the cloak (default: red)')
parser.add_argument('--camera', type=int, default=0, help='Camera index (default: 0)')
args = parser.parse_args()

# Color ranges in HSV
COLOR_RANGES = {
    'red': [(np.array([0, 120, 70]), np.array([10, 255, 255])),
            (np.array([170, 120, 70]), np.array([180, 255, 255]))],
    'blue': [(np.array([94, 80, 2]), np.array([126, 255, 255]))],
    'green': [(np.array([40, 40, 40]), np.array([80, 255, 255]))]
}

print(f"""
🧙 Harry Potter's Invisibility Cloak
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Selected Color: {args.color.upper()}
Camera Index: {args.camera}

📌 Instructions:
1. Stay OUT of frame for 3 seconds
2. Background will be captured automatically
3. Use a {args.color} colored cloth
4. Press 'q' to quit

Initializing camera...
""")

# Capture from webcam
cap = cv2.VideoCapture(args.camera)

if not cap.isOpened():
    print("❌ Error: Could not open camera. Check if it's being used by another app.")
    exit(1)

print("✅ Camera opened successfully!")
print("⏳ Capturing background in 3 seconds... STAY OUT OF FRAME!")
time.sleep(3)

# Capture background (30 frames for smoothness)
background = None
for i in range(30):
    ret, background = cap.read()
    if not ret:
        print("❌ Error: Failed to capture background.")
        exit(1)
        
background = np.flip(background, axis=1)
print("✅ Background captured! You can now enter the frame.\n")

frame_count = 0
start_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("❌ Error: Failed to grab frame from webcam.")
        break

    frame = np.flip(frame, axis=1)
    
    # Calculate FPS
    frame_count += 1
    if frame_count % 30 == 0:
        fps = 30 / (time.time() - start_time)
        start_time = time.time()

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create mask for selected color
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    for lower, upper in COLOR_RANGES[args.color]:
        mask = cv2.bitwise_or(mask, cv2.inRange(hsv, lower, upper))

    # ✅ Noise removal (important)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=2)

    # Inverse mask
    mask_inv = cv2.bitwise_not(mask)

    # Cloak effect
    res1 = cv2.bitwise_and(background, background, mask=mask)
    res2 = cv2.bitwise_and(frame, frame, mask=mask_inv)
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)
    
    # Add instructions overlay
    cv2.putText(final_output, "Press 'q' to quit", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(final_output, f"Color: {args.color.upper()}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Show outputs
    cv2.imshow("🧙 Invisibility Cloak", final_output)
    cv2.imshow("🎭 Mask Debug (White = Detected)", mask)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("\n✨ Thank you for using the Invisibility Cloak!")
cap.release()
cv2.destroyAllWindows()
