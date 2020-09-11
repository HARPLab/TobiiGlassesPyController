import cv2
import av
import numpy as np
from tobiiglassesctrl import TobiiGlassesController
import zmq
import imagezmq

def calibrate():
    # calibrate
    print(tobiiglasses.get_battery_info())
    print(tobiiglasses.get_storage_info())

    if tobiiglasses.is_recording():
        rec_id = tobiiglasses.get_current_recording_id()
        tobiiglasses.stop_recording(rec_id)

    project_name = input("Please insert the project's name: ")
    project_id = tobiiglasses.create_project(project_name)

    participant_name = input("Please insert the participant's name: ")
    participant_id = tobiiglasses.create_participant(project_id, participant_name)

    calibration_id = tobiiglasses.create_calibration(project_id, participant_id)
    input("Put the calibration marker in front of the user, then press enter to calibrate")
    tobiiglasses.start_calibration(calibration_id)

    res = tobiiglasses.wait_until_calibration_is_done(calibration_id)

    if res is False:
        print("Calibration failed!")
        exit(1)
    return

if __name__ == "__main__":
    port = 5555
    sender = imagezmq.ImageSender("tcp://*:{}".format(port), REQ_REP=False)

    #  connect to Tobii
    tobiiglasses = TobiiGlassesController(video_scene=True)
    ipv4_address = tobiiglasses.get_address()

    # # calibrate
    # print(tobiiglasses.get_battery_info())
    # print(tobiiglasses.get_storage_info())
    #
    # if tobiiglasses.is_recording():
    #     rec_id = tobiiglasses.get_current_recording_id()
    #     tobiiglasses.stop_recording(rec_id)
    #
    # project_name = input("Please insert the project's name: ")
    # project_id = tobiiglasses.create_project(project_name)
    #
    # participant_name = input("Please insert the participant's name: ")
    # participant_id = tobiiglasses.create_participant(project_id, participant_name)
    #
    # calibration_id = tobiiglasses.create_calibration(project_id, participant_id)
    # input("Put the calibration marker in front of the user, then press enter to calibrate")
    # tobiiglasses.start_calibration(calibration_id)
    #
    # res = tobiiglasses.wait_until_calibration_is_done(calibration_id)
    #
    # if res is False:
    #     print("Calibration failed!")
    #     exit(1)

    # start video stream
    tobiiglasses.start_streaming()

    rtsp_url = "rtsp://[%s]:8554/live/scene" % ipv4_address
    container = av.open(rtsp_url, options={'rtsp_transport': 'tcp'})
    stream = container.streams.video[0]
    frame_counter = 0
    jpeg_quality = 100

    for frame in container.decode(stream):
        frame_counter += 1

        data_gp = tobiiglasses.get_data()['gp']
        data_gp3 = tobiiglasses.get_data()['gp3']
        data_pts = tobiiglasses.get_data()['pts']
        frame_cv = frame.to_ndarray(format='bgr24')

        ret_code, jpg_buffer = cv2.imencode(
            ".jpg", frame_cv, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
        msg = "%d %f" % (frame_counter, frame.pts)  # send frame_counter to make sure no drops and pts to sync
        sender.send_jpg(msg, jpg_buffer)
        print("Sent frame {}".format(frame_counter), msg)

        # print(data_gp['ts'], data_gp3['ts'], data_pts['ts'])
        print(data_pts)
        print(frame.time, frame.pts, frame.time_base)
        if data_gp['ts'] > 0 and data_pts['ts'] > 0:
            offset = data_gp['ts'] / 1000.0 - data_pts['ts'] / 1000.0  # in milliseconds
            print(data_pts, data_gp)

            print('Frame_pts = %f' % float(frame.pts))
            print('Frame_time = %f' % float(frame.time))
            print('Gaze ts = %f' % float(data_gp['ts']))
            print('Data_pts = %f' % float(data_pts['pts']))
            print('Offset = %f' % float(offset))

            # Overlay gazepoint
            height, width = frame_cv.shape[:2]
            cv2.circle(frame_cv, (int(data_gp['gp'][0] * width), int(data_gp['gp'][1] * height)), 20, (0, 0, 255), 6)




        # Display Stream
        # cv2.imshow("Livestream", frame_cv)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    # TODO add:
    ## 1. sync in support
    ## 2. all gaze points - gp, gp3
    ## 3. ts, pts, ets, vts supports
    #1 test streaming
    #2 setup sockets/design ROS interface w ZMQ?
    #3 design ROS wrapper - which things are important/which topics to have etc

    cv2.destroyAllWindows()
    tobiiglasses.stop_streaming()
    tobiiglasses.close()
