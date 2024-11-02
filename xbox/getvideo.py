import cv2
import time
import mediapipe as mp
import threading
import datetime
from xbox_read import XboxController
import serial

CANNY_HIGH = 175
CANNY_LOW = 174

# /dev/video0 = internal camera (id = 0)
# /dev/video2 = analog camera (id = 2)
cam = cv2.VideoCapture('/dev/video2')
xc = XboxController()
ser = serial.Serial(
    port='/dev/ttyUSB1',
    baudrate=115200,
    timeout=2)

ser.flush()


def colorAndCannyEdge():
    global cam
    global CANNY_HIGH
    global CANNY_LOW
    dtob = str(datetime.datetime.now())
    out = cv2.VideoWriter('../logs/flight'+dtob+'.avi', -1, 20.0, (640, 480))
    while (True):
        _, frame = cam.read()
        out.write(frame)
        cv2.imshow('color', frame)
        canny = cv2.Canny(frame, CANNY_LOW, CANNY_HIGH)
        cv2.imshow('canny', canny)
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            break


def depthEstimation():
    global cam
    mono_model = cv2.dnn.readNet("model-small.onnx")

    def depth_to_distance(depth):
        return -1.5 * depth + 2
    while True:

        ret, frame = cam.read()
        height, width, channels = frame.shape
        start_time = time.time()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        blob = cv2.dnn.blobFromImage(
            frame, 1/255., (256, 256), (123.675, 116.28, 103.53), True, False)
        mono_model.setInput(blob)
        depth_map = mono_model.forward()
        depth_map = depth_map[0, :, :]
        depth_map = cv2.resize(depth_map, (width, height))
        depth_map = cv2.normalize(
            depth_map, None, 0, 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        fps = 1 / (time.time() - start_time)
        cv2.putText(depth_map, f"FPS is {int(fps)}", (15, 65),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
        cv2.imshow("Depth Map", depth_map)
        if cv2.waitKey(1) & 0xFF == 'q':
            break


def commLora():
    while True:
        print(xc.read())
        ser.write((str(xc.read()).replace(" ", "")+"\n").encode('utf-8'))
        time.sleep(0.2)
        print(ser.readline())


cevid = threading.Thread(target=colorAndCannyEdge)
depthvid = threading.Thread(target=depthEstimation)
commlora = threading.Thread(target=commLora)

cevid.start()
commlora.start()

# Depth Estimation temporarily disabled -- too lagggy
# depthvid.start()

cevid.join()
# depthvid.join()
cam.release()
cv2.destroyAllWindows()
