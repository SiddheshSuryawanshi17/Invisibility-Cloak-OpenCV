import cv2
import numpy as np
import time
import argparse
from datetime import datetime

def get_color_range(color):
    """Returns HSV color ranges for different colors"""
    colors = {
        'red': {
            'lower1': np.array([0, 120, 70]),
            'upper1': np.array([10, 255, 255]),
            'lower2': np.array([170, 120, 70]),
            'upper2': np.array([180, 255, 255])
        },
        'blue': {
            'lower1': np.array([94, 80, 2]),
            'upper1': np.array([126, 255, 255]),
            'lower2': None,
            'upper2': None
        },
        'green': {
            'lower1': np.array([35, 80, 50]),
            'upper1': np.array([85, 255, 255]),
            'lower2': None,
            'upper2': None
        }
    }
    return colors.get(color.lower(), colors['red'])

def main():
    parser = argparse.ArgumentParser(description='Invisibility Cloak using OpenCV')
    parser.add_argument('--color', type=str, default='red', choices=['red', 'blue', 'green'],
                        help='Color of the cloak (default: red)')
    parser.add_argument('--record', action='store_true', help='Record the output video')
    parser.add_argument('--no-debug', action='store_true', help='Hide the mask debug window')
    args = parser.parse_args()

    print(f"""
╔═══════════════════════════════════════════════════════════╗
║  🧙 Harry Potter's Invisibility Cloak - OpenCV Edition   ║
╚═══════════════════════════════════════════════════════════╝

Harry: Hey! Would you like to try my invisibility cloak?
       It's awesome!!

Settings:
  🎨 Cloak Color: {args.color.upper()}
  🎥 Recording: {'ON' if args.record else 'OFF'}
  
📋 Controls:
  • Press 'Q' to quit
  • Press 'R' to recapture background
  • Press 'SPACE' to toggle mask debug view
  
Prepare to get invisible in 3 seconds...
""")

    # Capture from webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open webcam!")
        print("   Check if your camera is connected and not being used by another app.")
        return
    
    time.sleep(3)

    # Get video properties for recording
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 20
    
    # Setup video writer if recording
    video_writer = None
    if args.record:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"invisibility_cloak_{timestamp}.avi"
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_writer = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))
        print(f"🎥 Recording to: {output_file}")

    # Capture background
    def capture_background():
        print("📸 Capturing background... Stay out of frame!")
        time.sleep(2)
        bg = None
        for i in range(30):
            ret, frame = cap.read()
            if not ret:
                print("❌ Error: Failed to grab frame from webcam. Check camera permissions!")
                print("   macOS: System Settings → Privacy & Security → Camera → Add Terminal/IDE")
                cap.release()
                exit()
            bg = frame
            print(f"  Progress: {i+1}/30", end='\r')
        print("\n✅ Background captured! Now put on your cloak!")
        return np.flip(bg, axis=1)

    background = capture_background()
    color_range = get_color_range(args.color)
    show_debug = not args.no_debug

    print("\n🎬 Starting invisibility effect...\n")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("❌ Error: Failed to grab frame from webcam.")
            break

        frame = np.flip(frame, axis=1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create mask for selected color
        mask1 = cv2.inRange(hsv, color_range['lower1'], color_range['upper1'])
        if color_range['lower2'] is not None:
            mask2 = cv2.inRange(hsv, color_range['lower2'], color_range['upper2'])
            mask = mask1 + mask2
        else:
            mask = mask1

        # Noise removal
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
        mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=2)
        mask = cv2.GaussianBlur(mask, (5, 5), 0)

        # Inverse mask
        mask_inv = cv2.bitwise_not(mask)

        # Cloak effect
        res1 = cv2.bitwise_and(background, background, mask=mask)
        res2 = cv2.bitwise_and(frame, frame, mask=mask_inv)
        final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

        # Add UI overlay
        cv2.putText(final_output, f"Cloak: {args.color.upper()}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(final_output, "Press 'Q' to quit | 'R' to reset BG | SPACE for debug", 
                    (10, frame_height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        if args.record:
            cv2.circle(final_output, (frame_width - 30, 30), 8, (0, 0, 255), -1)
            cv2.putText(final_output, "REC", (frame_width - 60, 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Show outputs
        cv2.imshow("🧙 Invisibility Cloak", final_output)
        if show_debug:
            cv2.imshow("🎭 Mask Debug (White = Detected)", mask)

        # Record frame
        if video_writer is not None:
            video_writer.write(final_output)

        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            background = capture_background()
        elif key == ord(' '):
            show_debug = not show_debug
            if not show_debug:
                cv2.destroyWindow("🎭 Mask Debug (White = Detected)")

    # Cleanup
    cap.release()
    if video_writer is not None:
        video_writer.release()
        print(f"\n✅ Video saved: {output_file}")
    cv2.destroyAllWindows()
    print("\n👋 Thanks for using the Invisibility Cloak! Mischief Managed!")

if __name__ == "__main__":
    main()
