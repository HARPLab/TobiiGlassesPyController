import cv2
import cv2.aruco as aruco
import numpy as np
from aruco_gen import Aruco_Detector, AOI_Aruco

img = cv2.imread("aruco_side_bracket.png")
board = aruco.GridBoard_create(markersX=1,
                                markersY=4,
                                dictionary=aruco.Dictionary_get(aruco.DICT_6X6_250),
                                firstMarker=12)

markerCorners, markerIds, rejectedPts = aruco.detectMarkers(img, aruco.Dictionary_get(aruco.DICT_6X6_250),
                                                            parameters=aruco.DetectorParameters_create())
# aruco.estimatePoseBoard(markerCorners, markerIds, board=board)
print(markerCorners, markerIds)
