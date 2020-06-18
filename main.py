from collections import defaultdict
from typing import Tuple, List

import cv2
import numpy as np
import pytesseract
from PIL import Image

Point = Tuple[int, int]
Quad = Tuple[Point, Point, Point, Point]
Line = Tuple[Point, Point]


def imageToStr(img: Image) -> str:
    ou = pytesseract.image_to_string(img)
    return ou


def imageToHoughLines(pil_img: Image):
    img = np.array(pil_img)[:, :, ::-1].copy()
    out = list()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    return lines


def imageToLines(pil_img: Image) -> List[Line]:
    out = list()
    lines = imageToHoughLines(pil_img)
    for line in lines:
        for rho, theta in line:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            out.append(((x1, y1), (x2, y2)))

    return out


def segment_by_angle_kmeans(lines, k=2, **kwargs):
    """Groups lines based on angle with k-means.

    Uses k-means on the coordinates of the angle on the unit circle
    to segment `k` angles inside `lines`.
    """

    # Define criteria = (type, max_iter, epsilon)
    default_criteria_type = cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER
    criteria = kwargs.get('criteria', (default_criteria_type, 10, 1.0))
    flags = kwargs.get('flags', cv2.KMEANS_RANDOM_CENTERS)
    attempts = kwargs.get('attempts', 10)

    # returns angles in [0, pi] in radians
    angles = np.array([line[0][1] for line in lines])
    # multiply the angles by two and find coordinates of that angle
    pts = np.array([[np.cos(2 * angle), np.sin(2 * angle)]
                    for angle in angles], dtype=np.float32)

    # run kmeans on the coords
    labels, centers = cv2.kmeans(pts, k, None, criteria, attempts, flags)[1:]
    labels = labels.reshape(-1)  # transpose to row vec

    # segment lines based on their kmeans label
    segmented = defaultdict(list)
    for i, line in zip(range(len(lines)), lines):
        segmented[labels[i]].append(line)
    segmented = list(segmented.values())
    return segmented


def intersection(line1, line2):
    """Finds the intersection of two lines given in Hesse normal form.

    Returns closest integer pixel locations.
    See https://stackoverflow.com/a/383527/5087436
    """
    rho1, theta1 = line1[0]
    rho2, theta2 = line2[0]
    A = np.array([
        [np.cos(theta1), np.sin(theta1)],
        [np.cos(theta2), np.sin(theta2)]
    ])
    b = np.array([[rho1], [rho2]])
    x0, y0 = np.linalg.solve(A, b)
    x0, y0 = int(np.round(x0)), int(np.round(y0))
    tup = (x0, y0)
    return tup


def segmented_intersections(lines):
    """Finds the intersections between groups of lines."""

    intersections = []
    for i, group in enumerate(lines[:-1]):
        for next_group in lines[i + 1:]:
            for line1 in group:
                for line2 in next_group:
                    intersections.append(intersection(line1, line2))

    return intersections


def findLineIntersections(pil_img: Image, eps: float = 10.0) -> List[Tuple[int, int]]:
    ret = set()
    lines = imageToHoughLines(pil_img)

    segmented = segment_by_angle_kmeans(lines)
    intersecions = segmented_intersections(segmented)
    # Ezen kéne még heggeszteni, hogy ne O(n^2) legyen
    for i in range(len(intersecions)):
        for j in range(i + 1, len(intersecions)):
            dist = np.linalg.norm(np.array(intersecions[i]) - np.array(intersecions[j]))
            if dist < eps:
                break
        else:
            ret.add(intersecions[i])

    return list(ret)


def findQuadrants(intersections: List[List[Tuple[int, int]]]) -> List[
    Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]]]:
    pass


if __name__ == "__main__":
    print(imageToStr(Image.open('testimg/1.png')))
    print(imageToLines(Image.open('testimg/2.png')))
    print(findLineIntersections(Image.open('testimg/2.png')))
    img = cv2.imread('testimg/2.png')
    for point in findLineIntersections(Image.open('testimg/2.png')):
        cv2.circle(img, point, 1, (255, 0, 0), 1)

    cv2.imshow('img', img)
    cv2.waitKey(0)
