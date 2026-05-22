import cv2
import numpy as np


#helpers
def _ensure_bgr(roi: np.ndarray) -> np.ndarray:
    "Make sure the output is always 3channel pgr"
    if len(roi.shape) == 2:
        return cv2.cvtColor(roi, cv2.COLOR_GRAY2BGR)
    return roi


def _odd(n: int) -> int:
    "Return n as the nearest odd number ≥ 1 (required by GaussianBlur)"
    n = max(1, int(n))
    return n if n % 2 == 1 else n + 1


# Filter 1 — Glow Effect
def apply_glow(roi: np.ndarray, intensity: float) -> np.ndarray:
    "intensity  →  how strong the blur bloom is  (0 = subtle, 1 = heavy)"
    # Map intensity to blur kernel size  (5 … 35)
    k = _odd(5 + intensity * 30)

    blurred = cv2.GaussianBlur(roi, (k, k), 0)

    # Blend original + blurred  to create bloom
    alpha = 0.55 + intensity * 0.35          # 0.55 … 0.90
    glow  = cv2.addWeighted(roi, alpha, blurred, 1.0 - alpha + 0.4, 0)

    # Boost brightness slightly
    bright = np.clip(glow.astype(np.int16) + int(intensity * 30), 0, 255).astype(np.uint8)
    return bright


#Filter 2 — Black & White

def apply_anime_bw(roi: np.ndarray, intensity: float) -> np.ndarray:
   
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # CLAHE for local contrast enhancement
    clip  = 1.0 + intensity * 7.0          # 1 … 8
    clahe = cv2.createCLAHE(clipLimit=clip, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Optional light sharpening pass
    kernel = np.array([[-1, -1, -1],
                       [-1,  9, -1],
                       [-1, -1, -1]], dtype=np.float32)
    sharpened = cv2.filter2D(enhanced, -1, kernel)
    sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)

    return _ensure_bgr(sharpened)


# Filter 3 — Edge Detection

def apply_edge_detection(roi: np.ndarray, intensity: float) -> np.ndarray:
   
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Blur slightly before Canny to reduce noise
    blur_k = _odd(3 + (1.0 - intensity) * 4)
    blurred = cv2.GaussianBlur(gray, (blur_k, blur_k), 0)

    # Canny thresholds: high intensity → lower thresholds → more edges
    t_low  = int(30  + (1.0 - intensity) * 70)
    t_high = int(100 + (1.0 - intensity) * 100)
    edges  = cv2.Canny(blurred, t_low, t_high)

    # Colour the edges cyan/green on dark background
    result = np.zeros_like(roi)
    result[edges > 0] = (0, 255, 180)       # cyan-green  (BGR)

    # Blend a dim version of the original underneath for depth
    dim_original = (roi * 0.15).astype(np.uint8)
    result = cv2.add(result, dim_original)

    return result


# Filter 4 — Thermal / Energy Vision
def apply_thermal(roi: np.ndarray, intensity: float) -> np.ndarray:
    
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Slight blur for smoother thermal look
    k = _odd(3 + intensity * 6)
    blurred = cv2.GaussianBlur(gray, (k, k), 0)

    # Apply JET colormap (blue cold → red hot)
    thermal = cv2.applyColorMap(blurred, cv2.COLORMAP_JET)

    # Boost saturation with intensity
    hsv = cv2.cvtColor(thermal, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * (1.0 + intensity * 1.5), 0, 255)
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] * (0.7 + intensity * 0.5), 0, 255)
    result = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

    return result


# Filter dispatcher

FILTERS = [
    apply_glow,
    apply_anime_bw,
    apply_edge_detection,
    apply_thermal,
]


def apply_filter(roi: np.ndarray, filter_index: int, intensity: float) -> np.ndarray:
    "return the processed ROI"
    fn = FILTERS[filter_index % len(FILTERS)]
    return fn(roi, intensity)
