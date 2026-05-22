import numpy as np
from config import MIN_WINDOW_SIZE, CAM_WIDTH, CAM_HEIGHT


class FilterWindow:

    def get_rect(self, hands: dict):
        """
        Returns (x1, y1, x2, y2) in pixel coordinates, or None.
        x1, y1  →  top-left
        x2, y2  →  bottom-right
        Guarantees x1 < x2  and  y1 < y2  and minimum size.
        """
        left  = hands.get('left')
        right = hands.get('right')

        if left is None or right is None:
            return None

        #index finger tip as the corner markers
        lx, ly = left['index_tip']
        rx, ry = right['index_tip']

        #Sort so x1 < x2 and y1 < y2 regardless of hand positions
        x1 = max(0, min(lx, rx))
        y1 = max(0, min(ly, ry))
        x2 = min(CAM_WIDTH  - 1, max(lx, rx))
        y2 = min(CAM_HEIGHT - 1, max(ly, ry))

        #Reject if too small
        if (x2 - x1) < MIN_WINDOW_SIZE or (y2 - y1) < MIN_WINDOW_SIZE:
            return None

        return (x1, y1, x2, y2)

    def extract_roi(self, frame: np.ndarray, rect: tuple) -> np.ndarray:
        "Slice and return the ROI region from the frame"
        x1, y1, x2, y2 = rect
        return frame[y1:y2, x1:x2].copy()

    def paste_roi(self, frame: np.ndarray, roi: np.ndarray, rect: tuple) -> None:
        "Paste the processed ROI back into the frame (in-place)"
        x1, y1, x2, y2 = rect
        rh, rw = roi.shape[:2]
        #Guard against shape mismatch after any resize
        frame[y1:y1 + rh, x1:x1 + rw] = roi
