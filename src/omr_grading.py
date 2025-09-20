# omr_grading.py

import numpy as np
import cv2
from imutils import contours
import argparse
import matplotlib.pyplot as plt

# Helper function to display images in PyCharm (optional but useful for debugging)
def plt_imshow(title, image):
    # Convert BGR image to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(10, 6))
    plt.imshow(image)
    plt.title(title)
    plt.show()

    # Load the image
    image_path = "C:/Users/lordk/Documents/metamachine/data/omr_sheets/Img1.jpeg"  # <-- CHANGE THIS TO YOUR IMAGE PATH
    image = cv2.imread(image_path)
    orig = image.copy()

    # Convert to grayscale and blur it slightly
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Find edges using the Canny detector
    edged = cv2.Canny(blurred, 75, 200)

    # Uncomment the next line to see the edged image (good for debugging)
    # plt_imshow("Edged", edged)

    # Find contours in the edge map
    cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If any contours were found
    if len(cnts) > 0:
        # Sort the contours by area, largest first
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        # Loop over the sorted contours
        for c in cnts:
            # Approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            # If our approximated contour has four points,
            # we can assume we have found the exam
            if len(approx) == 4:
                docCnt = approx
                break

    # Draw the outline of the exam on the original image
    cv2.drawContours(orig, [docCnt], -1, (0, 255, 0), 3)
    # plt_imshow("Exam Outline", orig)

    # Apply a four point perspective transform to get a top-down view
    def four_point_transform(image, pts):
        # Obtain a consistent order of the points and unpack them
        rect = order_points(pts)
        (tl, tr, br, bl) = rect
        # Compute the width of the new image
        widthA = np.linalg.norm(br - bl)
        widthB = np.linalg.norm(tr - tl)
        maxWidth = max(int(widthA), int(widthB))
        # Compute the height of the new image
        heightA = np.linalg.norm(tr - br)
        heightB = np.linalg.norm(tl - bl)
        maxHeight = max(int(heightA), int(heightB))
        # Construct the set of destination points
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")
        # Compute the perspective transform matrix and apply it
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        return warped

    # Helper function for four_point_transform
    def order_points(pts):
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]  # top-left has smallest sum
        rect[2] = pts[np.argmax(s)]  # bottom-right has largest sum
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]  # top-right has smallest difference
        rect[3] = pts[np.argmax(diff)]  # bottom-left has largest difference
        return rect

    # Apply the transform to get the warped image
    warped = four_point_transform(gray, docCnt.reshape(4, 2))
    # Threshold the warped image to get a binary image (black and white)
    thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    # plt_imshow("Thresholded", thresh)