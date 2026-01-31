# Demo Assets

Place your demo images and GIFs here.

## Recommended Content
- `demo.gif` - Short GIF showing the invisibility effect
- `before_after.png` - Side-by-side comparison
- `setup.jpg` - Setup photo showing the colored cloth

## Creating a Demo GIF

Using `ffmpeg`:
```bash
# Record a short video first, then convert
ffmpeg -i output.avi -vf "fps=10,scale=640:-1:flags=lanczos" -loop 0 demo.gif
```

Keep file sizes reasonable (<5MB) for GitHub.
