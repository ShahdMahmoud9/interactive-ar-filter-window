import cv2
import mediapipe as mp
import numpy as np
from config import (
    NUM_HANDS, DETECTION_CONF, TRACKING_CONF,
    CAM_WIDTH, CAM_HEIGHT,
    LANDMARK_COLOR, LANDMARK_RADIUS,
)

# MediaPipe landmark indices we care about
IDX_WRIST       = 0
IDX_THUMB_TIP   = 4
IDX_INDEX_TIP   = 8
IDX_MIDDLE_TIP  = 12
IDX_RING_TIP    = 16
IDX_PINKY_TIP   = 20


class HandTracker:
    def __init__(self):
        self._mp_hands = mp.solutions.hands
        self._hands = self._mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=NUM_HANDS,
            min_detection_confidence=DETECTION_CONF,
            min_tracking_confidence=TRACKING_CONF,
        )
        self._mp_draw = mp.solutions.drawing_utils

    def process(self, frame_bgr: np.ndarray) -> dict:
        """
        Process one BGR frame
        Returns
        dict with keys  'left'  and  'right'.
        Each value is either None (hand not visible) or a dict:
          {
            'landmarks' : list of (x_px, y_px) for all 21 points,
            'wrist'     : (x, y),
            'thumb_tip' : (x, y),
            'index_tip' : (x, y),
          }
        """
        h, w = frame_bgr.shape[:2]
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        results = self._hands.process(rgb)

        hands = {'left': None, 'right': None}

        if not results.multi_hand_landmarks:
            return hands

        for hand_landmarks, hand_info in zip(
            results.multi_hand_landmarks,
            results.multi_handedness,
        ):
            # MediaPipe labels are from the *mirrored* view so we flip them
            label = hand_info.classification[0].label.lower()   # 'left' or 'right'
            label = 'right' if label == 'left' else 'left'       # mirror correction

            lm_list = []
            for lm in hand_landmarks.landmark:
                x_px = int(lm.x * w)
                y_px = int(lm.y * h)
                lm_list.append((x_px, y_px))

            hands[label] = {
                'landmarks' : lm_list,
                'wrist'     : lm_list[IDX_WRIST],
                'thumb_tip' : lm_list[IDX_THUMB_TIP],
                'index_tip' : lm_list[IDX_INDEX_TIP],
            }

        return hands

    
    def draw_landmarks(self, frame_bgr: np.ndarray, hands: dict) -> None:
        """Draw thumb tip and index tip circles on the frame (in-place)."""
        for side, data in hands.items():
            if data is None:
                continue
            for pt in [data['thumb_tip'], data['index_tip']]:
                cv2.circle(frame_bgr, pt, LANDMARK_RADIUS, LANDMARK_COLOR, -1)
    def release(self):
        self._hands.close()
