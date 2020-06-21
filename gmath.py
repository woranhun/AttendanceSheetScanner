import math
from collections import defaultdict
from typing import Tuple, List
import cv2
import numpy as np
from PIL import Image
from scipy.spatial import distance
from numpyext import normalize, nparray_to_point

from compvis import ComputerVision

Point = np.ndarray
Quad = Tuple[Point, Point, Point, Point]
Line = Tuple[Point, Point]


class GraphicsMath:

    @staticmethod
    def lerp_point(p1: Point, p2: Point, amount: float) -> Point:
        """Linearly interpolates two points given a factor"""
        return (p2 - p1) * amount + p1

    @staticmethod
    def transform_to_rectangle(img: Image, points: Quad) -> Image:
        """Transforms a quad into a rectangle"""

        # Top points
        sorted_points = sorted(points, key=lambda point: point[1])
        if sorted_points[0][0] < sorted_points[1][0]:
            top_left = sorted_points[0]
            top_right = sorted_points[1]
        else:
            top_left = sorted_points[1]
            top_right = sorted_points[0]

        # Bottom points
        if sorted_points[2][0] < sorted_points[3][0]:
            bottom_left = sorted_points[2]
            bottom_right = sorted_points[3]
        else:
            bottom_left = sorted_points[3]
            bottom_right = sorted_points[2]

        left_len = distance.euclidean(top_left, bottom_left)
        right_len = distance.euclidean(top_right, bottom_right)
        top_len = distance.euclidean(top_left, top_right)
        bottom_len = distance.euclidean(bottom_left, bottom_right)

        long_side_len = math.floor(max(left_len, right_len))
        long_top_len = math.floor(max(top_len, bottom_len))

        input_img = img.convert("RGB")
        output_img = Image.new("RGB", (long_top_len, long_side_len))

        for x in range(long_top_len):
            x_lerp_factor = x / long_top_len

            top_point = GraphicsMath.lerp_point(top_left, top_right, x_lerp_factor)
            bottom_point = GraphicsMath.lerp_point(bottom_left, bottom_right, x_lerp_factor)

            for y in range(long_side_len):
                y_lerp_factor = y / long_side_len

                input_point = GraphicsMath.lerp_point(top_point, bottom_point, y_lerp_factor)
                output_point = (x, y)

                col = input_img.getpixel(nparray_to_point(input_point))
                output_img.putpixel(output_point, col)

        return output_img

    @staticmethod
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

    @staticmethod
    def intersection(line1, line2) -> Point:
        """Finds the intersection of two lines given in Hesse normal form.

        Returns closest integer pixel locations.
        See https://stackoverflow.com/a/383527/5087436
        """
        rho1, theta1 = line1[0]
        rho2, theta2 = line2[0]
        arr = np.array([
            [np.cos(theta1), np.sin(theta1)],
            [np.cos(theta2), np.sin(theta2)]
        ])
        b = np.array([[rho1], [rho2]])
        x0, y0 = np.linalg.solve(arr, b)
        x0, y0 = int(np.round(x0)), int(np.round(y0))
        return np.array([x0, y0])

    @staticmethod
    def segmented_intersections(lines) -> List[Point]:
        """Finds the intersections between groups of lines."""

        intersections = []
        for i, group in enumerate(lines[:-1]):
            for next_group in lines[i + 1:]:
                for line1 in group:
                    for line2 in next_group:
                        intersections.append(GraphicsMath.intersection(line1, line2))

        return intersections

    @staticmethod
    def findLineIntersections(pil_img: Image, eps: float = 10.0) -> List[Point]:
        ret = []
        lines = ComputerVision.imageToHoughLines(pil_img)

        segmented = GraphicsMath.segment_by_angle_kmeans(lines)
        intersecions = GraphicsMath.segmented_intersections(segmented)
        # Ezen kéne még heggeszteni, hogy ne O(n^2) legyen
        for i in range(len(intersecions)):
            for j in range(i + 1, len(intersecions)):
                dist = np.linalg.norm(np.array(intersecions[i]) - np.array(intersecions[j]))
                if dist < eps:
                    break
            else:
                ret.append(intersecions[i])

        return ret

    @staticmethod
    def create_grid_from_points(points: List[Point], eps: float = 5) -> List[Quad]:
        points.sort(key=lambda p: p[1])
        points.sort(key=lambda p: p[0])

        top_left = points.pop(0)

        line = [top_left]
        for i in range(len(points) - 1, 0, -1):
            p = points[i]
            if np.abs(top_left[1] - p[1]) < eps:
                line.append(points.pop(i))

        line.sort(key=lambda p: p[0])

        grid = []
        for top_point in line:
            vertical_line = [top_point]

            for p in points:
                if np.abs(top_point[0] - p[0]) < eps:
                    vertical_line.append(p)

            grid.append(vertical_line)

        quads = []
        for x in range(len(grid) - 1):
            for y in range(len(grid[x]) - 1):
                p1 = grid[x][y]
                p2 = grid[x][y + 1]
                p3 = grid[x + 1][y + 1]
                p4 = grid[x + 1][y]
                quads.append((p1, p2, p3, p4))

        return quads
