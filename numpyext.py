from typing import Tuple
import numpy as np

Point = np.ndarray
Quad = Tuple[Point, Point, Point, Point]
Line = Tuple[Point, Point]


def normalize(vec: np.ndarray) -> np.ndarray:
    return vec / np.sqrt(np.dot(vec, vec))


def nparray_to_point(arr: np.ndarray) -> Tuple[int, int]:
    return round(arr[0]), round(arr[1])
