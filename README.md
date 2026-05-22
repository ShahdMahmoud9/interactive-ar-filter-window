# AR Filter Window — Real-Time Gesture-Controlled Visual Effects

> Control a floating AR filter window in mid-air using nothing but your hands.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green?style=flat-square&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10+-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)
![GPU](https://img.shields.io/badge/GPU-Not%20Required-lightgrey?style=flat-square)

---

## 📌 What Is This?

An interactive AR-style application that uses your **webcam + hand gestures** to create a floating rectangular "filter window" in the air.

- 🟢 **Inside** the window → a real-time visual filter is applied
- ⚫ **Outside** the window → your webcam feed stays completely normal

No GPU needed. Runs smoothly on a standard laptop CPU.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🖐️ **Dual Hand Tracking** | Tracks both hands using MediaPipe Hands (21 landmarks each) |
| 🔲 **Dynamic Filter Window** | Your two index fingers define the corners of a live rectangle |
| 🤏 **Pinch to Switch** | Pinch thumb + index finger to cycle through filters |
| 📏 **Distance = Intensity** | Move hands apart or together to control filter strength |
| ⚡ **ROI-Only Processing** | Filters applied only inside the window — lightweight and fast |
| 🎨 **4 Visual Filters** | Glow, Anime B&W, Edge Detection, Thermal Vision |

---

## 🎨 Filters

### 1. 🌟 Glow Effect
Soft bloom and bright highlights, inspired by anime aura scenes and futuristic AR visuals. Hand distance controls bloom intensity.

### 2. 🖤 Anime Black & White
Manga-style high-contrast grayscale with CLAHE enhancement and sharpening. Looks like a dramatic comic panel.

### 3. 🔷 Edge Detection
Cyberpunk-style cyan outlines on a dark background using Canny edge detection. Hand distance controls edge sensitivity.

### 4. 🔴 Thermal Vision
Heat-map color mapping (blue → red) with boosted saturation. Looks like an energy scanner.

---

## 🕹️ Controls

| Gesture / Key | Action |
|---|---|
| ✋ Raise both hands | Activate the filter window |
| 👆 Move index fingers | Resize and reposition the window |
| 🤏 Pinch right hand | Switch to the next filter |
| ↔️ Move hands apart/together | Adjust filter intensity |
| `ESC` | Quit the application |

> **Note:** If pinch is detected on the wrong hand, see the [Troubleshooting](#-troubleshooting) section below.

---

## 📁 Project Structure

```
ar_filter_project/
│
├── main.py               # Entry point — main loop
├── hand_tracker.py       # MediaPipe hand tracking & landmark extraction
├── gesture_detector.py   # Pinch detection, cooldown, hand distance
├── filter_window.py      # Rectangle calculation from hand positions
├── filters.py            # All four visual filters
├── renderer.py           # ROI compositing & HUD overlay
├── config.py             # Global constants & settings
└── requirements.txt      # Python dependencies
```

---

## ⚙️ How the Filter Window Works

The window is built from the positions of your **index finger tips**:

```
Left index tip  →  one corner  (x1, y1)
Right index tip →  opposite corner  (x2, y2)
```

The rectangle is always sorted so `x1 < x2` and `y1 < y2`, meaning it works correctly regardless of which hand is higher or further left.

Once the rectangle is computed:
1. The ROI (region of interest) is extracted from the frame
2. The selected filter is applied to the ROI only
3. The processed ROI is pasted back into the original frame
4. Everything outside the rectangle is untouched

---

## 🚀 Installation & Usage

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ar-filter-window.git
cd ar-filter-window
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run

```bash
python main.py
```

> Make sure your webcam is connected and accessible before running.

---

## 📋 Requirements

- Python 3.8+
- Webcam (any standard USB or built-in)
- No GPU required

```
opencv-python >= 4.8.0
mediapipe     >= 0.10.0
numpy         >= 1.24.0
```

---

## 🛠️ Configuration

All tunable parameters are in `config.py`:

```python
CAM_WIDTH  = 640          # Camera resolution
CAM_HEIGHT = 480
PINCH_THRESHOLD_PX  = 35  # How close thumb+index must be to trigger pinch
SWITCH_COOLDOWN_SEC = 1.0 # Minimum seconds between filter switches
MIN_WINDOW_SIZE     = 40  # Minimum window size in pixels
```

---

## 🔧 Troubleshooting

### Pinch is detected on the wrong hand
Some webcams return mirrored handedness labels from MediaPipe. To fix, open `gesture_detector.py` and change `'right'` to `'left'` in two places:

```python
# In check_pinch()
right = hands.get('left')   # ← change this

# In pinch_distance()
right = hands.get('left')   # ← and this
```

### Low FPS
- Make sure no other apps are using the webcam
- Lower `CAM_FPS` in `config.py`
- The app is already optimized for CPU — ROI-only processing keeps it lightweight

### Window not appearing
- Both hands must be fully visible to the camera
- Make sure your index fingers are at least 40px apart (set by `MIN_WINDOW_SIZE`)

---

## 🏗️ Built With

- **[OpenCV](https://opencv.org/)** — webcam capture, image processing, rendering
- **[MediaPipe](https://mediapipe.dev/)** — real-time hand tracking (CPU optimized)
- **[NumPy](https://numpy.org/)** — frame manipulation and math

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙌 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

*Built to run fast on everyday hardware — no fancy GPU required.*
