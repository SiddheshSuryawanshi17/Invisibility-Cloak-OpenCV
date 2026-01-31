"""
Configuration file for Invisibility Cloak
Adjust these values to fine-tune detection for your environment
"""

# Color Detection Settings (HSV ranges)
COLOR_RANGES = {
    'red': {
        'lower1': [0, 120, 70],      # Lower red hue range
        'upper1': [10, 255, 255],
        'lower2': [170, 120, 70],    # Upper red hue range
        'upper2': [180, 255, 255]
    },
    'blue': {
        'lower1': [94, 80, 2],
        'upper1': [126, 255, 255],
    },
    'green': {
        'lower1': [35, 80, 50],
        'upper1': [85, 255, 255],
    },
    'yellow': {
        'lower1': [20, 100, 100],
        'upper1': [30, 255, 255],
    }
}

# Camera Settings
CAMERA_INDEX = 0              # Default camera (0 = built-in, 1 = external)
CAMERA_WARMUP_TIME = 3        # Seconds to wait for camera initialization
BACKGROUND_FRAMES = 30        # Number of frames to capture for background

# Processing Settings
MORPHOLOGY_KERNEL_SIZE = (3, 3)    # Kernel for noise removal
DILATION_ITERATIONS = 2             # Number of dilation iterations
GAUSSIAN_BLUR_KERNEL = (5, 5)      # Kernel for smoothing mask edges

# Recording Settings
DEFAULT_FPS = 20
VIDEO_CODEC = 'XVID'          # Video codec (XVID, MJPG, MP4V)
OUTPUT_FORMAT = '.avi'         # Output video format

# UI Settings
FONT = 0                       # cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.7
FONT_THICKNESS = 2
TEXT_COLOR = (0, 255, 0)      # Green
