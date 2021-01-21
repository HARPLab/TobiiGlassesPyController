"""pub_sub_broadcast.py -- broadcast OpenCV stream using PUB SUB."""

import sys
# import socket
import traceback
from time import sleep
import cv2
# from imutils.video import VideoStream
import time
import zmq
import imagezmq

if __name__ == "__main__":
    # Publish on port
    port = 5555
    sender = imagezmq.ImageSender("tcp://*:{}".format(port), REQ_REP=False)
    sender = imagezmq.ImageSender("ipc:///tmp/foo", REQ_REP=False)

    # Open input stream; comment out one of these capture = VideoStream() lines!
    # Webcam source for broadcast images
    capture = cv2.VideoCapture(0)  # Webcam

    sleep(1.0)  # Warmup time
    print("Input stream opened")

    # JPEG quality, 0 - 100
    jpeg_quality = 100

    # Send RPi hostname with each image
    # This might be unnecessary in this pub sub mode, as the receiver will
    #    already need to know our address and can therefore distinguish streams
    # Keeping it anyway in case you wanna send a meaningful tag or something
    #    (or have a many to many setup)
    # rpi_name = socket.gethostname()

    frame = cv2.imread("dash_aruco_1.png")
    try:
        counter = 0
        while True:
            ret, frame = capture.read()

            ret_code, jpg_buffer = cv2.imencode(
                ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
            send_starttime = time.monotonic()
            msg = "%d %f" % (counter, send_starttime)
            sender.send_jpg(msg, jpg_buffer)
            # sender.send_image(msg, frame)
            print("Sent frame {}".format(counter))

            # pub sending start time to check transport duration
            # time_socket.send_string("time %f" % send_starttime)
            print(send_starttime)

            counter = counter + 1

    except (KeyboardInterrupt, SystemExit):
        print('Exit due to keyboard interrupt')
    except Exception as ex:
        print('Python error with no Exception handler:')
        print('Traceback error:', ex)
        traceback.print_exc()
    finally:
        capture.release()
        sender.close()
        sys.exit()
