# Invisibility Cloak using OpenCV

> *"It is our choices, Harry, that show what we truly are, far more than our abilities."* – Albus Dumbledore

This is a fun real-time computer vision project where you can make yourself "invisible" using Python and OpenCV, just like Harry Potter's cloak! The project uses color detection and image masking to create a magical invisibility effect.

## Demo

<p align="center">
  <img src="working_demo_screenshot.png" alt="Invisibility Cloak in Action" width="800">
</p>

*The magic in action - Watch as the black cloth makes the person invisible in real-time!*

## Features

- **Multiple Color Support**: Choose between red, blue, or green cloaks
- **Video Recording**: Save your magical moments
- **Live Background Refresh**: Recapture background without restarting
- **Debug Mode**: See exactly what the algorithm detects
- **Configurable Settings**: Easy customization via config file
- **Cross-Platform**: Works on Windows, macOS, and Linux

## How It Works

1. **Background Capture**: Captures 30 frames of the static background
2. **Color Detection**: Identifies the specified color (red/blue/green) in HSV color space
3. **Mask Creation**: Creates a binary mask of detected color regions
4. **Noise Removal**: Applies morphological operations to clean up the mask
5. **Image Replacement**: Replaces masked regions with the background
6. **Magic!**: The colored cloth appears invisible!

### Technical Details
- Uses HSV color space for robust color detection
- Morphological operations (opening, closing, dilation) for noise reduction
- Gaussian blur for smooth mask edges
- Bitwise operations for efficient image composition

## Tech Stack

- **Python 3.7+**
- **OpenCV** - Computer vision operations
- **NumPy** - Array manipulations

## Installation & Usage

### Prerequisites
- Python 3.7 or higher
- Webcam/Camera
- Colored cloth (red, blue, or green)

### Quick Start

#### macOS/Linux:
```bash
# Clone the repository
git clone https://github.com/yourusername/Invisibility-Cloak-OpenCV.git
cd Invisibility-Cloak-OpenCV

# Install dependencies
pip3 install -r requirements.txt

# Run the basic version
python3 cloak.py
```

#### Windows:
```bash
pip install -r requirements.txt
python cloak.py
```

### Advanced Usage

```bash
# Use blue cloak instead of red
python3 cloak.py --color blue

# Record the output video
python3 cloak.py --record

# Use green cloak and record
python3 cloak.py --color green --record

# Hide debug window
python3 cloak.py --no-debug
```

## Controls

| Key | Action |
|-----|--------|
| `Q` | Quit the application |
| `R` | Recapture background |
| `SPACE` | Toggle mask debug view |

## Step-by-Step Instructions

1. **Setup**: Ensure your camera is connected and positioned properly
2. **Run**: Execute the script with your chosen options
3. **Background**: Stay out of frame during background capture (first 3 seconds)
4. **Cloak**: Put on or hold the colored cloth in front of the camera
5. **Magic**: Watch yourself disappear!

## Configuration

Edit `config.py` to customize:
- HSV color ranges for better detection
- Morphological operation parameters
- Camera settings
- Recording options

## Troubleshooting

### Camera Issues (macOS)
```
Error: OpenCV: not authorized to capture video
```
**Solution**: 
1. Open System Settings → Privacy & Security → Camera
2. Add Terminal (or your IDE like VS Code) to allowed apps
3. Restart Terminal and try again

### Poor Detection
**Solution**:
- Ensure good lighting conditions
- Use a solid-colored cloth without patterns
- Adjust HSV ranges in `config.py`
- Try different colors (blue works well in bright environments)

### Flickering Effect
**Solution**:
- Increase `DILATION_ITERATIONS` in `config.py`
- Ensure stable camera position
- Avoid moving background objects

## Contributing

Contributions are welcome! Here are some ideas:
- Add more color options
- Implement gesture controls
- Add GUI for settings
- Support for multiple people
- Performance optimizations

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Credits

### Project Maintainer & Original Author
**Rohini Sonawane**  
BE Artificial Intelligence & Data Science  
Savitribai Phule Pune University

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/your-profile)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat&logo=github)](https://github.com/rohini-username)

### Contributors
**Siddhesh Suryawanshi**  
BE Artificial Computer Engineering
Savitribai Phule Pune University
Enhanced with multi-color support, video recording, improved error handling, and comprehensive documentation.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/siddhesh-suryawanshi-866b67361/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat&logo=github)](https://github.com/SiddheshSuryawanshi17)

## Acknowledgments

- Inspired by the Harry Potter series by J.K. Rowling
- OpenCV community for excellent documentation
- All contributors who helped improve this project

## Learn More

- [OpenCV Documentation](https://docs.opencv.org/)
- [HSV Color Space Explained](https://en.wikipedia.org/wiki/HSL_and_HSV)
- [Morphological Transformations](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html)

---

If you found this project helpful, please star the repository!

Made with love and a bit of magic
