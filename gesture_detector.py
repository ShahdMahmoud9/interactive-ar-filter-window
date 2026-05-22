import time
import math
from config import PINCH_THRESHOLD_PX, SWITCH_COOLDOWN_SEC, CAM_WIDTH, CAM_HEIGHT


class GestureDetector:

    def __init__(self):
        self._last_switch_time = 0.0
        self._pinch_was_active = False          

    @staticmethod
    def _distance(p1: tuple, p2: tuple) -> float:
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    
    def check_pinch(self, hands: dict) -> bool:
        """
        Returns True ONCE when a new right-hand pinch is detected
        and the cooldown has elapsed.
        """
        right = hands.get('right')
        if right is None:
            self._pinch_was_active = False
            return False

        dist = self._distance(right['thumb_tip'], right['index_tip'])
        is_pinching = dist < PINCH_THRESHOLD_PX

        now = time.time()
        fired = False

        if is_pinching and not self._pinch_was_active:
            if now - self._last_switch_time >= SWITCH_COOLDOWN_SEC:
                fired = True
                self._last_switch_time = now

        self._pinch_was_active = is_pinching
        return fired


    def hand_distance_normalized(self, hands: dict) -> float:
        """
        Returns a value in [0.0, 1.0] representing how far apart both hands are.
        0.0  →  hands touching
        1.0  →  hands at maximum expected distance (full frame diagonal)
        Returns 0.5 if only one hand is visible.
        """
        left  = hands.get('left')
        right = hands.get('right')

        if left is None or right is None:
            return 0.5

        dist = self._distance(left['wrist'], right['wrist'])
        max_dist = math.hypot(CAM_WIDTH, CAM_HEIGHT)   # ~800 px
        return min(dist / max_dist, 1.0)

    
    def pinch_distance(self, hands: dict) -> float:
        right = hands.get('right')
        if right is None:
            return 999.0
        return self._distance(right['thumb_tip'], right['index_tip'])