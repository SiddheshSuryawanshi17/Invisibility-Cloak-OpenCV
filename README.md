# Invisibility Cloak using OpenCV - Enhanced Edition

> **⚡ This is an independently enhanced fork** of [Rohini Sonawane's Invisibility-Cloak-OpenCV](https://github.com/ROHINI177/Invisibility-Cloak-OpenCV) with AI capabilities, GUI interface, and advanced effects added by Siddhesh Suryawanshi.

This is a fun real-time computer vision project where you can make yourself "invisible" using Python and OpenCV, just like Harry Potter's cloak!

## ✨ What's New in This Enhanced Version?

### GUI Version
- User-friendly interface with tkinter
- Multi-language support (English, Spanish, Hindi, French)
- Real-time transparency control
- Easy color selection

### AI-Enhanced Version
- **No colored cloth needed!** Uses MediaPipe AI
- Detects your body automatically
- Multiple modes: Full Invisibility, Ghost, Outline

### Advanced Effects Version
- Multiple color detection
- Special effects: Blur, Pixelate, Rainbow
- Adjustable transparency levels
- Screenshot capture feature

### Color Calibration Tool
- Fine-tune HSV values for perfect detection
- Real-time mask preview

## How It Works
- **Basic Version:** Detects colored cloth in webcam feed and replaces it with static background
- **AI Version:** Uses MediaPipe to detect person and make them invisible (no cloth needed!)
- **Advanced Version:** Multiple colors with special effects and transparency control

## Tech Stack
- Python 3.7+
- OpenCV 4.8+
- Numpy 1.24+
- MediaPipe 0.10+ (for AI version)
- Tkinter (for GUI version)
- Pillow 10.0+ (for GUI version)

## Prerequisites
- Python 3.7 or higher
- Working webcam
- Colored cloth (red/blue/green/yellow) - *not needed for AI version*

## 🚀 How to Run

### Step 1: Clone & Install
```bash
git clone https://github.com/SiddheshSuryawanshi17/Invisibility-Cloak-OpenCV.git
cd Invisibility-Cloak-OpenCV
pip install -r requirements.txt
```

### Step 2: Choose Your Version

#### Basic Version (Original)
```bash
python cloak.py
```

#### GUI Version (Recommended for Beginners)
```bash
python cloak_gui.py
```
- Select language and color
- Click "Capture Background" (stay out of frame!)
- Click "Start Cloak" and enjoy!

#### AI Version (No Cloth Needed!)
```bash
python cloak_ai.py
```
**Controls:** `1`=Invisible | `2`=Ghost | `3`=Outline | `r`=Reset | `s`=Screenshot | `q`=Quit

#### Advanced Effects Version
```bash
python cloak_advanced.py
```
**Controls:** `1-5`=Transparency | `e`=Effects | `c`=Color | `r`=Reset | `s`=Screenshot | `q`=Quit

#### Color Calibration Tool
```bash
python color_calibration.py
```
Adjust sliders until cloth appears white in mask window!

## 💡 Tips for Best Results
- Use **bright colored cloth** for better detection
- Ensure **good lighting** in room
- Keep **background static** during capture
- **Stay out of frame** for first 3 seconds
- AI version works best with **even lighting**

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Camera not opening | Try `--camera 1` or close other apps |
| Poor color detection | Use `color_calibration.py` tool |
| Low FPS / Lag | Close other apps, use basic version |
| AI version slow | Try `python cloak_ai.py --model 0` |
| Module not found | Run `pip install -r requirements.txt` |

## 📷 Demo
![Invisibility Cloak Demo](Screenshot%202026-01-29%20234644.png)

*The invisibility cloak in action!*

## Contributing
Contributions are welcome! Feel free to submit issues and pull requests.

## Acknowledgments

### Original Project
**Rohini Sonawane**  
BE Artificial Intelligence & Data Science  
Savitribai Phule Pune University  
[Original Repository](https://github.com/ROHINI177/Invisibility-Cloak-OpenCV)

### Enhanced By
**Siddhesh Suryawanshi**  
[GitHub](https://github.com/SiddheshSuryawanshi17) | [LinkedIn](https://www.linkedin.com/in/siddhesh-suryawanshi-866b67361/)

**Major Enhancements Added:**
- ✅ **GUI Version** with multi-language support
- ✅ **AI-Enhanced Version** using MediaPipe (no cloth needed!)
- ✅ **Advanced Effects** (blur, pixelate, rainbow)
- ✅ **Color Calibration Tool** for HSV tuning
- ✅ **Multiple Effect Modes** (invisible, ghost, outline)
- ✅ **Screenshot Feature** for saving outputs
- ✅ **Command-line Arguments** for flexibility
- ✅ **Enhanced Documentation** with step-by-step guides
- ✅ **Performance Optimizations** and error handling

### Special Thanks
- OpenCV community for excellent documentation
- MediaPipe team for AI segmentation models
- All contributors and users of this project

## License
This project builds upon the original work and maintains the same open-source spirit.

---

⭐ **If you find this project helpful, please star the repository!**

**Original Project:** [ROHINI177/Invisibility-Cloak-OpenCV](https://github.com/ROHINI177/Invisibility-Cloak-OpenCV)

