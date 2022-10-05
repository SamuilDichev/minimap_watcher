import numpy as np

MONITOR_WIDTH = 1920
MONITOR_HEIGHT = 1080

MINIMAP_TOP_OFFSET = 55
MINIMAP_LEFT_OFFSET = 1760
MINIMAP_BOX_SIDE = 109

YELLOW_HUE_RANGE = {
    "min": np.array([22, 150, 0], np.uint8),
    "max": np.array([45, 255, 255], np.uint8),
}
