import numpy as np
import cv2


def checker_pose(image, camMtx, distCoeffs):
    patternSize = (5, 4)
    ret, corners = cv2.findChessboardCorners(image, patternSize)
    #
    corners_refined = cv2.cornerSubPix(image, corners, (11, 11), (-1, -1), criteria)
    # Find the rotation and translation vectors.
    ret, rvecs, tvecs = cv2.solvePnP(objp, corners_refined, camMtx, distCoeffs)

    return