import cv2
import cv2.aruco as aruco
import numpy as np
from aruco_gen import Aruco_Detector, AOI_Aruco


# load test image and camera parameters for the assoc camera
# img = cv2.imread("aruco_side_bracket.png")
img = cv2.imread("/home/abhijat/Documents/Research/Light_Curtain/jeep_recce/jeep_targets_installed.jpeg")

img = cv2.resize(img, None, fx=1/3, fy=1/3)
#
camMtx = np.eye(3)  # tobii [1139.83, 0., 940.846, 0., 1140.3, 525.317, 0., 0., 1.]
#
# distortion coefficients
distCoeffs = np.zeros((1, 5))  # tobii [0.109722, -0.000415268, -2.60221E-05,  -0.382931, 0.371597]
tobii_wfcam_arucodetector = Aruco_Detector(camMtx, distCoeffs)

# init a board you expect to find in the image
aruco_grid_top = AOI_Aruco("top_ws", 16, tobii_wfcam_arucodetector,
                           markers_x=8, markers_y=1, height=508, width=4064,
                           markerLength=0.044, markerSeparation=0.005)  # marker length = 2" to m (2" x 16")

aruco_grid_bot = AOI_Aruco("bot_ws", 24, tobii_wfcam_arucodetector,
                              markers_x=8, markers_y=2, height=855, width=3810,
                              markerLength=0.034, markerSeparation=0.005)
aruco_grid_SB = AOI_Aruco("side_bracket", 12, tobii_wfcam_arucodetector,
                              markers_x=1, markers_y=4, height=3048, width=841,
                              markerLength=0.070, markerSeparation=0.005)

# detect the board in the image
corners, ids\
    = tobii_wfcam_arucodetector.getCorners(img, aruco.Dictionary_get(aruco.DICT_6X6_250))
counter = len(ids)

# can we also calibrate with these images? Should be possible but might need an image with just 1 board
# ret, camMtx_det, distCoeffs_det, rvecs, tvecs = \
# aruco.calibrateCameraAruco(corners, ids, counter, aruco_grid_SB.getAOI(), img.shape[:-1], None, None)

(valid, rvec, tvec) = aruco_grid_SB.estimatePose(corners, ids, camMtx, distCoeffs)
# markerCorners, markerIds, rejectedPts = aruco.detectMarkers(img, aruco.Dictionary_get(aruco.DICT_6X6_250),
#                                                             parameters=aruco.DetectorParameters_create())

# estimate pose
# aruco.estimatePoseBoard(markerCorners, markerIds, board=board)

# draw the detected aruco board axis
aruco.drawAxis(img, camMtx, distCoeffs, rvec, tvec, length=0.5)
cv2.imshow("raw_image", img)
cv2.waitKey(0)
print(corners, ids)
