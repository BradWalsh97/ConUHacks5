import time
import cv2
import os
import slack

directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "temp_capture")

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

def capture_calibration(client):


if __name__ == "__main__":
    if not os.path.isdir(directory):
        os.mkdir(directory)
    start_capturing(25, 5, directory)