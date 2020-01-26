import time
import cv2
import os
import slack

calibration_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "calibration")
pomodoro_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pomodoro")

def start_capturing(capture_time, interval, dir):
    start_time = time.time() 
    i = 0

    while (time.time() - start_time < capture_time):
        capture_image(dir, "capture" + str(i) + ".png")
        time.sleep(interval)
        i += 1

def capture_image(dir, name):
    path = os.path.abspath(dir + "/" + name)

    camera_port = 0
    camera = cv2.VideoCapture(camera_port)
    time.sleep(0.1)  # If you don't wait, the image will be dark
    return_value, image = camera.read()
    cv2.imwrite(path, image)
    del(camera)  # so a others can use the camera as soon as possible



