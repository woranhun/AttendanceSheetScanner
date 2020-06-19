from PIL import Image
from gmath import GraphicsMath


def run_tests():
    img = Image.open("testImages/quads2.jpg")
    quad = ((341, 46), (243, 894), (1256, 869), (1281, 311))
    output = GraphicsMath.transform_to_rectangle(img, quad)
    output.show(img)


if __name__ == '__main__':
    run_tests()
