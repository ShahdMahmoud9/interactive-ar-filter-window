import sys
import cv2

from config       import CAM_WIDTH, CAM_HEIGHT, CAM_FPS
from hand_tracker    import HandTracker
from gesture_detector import GestureDetector
from filter_window   import FilterWindow
from filters         import apply_filter
from renderer        import Renderer


def main():
    #Camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        sys.exit(1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  CAM_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS,          CAM_FPS)

    #Components
    tracker  = HandTracker()
    gesture  = GestureDetector()
    win      = FilterWindow()
    renderer = Renderer()

    #State
    filter_index = 0

    print("[INFO] AR Filter Window started.")
    print("       Raise both hands to activate the filter window.")
    print("       Pinch your RIGHT hand to switch filters.")
    print("       Press ESC to quit.\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to grab frame.")
            break

        # Mirror the frame so it feels like a mirror (natural UX)
        frame = cv2.flip(frame, 1)

        # Hand tracking
        hands = tracker.process(frame)

        #Gesture detection 
        if gesture.check_pinch(hands):
            filter_index = (filter_index + 1) % 4
            print(f"[INFO] Switched to filter {filter_index}")

        intensity   = gesture.hand_distance_normalized(hands)
        pinch_dist  = gesture.pinch_distance(hands)

        #Filter window rectangle 
        rect = win.get_rect(hands)

        #Apply filter inside window 
        if rect is not None:
            roi          = win.extract_roi(frame, rect)
            filtered_roi = apply_filter(roi, filter_index, intensity)
            win.paste_roi(frame, filtered_roi, rect)

            # Draw the window border on top
            renderer.draw_window_rect(frame, rect)

        # Draw hand landmarks & connecting line
        tracker.draw_landmarks(frame, hands)
        renderer.draw_finger_line(frame, hands)

        # HUD overlay
        renderer.draw_hud(
            frame,
            filter_index  = filter_index,
            intensity     = intensity,
            pinch_dist    = pinch_dist,
            rect_visible  = rect is not None,
        )

        #Display]
        cv2.imshow("AR Filter Window", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:   # ESC
            print("[INFO] Exiting.")
            break

    #Cleanup 
    tracker.release()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
