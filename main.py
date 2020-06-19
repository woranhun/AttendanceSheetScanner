import cv2
from PIL import Image

from compVision import ComputerVision
from gmath import GraphicsMath


if __name__ == "__main__":
    print(ComputerVision.imageToStr(Image.open('testimg/1.png')))
    print(ComputerVision.imageToLines(Image.open('testimg/2.png')))
    print(GraphicsMath.findLineIntersections(Image.open('testimg/2.png')))
    img = cv2.imread('testimg/2.png')
    for point in GraphicsMath.findLineIntersections(Image.open('testimg/2.png')):
        cv2.circle(img, point, 1, (255, 0, 0), 1)

    cv2.imshow('img', img)
    cv2.waitKey(0)
