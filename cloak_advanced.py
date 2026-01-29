"""
Advanced Invisibility Cloak with Multiple Effects
Features: Multiple cloaks, transparency control, special effects
"""

import cv2
import numpy as np
import time
import argparse

COLOR_RANGES = {
    'red': [(np.array([0, 120, 70]), np.array([10, 255, 255])),
            (np.array([170, 120, 70]), np.array([180, 255, 255]))],
    'blue': [(np.array([94, 80, 2]), np.array([126, 255, 255]))],
    'green': [(np.array([40, 40, 40]), np.array([80, 255, 255]))],
    'yellow': [(np.array([20, 100, 100]), np.array([30, 255, 255]))],
}

print("""
🎭 Advanced Invisibility Cloak
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Features:
✨ Multiple color detection simultaneously
✨ Adjustable transparency (0-100%)
✨ Special effects (blur, pixelate, rainbow)
✨ Real-time color switching

Controls:
q - Quit
1-5 - Change transparency (20%, 40%, 60%, 80%, 100%)
r - Reset background
e - Cycle effects
c - Toggle color detection
s - Save screenshot

Initializing...
""")

parser = argparse.ArgumentParser()
parser.add_argument('--camera', type=int, default=0)
parser.add_argument('--colors', nargs='+', default=['red'], 
                    choices=['red', 'blue', 'green', 'yellow'],
                    help='Colors to detect (can specify multiple)')
args = parser.parse_args()

cap = cv2.VideoCapture(args.camera)

if not cap.isOpened():
    print("❌ Error: Could not open camera")
    exit(1)

print("⏳ Capturing background in 3 seconds...")
time.sleep(3)

background = None
for i in range(30):
    ret, background = cap.read()
background = cv2.flip(background, 1)

print("✅ Background captured!\n")

# Effect settings
transparency = 1.0
effect_mode = 0  # 0: normal, 1: blur, 2: pixelate, 3: rainbow
active_colors = args.colors
all_colors = list(COLOR_RANGES.keys())

def apply_effect(img, mode):
    """Apply special effects to the cloak area"""
    if mode == 1:  # Blur
        return cv2.GaussianBlur(img, (21, 21), 0)
    elif mode == 2:  # Pixelate
        h, w = img.shape[:2]
        temp = cv2.resize(img, (w//10, h//10), interpolation=cv2.INTER_LINEAR)
        return cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)
    elif mode == 3:  # Rainbow
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = (hsv[:, :, 0] + int(time.time() * 50) % 180) % 180
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return img

frame_count = 0
start_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Detect multiple colors
    combined_mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    
    for color in active_colors:
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        for lower, upper in COLOR_RANGES[color]:
            mask = cv2.bitwise_or(mask, cv2.inRange(hsv, lower, upper))
        combined_mask = cv2.bitwise_or(combined_mask, mask)
    
    # Noise removal
    kernel = np.ones((5, 5), np.uint8)
    combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel, iterations=2)
    combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    combined_mask = cv2.GaussianBlur(combined_mask, (7, 7), 0)
    
    mask_inv = cv2.bitwise_not(combined_mask)
    
    # Apply effect to background
    effect_background = apply_effect(background.copy(), effect_mode)
    
    # Create cloak effect with transparency
    res1 = cv2.bitwise_and(effect_background, effect_background, mask=combined_mask)
    res2 = cv2.bitwise_and(frame, frame, mask=mask_inv)
    
    # Blend with transparency
    mask_3ch = cv2.cvtColor(combined_mask, cv2.COLOR_GRAY2BGR) / 255.0
    final_output = (res1 * mask_3ch * transparency + 
                   frame * mask_3ch * (1 - transparency) +
                   res2).astype(np.uint8)
    
    # Calculate FPS
    frame_count += 1
    if frame_count % 30 == 0:
        fps = 30 / (time.time() - start_time)
        start_time = time.time()
    
    # UI overlays
    effects = ['Normal', 'Blur', 'Pixelate', 'Rainbow']
    cv2.putText(final_output, f"Colors: {', '.join(active_colors)}", 
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(final_output, f"Transparency: {int(transparency * 100)}%", 
                (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(final_output, f"Effect: {effects[effect_mode]}", 
                (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(final_output, f"FPS: {int(fps) if frame_count > 30 else 0}", 
                (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    # Instructions
    help_text = "1-5:Trans | E:Effect | C:Colors | R:Reset | S:Save | Q:Quit"
    cv2.putText(final_output, help_text, (10, frame.shape[0] - 20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    cv2.imshow("🎭 Advanced Invisibility Cloak", final_output)
    cv2.imshow("🎨 Mask (All Colors)", combined_mask)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('1'):
        transparency = 0.2
    elif key == ord('2'):
        transparency = 0.4
    elif key == ord('3'):
        transparency = 0.6
    elif key == ord('4'):
        transparency = 0.8
    elif key == ord('5'):
        transparency = 1.0
    elif key == ord('e'):
        effect_mode = (effect_mode + 1) % 4
        print(f"Effect: {effects[effect_mode]}")
    elif key == ord('c'):
        # Cycle through colors
        current_idx = all_colors.index(active_colors[0]) if active_colors else 0
        next_color = all_colors[(current_idx + 1) % len(all_colors)]
        active_colors = [next_color]
        print(f"Detecting: {next_color}")
    elif key == ord('r'):
        print("📸 Recapturing background...")
        for i in range(30):
            ret, background = cap.read()
        background = cv2.flip(background, 1)
        print("✅ Background updated!")
    elif key == ord('s'):
        filename = f"cloak_advanced_{int(time.time())}.jpg"
        cv2.imwrite(filename, final_output)
        print(f"💾 Screenshot saved: {filename}")

print("\n✨ Thanks for using Advanced Invisibility Cloak!")
cap.release()
cv2.destroyAllWindows()
