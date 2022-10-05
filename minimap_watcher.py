import argparse
import os
import platform
import time

import numpy as np
import cv2
from mss import mss, screenshot

from constants import (
    YELLOW_HUE_RANGE,
    MINIMAP_TOP_OFFSET,
    MINIMAP_LEFT_OFFSET,
    MINIMAP_BOX_SIDE,
    MONITOR_WIDTH,
)


def is_color_in_img(image: screenshot.ScreenShot, color_range_min, color_range_max):
    img_hsv = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2HSV)
    threshold_img = cv2.inRange(img_hsv, color_range_min, color_range_max)
    n_pixels_in_threshold = np.count_nonzero(threshold_img != 0)
    return n_pixels_in_threshold > 20, threshold_img


def show_img(img):
    cv2.imshow('screen', np.array(img))
    cv2.waitKey()


def send_notification(msg):
    plt = platform.system()
    title = "Minimap Watcher"

    if plt == 'Linux':
        command = f'''
        notify-send "{title}" "{msg}"
        '''
        os.system(command)
    else:
        print(msg)


def main():
    parser = argparse.ArgumentParser(
        description="Watches the pixels in your WoW minimap and alerts you when a yellow dot appears.\n"
        "Only tested at 1080p in windowed borderless, i.e. no borders like fullscreen, but mouse is free."
     )
    parser.add_argument('--fps', default=20, help="How many times per second to check the map")
    parser.add_argument('--monitor-offset', default=0, help="Monitor 0 is your left most monitor, then 1, then 2, etc")
    parser.add_argument('--alert-sleep', default=5, help="If an alert triggers, take X seconds before triggering again")
    parser.add_argument('--debug', action='store_true', help="Shows captured screen area in original and in color threshold modes")
    args = parser.parse_args()

    loop_sleep_seconds = 1 / int(args.fps)
    minimap_box = {
        'top': MINIMAP_TOP_OFFSET,
        'left': int(args.monitor_offset) * MONITOR_WIDTH + MINIMAP_LEFT_OFFSET,
        'width': MINIMAP_BOX_SIDE,
        'height': MINIMAP_BOX_SIDE,
    }

    last_alert = 0
    with mss() as sct:
        while True:
            original_img = sct.grab(minimap_box)
            found_node, threshold_img = is_color_in_img(original_img, YELLOW_HUE_RANGE["min"], YELLOW_HUE_RANGE["max"])

            if found_node and time.time() - last_alert > int(args.alert_sleep):
                send_notification("Found something in minimap!")
                last_alert = time.time()

            if args.debug:
                cv2.imshow('original_minimap', np.array(original_img))
                cv2.imshow('threshold_minimap', np.array(threshold_img))
                if cv2.waitKey(int(loop_sleep_seconds * 1000)) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break
            else:
                time.sleep(loop_sleep_seconds)


if __name__ == "__main__":
    main()
