import cv2
import numpy as np
from config import (
    FILTER_NAMES, RECT_COLOR, RECT_THICKNESS,
    TEXT_COLOR, CAM_WIDTH, CAM_HEIGHT,
    PINCH_THRESHOLD_PX,
)


class Renderer:
    def draw_window_rect(
        self,
        frame: np.ndarray,
        rect: tuple,
        color: tuple = RECT_COLOR,
    ) -> None:
        "Draw the AR filter window border (in-place)"
        x1, y1, x2, y2 = rect
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, RECT_THICKNESS)

        # Corner accent marks for a futuristic look
        corner_len = 14
        thick = RECT_THICKNESS + 1
        corners = [
            # top-left
            [(x1, y1 + corner_len), (x1, y1), (x1 + corner_len, y1)],
            # top-right
            [(x2 - corner_len, y1), (x2, y1), (x2, y1 + corner_len)],
            # bottom-left
            [(x1, y2 - corner_len), (x1, y2), (x1 + corner_len, y2)],
            # bottom-right
            [(x2 - corner_len, y2), (x2, y2), (x2, y2 - corner_len)],
        ]
        for pts in corners:
            for i in range(len(pts) - 1):
                cv2.line(frame, pts[i], pts[i + 1], (255, 255, 255), thick)

   
    def draw_hud(
        self,
        frame: np.ndarray,
        filter_index: int,
        intensity: float,
        pinch_dist: float,
        rect_visible: bool,
    ) -> None:
        #Filter name
        name = FILTER_NAMES[filter_index % len(FILTER_NAMES)]
        cv2.putText(
            frame,
            f"Filter: {name}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            TEXT_COLOR,
            2,
            cv2.LINE_AA,
        )

        #Intensity bar
        bar_x, bar_y, bar_w, bar_h = 10, 45, 160, 12
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), (60, 60, 60), -1)
        filled = int(bar_w * intensity)
        bar_color = (0, int(180 + 75 * intensity), int(255 * (1 - intensity)))
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + filled, bar_y + bar_h), bar_color, -1)
        cv2.putText(
            frame,
            f"Intensity {int(intensity * 100):3d}%",
            (bar_x + bar_w + 6, bar_y + 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.42,
            TEXT_COLOR,
            1,
            cv2.LINE_AA,
        )

        #Pinch indicator
        is_pinching = pinch_dist < PINCH_THRESHOLD_PX
        pinch_color = (0, 255, 100) if is_pinching else (80, 80, 80)
        pinch_text  = "PINCH" if is_pinching else "Pinch to switch"
        cv2.putText(
            frame,
            pinch_text,
            (10, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            pinch_color,
            1,
            cv2.LINE_AA,
        )

        #Window status
        status       = "Window: ACTIVE" if rect_visible else "Show both hands"
        status_color = (0, 255, 180) if rect_visible else (0, 140, 255)
        cv2.putText(
            frame,
            status,
            (10, CAM_HEIGHT - 12),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            status_color,
            1,
            cv2.LINE_AA,
        )

        #Instructions (top-right)
        cv2.putText(
            frame,
            "ESC: quit  |  Pinch R hand: switch",
            (CAM_WIDTH - 300, CAM_HEIGHT - 12),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.40,
            (160, 160, 160),
            1,
            cv2.LINE_AA,
        )

    def draw_finger_line(
        self,
        frame: np.ndarray,
        hands: dict,
    ) -> None:
        left  = hands.get('left')
        right = hands.get('right')
        if left is None or right is None:
            return
        cv2.line(
            frame,
            left['index_tip'],
            right['index_tip'],
            (80, 80, 80),
            1,
            cv2.LINE_AA,
        )