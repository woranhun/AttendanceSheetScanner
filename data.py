class Student(object):

    def __init__(self, name: str):
        self.name = name
        self.signs = []

    def set_signed(self, class_num: int, signed: bool) -> None:
        while len(self.signs) <= class_num:
            self.signs.append(False)
        self.signs[class_num] = signed
