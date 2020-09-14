#   Copyright (C) 2020  Davide De Tommaso
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>


import cv2
import cv2.aruco as aruco
import numpy as np
import os


class Aruco_Detector:

    def __init__(self, cameraMatrix, distCoeffs):
        self.__cameraMatrix__ = cameraMatrix
        self.__distCoeffs__ = distCoeffs

    def getCorners(self, opencvMat, aruco_dict):
        opencvMat = cv2.cvtColor(opencvMat, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(opencvMat, aruco_dict)
        return (corners, ids)

    def getDetectedFeatures(self, board, corners, ids):
        (valid, rvec, tvec) = board.estimatePose(corners, ids, self.__cameraMatrix__, self.__distCoeffs__)
        detected_features_points = None
        if valid > 0:
            imgpts, jac = cv2.projectPoints(board.feature_3dpoints, rvec, tvec,\
                                            self.__cameraMatrix__, self.__distCoeffs__)
            detected_features_points = np.array([[int(imgpts[0][0][0]), int(imgpts[0][0][1])],
                                                 [int(imgpts[1][0][0]), int(imgpts[1][0][1])],
                                                 [int(imgpts[2][0][0]), int(imgpts[2][0][1])],
                                                 [int(imgpts[3][0][0]), int(imgpts[3][0][1])]  ])
        return detected_features_points


class AOI_Aruco:

    def __init__(self, aoi_label, aoi_id, aruco_detector,
                 markerLength=0.1, markerSeparation=0.1,
                 width=1920, height=1080,
                 markers_x=3,  markers_y=2,
                 aruco_dict=aruco.Dictionary_get(aruco.DICT_6X6_250)):
        self.aoi_label = aoi_label
        self.aoi_id = aoi_id
        self.markerLength = markerLength
        self.markerSeparation = markerSeparation
        self.__width__ = width
        self.__height__ = height
        self.__markers_x__ = markers_x
        self.__markers_y__ = markers_y
        self.__aruco_dict__ = aruco_dict
        self.__margin_size__ = 40

        if self.__markers_x__ > 1 and self.__markers_y__ > 1:
            self.feature_3dpoints = np.array( [[self.markerLength, self.__markers_y__*self.markerLength + (self.__markers_y__-1)*self.markerSeparation, 0.0],
                                               [(self.__markers_x__-1)*self.markerLength + (self.__markers_x__-1)*self.markerSeparation, self.__markers_y__*self.markerLength + (self.__markers_y__-1)*self.markerSeparation, 0.0],
                                               [self.markerLength, 0.0, 0.0],
                                               [(self.__markers_x__-1)*self.markerLength + (self.__markers_x__-1)*self.markerSeparation, 0.0, 0.0] ])

        elif self.__markers_x__ == 1 or self.__markers_y__ == 1:
            self.feature_3dpoints = np.array( [[0.0, self.markerLength, 0.0],
                                               [self.markerLength, self.markerLength, 0.0],
                                               [0.0, 0.0, 0.0],
                                               [self.markerLength, 0.0, 0.0] ])

        self.__aoi__ = aruco.GridBoard_create(markersX=self.__markers_x__,
                                   markersY=self.__markers_y__,
                                   markerLength=self.markerLength,
                                   markerSeparation=self.markerSeparation,
                                   dictionary=self.__aruco_dict__,
                                   firstMarker=self.aoi_id)

        corners, self.__ids__ = aruco_detector.getCorners(self.getCVMat(), self.__aruco_dict__)
        self.features_2dpoints = aruco_detector.getDetectedFeatures(self, corners, self.__ids__)

    def estimatePose(self, corners, ids, cameraMatrix, distCoeffs):
        rvec = np.array( [0.0, 0.0, 0.0] )
        tvec = np.array( [0.0, 0.0, 0.0] )
        (valid, rvec, tvec) = aruco.estimatePoseBoard(corners, ids, self.__aoi__, cameraMatrix, distCoeffs, rvec, tvec)
        return (valid, rvec, tvec)

    def exportAOI(self, filepath):
        img = self.getCVMat()
        # if self.__markers_x__ > 1 and self.__markers_y__ > 1:
        #     cv2.rectangle(img,
        #                   (self.features_2dpoints[0][0],
        #                    self.features_2dpoints[0][1]-10),
        #                   (self.features_2dpoints[3][0],
        #                    self.features_2dpoints[3][1]+10),
        #                   (255,255,255),
        #                   -1)
        cv2.imwrite(os.path.join(filepath, self.getAOIFilename()), img)

    def getAOI(self):
        return self.__aoi__

    def getCVMat(self):
        img = np.zeros([self.__height__, self.__width__, 1], dtype=np.uint8)
        img.fill(255)
        self.__aoi__.draw((self.__width__, self.__height__), img, marginSize=self.__margin_size__)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        return img

    def getAOIFilename(self):
        return "aruco_%s.png" % self.aoi_label
        # return "aruco_%s.svg" % self.aoi_label


def sample_generate():

    # detector is associated with camera
    # TODO put in world camera calib here
    tobii_wfcam_arucodetector = Aruco_Detector(np.eye(3), np.zeros((1, 5)))
    aruco_storage_dir = "./aruco_boards"

    # radio panel board 7.5" x 10" - 12 ids (0-11)
    # (190.5 x 254) mm
    boardid_RP = 0
    aruco_grid_RP = AOI_Aruco("radio_panel", boardid_RP, tobii_wfcam_arucodetector,
                              markers_x=3, markers_y=4, height=2540, width=1905,
                              markerLength=0.060, markerSeparation=0.003)  # marker length = ~2.5" to m (7.5" x 10")
    aruco_grid_RP.exportAOI(aruco_storage_dir)

    # side bracket board - (12, 13, 14, 15)
    # (304.8 x 84.1375) mm
    boardid_SB = 12
    aruco_grid_SB = AOI_Aruco("side_bracket", boardid_SB, tobii_wfcam_arucodetector,
                              markers_x=1, markers_y=4, height=3048, width=841,
                              markerLength=0.070, markerSeparation=0.005)  # marker length = ~3" to m (3.3125" x 12")
    aruco_grid_SB.exportAOI(aruco_storage_dir)

    # top windshield board (16, 17, 18, 19, 20, 21, 22, 23)
    # (50.8 x 406.4) mm
    boardid_top = 16
    aruco_grid_top = AOI_Aruco("top_ws", boardid_top, tobii_wfcam_arucodetector,
                              markers_x=8, markers_y=1, height=508, width=4064,
                              markerLength=0.044, markerSeparation=0.005)  # marker length = 2" to m (2" x 16")
    aruco_grid_top.exportAOI(aruco_storage_dir)

    # bottom windshield board (20-35)
    # (85.5 x 381) mm
    boardid_bot = 24
    aruco_grid_bot = AOI_Aruco("bot_ws", boardid_bot, tobii_wfcam_arucodetector,
                              markers_x=8, markers_y=2, height=855, width=3810,
                              markerLength=0.034, markerSeparation=0.005)  # marker length = ~1.55" to m (3.375" x 15")
    aruco_grid_bot.exportAOI(aruco_storage_dir)

    return


def __main__():
    # aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_100)
    # aruco_board = aruco.GridBoard_create(markersX=4, markersY=3, markerLength=0.0635,
    #                                      markerSeparation=0.001,
    #                                      dictionary=aruco_dict,
    #                                      firstMarker=1)
    #
    # board = aruco.drawPlanarBoard(aruco_board, (750, 1000))
    # cv2.imshow("Aruco board", board)
    # cv2.waitKey(0)

    sample_generate()
    return

if __name__ == __main__():
    __main__()
