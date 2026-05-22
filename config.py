

#Camera
CAM_WIDTH   = 640
CAM_HEIGHT  = 480
CAM_FPS     = 30

#MediaPipe
NUM_HANDS           = 2
DETECTION_CONF      = 0.7
TRACKING_CONF       = 0.6

#Gesture
PINCH_THRESHOLD_PX  = 35    # pixels — distance to consider a pinch
SWITCH_COOLDOWN_SEC = 1.0   # seconds between filter switches

#Filter Window
MIN_WINDOW_SIZE     = 40    # minimum width/height in pixels

#Filters
FILTER_NAMES = [
    "Glow Effect",
    "Anime B&W",
    "Edge Detection",
    "Thermal Vision",
]

#Display
FONT                = 0     # cv2.FONT_HERSHEY_SIMPLEX 
TEXT_COLOR          = (255, 255, 255)
RECT_COLOR          = (0, 255, 180)
RECT_THICKNESS      = 2
LANDMARK_COLOR      = (0, 220, 255)
LANDMARK_RADIUS     = 5
