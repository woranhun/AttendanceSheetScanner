from typing import Tuple, Generator
from PIL import Image
import math
import numpy as np
from scipy.spatial import distance

Point = Tuple[int, int]
Quad = Tuple[Point, Point, Point, Point]
Line = Tuple[Point, Point]


class GraphicsMath:
    @staticmethod
    def __sign(n: float) -> float:
        if n > 0:
            return 1
        elif n < 0:
            return -1
        else:
            return 0

    @staticmethod
    def lerp_point(p1: Point, p2: Point, amount: float) -> Point:
        return (
            round((p2[0] - p1[0]) * amount + p1[0]),
            round((p2[1] - p1[1]) * amount + p1[1])
        )

    @staticmethod
    def bresenhams_line(p1: Point, p2: Point) -> Generator[Point, None, None]:
        deltax = p2[0] - p1[0]
        deltay = p2[1] - p1[1]
        delta_err = abs(deltay / deltax)
        err = 0
        y = p1[1]
        for x in range(p1[0], p2[0]):
            yield x, y
            err = err + delta_err
            if err > 0.5:
                y = y + GraphicsMath.__sign(deltay) + 1
                err = err - 1

    @staticmethod
    def transform_to_rectangle(img: Image, points: Quad) -> Image:
        """Transforms a quad into a rectangle"""
        # p1 - p3 and p2 - p4 form a line
        sorted_points = sorted(points, key=lambda point: point[1])
        p1 = sorted_points[0]
        p2 = sorted_points[1]
        if sorted_points[0][0] < sorted_points[1][0]:
            top_left = sorted_points[0]
            top_right = sorted_points[1]
        else:
            top_left = sorted_points[1]
            top_right = sorted_points[0]

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

        long_side_len = max(left_len, right_len)
        long_top_len = max(top_len, bottom_len)

        input_img = img.convert("RGB")
        output_img = Image.new("RGB", (math.ceil(long_top_len), math.ceil(long_side_len)))

        for x in range(math.floor(long_top_len)):
            x_lerp_factor = x / long_top_len

            top_point = GraphicsMath.lerp_point(top_left, top_right, x_lerp_factor)
            bottom_point = GraphicsMath.lerp_point(bottom_left, bottom_right, x_lerp_factor)

            for y in range(math.floor(long_side_len)):
                y_lerp_factor = y / long_side_len

                input_point = GraphicsMath.lerp_point(top_point, bottom_point, y_lerp_factor)
                output_point = (x, y)

                col = input_img.getpixel(input_point)
                output_img.putpixel(output_point, col)

        return output_img
