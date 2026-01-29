"""
AI-Enhanced Invisibility Cloak using MediaPipe
Uses person segmentation for more accurate cloak detection
"""

import cv2
import numpy as np
import mediapipe as mp
import time
import argparse

print("""
🤖 AI-Enhanced Invisibility Cloak
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Using MediaPipe Selfie Segmentation for precise detection
This method doesn't require specific colored cloth!

Features:
✨ No specific color cloth needed
✨ Better edge detection
✨ Works with any background
✨ AI-powered segmentation

Press 'q' to quit
Press 's' to save screenshot
Press 'r' to recapture background

Initializing AI model...
""")

parser = argparse.ArgumentParser(description='AI-Enhanced Invisibility Cloak')
parser.add_argument('--camera', type=int, default=0, help='Camera index')
parser.add_argument('--model', type=int, default=1, choices=[0, 1], 
                    help='Segmentation model: 0=general, 1=landscape (better for full body)')
args = parser.parse_args()

# Initialize MediaPipe
mp_selfie_segmentation = mp.solutions.selfie_segmentation
segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=args.model)

cap = cv2.VideoCapture(args.camera)

if not cap.isOpened():
    print("❌ Error: Could not open camera")
    exit(1)

print("✅ AI Model loaded successfully!")
print("⏳ Capturing background in 3 seconds... STAY OUT OF FRAME!")
time.sleep(3)

# Capture background
background = None
for i in range(30):
    ret, background = cap.read()
background = cv2.flip(background, 1)

print("✅ Background captured!\n")
print("📌 Now enter frame - You'll become invisible!")

# Effect modes
effect_mode = 0  # 0: invisible, 1: ghost, 2: outline
transparency = 0.8

frame_count = 0
start_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    
    # AI Segmentation
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = segmentation.process(rgb_frame)
    
    # Create mask from segmentation
    condition = results.segmentation_mask > 0.5
    mask = condition.astype(np.uint8) * 255
    
    # Smooth edges
    mask = cv2.GaussianBlur(mask, (7, 7), 0)
    
    if effect_mode == 0:
        # Full invisibility
        mask_inv = cv2.bitwise_not(mask)
        res1 = cv2.bitwise_and(background, background, mask=mask)
        res2 = cv2.bitwise_and(frame, frame, mask=mask_inv)
        final_output = cv2.add(res1, res2)
        
    elif effect_mode == 1:
        # Ghost effect (semi-transparent)
        mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) / 255.0
        blended = (background * mask_3ch * transparency + 
                  frame * mask_3ch * (1 - transparency) +
                  frame * (1 - mask_3ch))
        final_output = blended.astype(np.uint8)
        
    elif effect_mode == 2:
        # Outline effect
        edges = cv2.Canny(mask, 100, 200)
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        edges_colored[:, :, 0] = 0  # Remove blue
        edges_colored[:, :, 1] = edges  # Green outline
        final_output = cv2.addWeighted(frame, 0.7, edges_colored, 0.3, 0)
    
    # Calculate FPS
    frame_count += 1
    if frame_count % 30 == 0:
        fps = 30 / (time.time() - start_time)
        start_time = time.time()
        
    # UI overlays
    cv2.putText(final_output, f"AI Mode: {['Invisible', 'Ghost', 'Outline'][effect_mode]}", 
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(final_output, f"FPS: {int(fps) if frame_count > 30 else 0}", 
                (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(final_output, "Press: q=quit | 1,2,3=modes | r=reset bg | s=save", 
                (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    cv2.imshow("🤖 AI Invisibility Cloak", final_output)
    cv2.imshow("🎭 Segmentation Mask", mask)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('1'):
        effect_mode = 0
    elif key == ord('2'):
        effect_mode = 1
    elif key == ord('3'):
        effect_mode = 2
    elif key == ord('r'):
        print("📸 Recapturing background...")
        for i in range(30):
            ret, background = cap.read()
        background = cv2.flip(background, 1)
        print("✅ Background updated!")
    elif key == ord('s'):
        filename = f"cloak_ai_{int(time.time())}.jpg"
        cv2.imwrite(filename, final_output)
        print(f"💾 Screenshot saved: {filename}")

print("\n✨ Thank you for using AI Invisibility Cloak!")
cap.release()
cv2.destroyAllWindows()
segmentation.close()
