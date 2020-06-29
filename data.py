class Student(object):

    def __init__(self, name: str, num_of_lectures: int):
        self.name = name
        self.signs = []
        for class_index in range(num_of_lectures):
            self.signs.append(False)

    def set_signed(self, class_num: int, signed: bool) -> None:
        while len(self.signs) <= class_num:
            self.signs.append(False)
        self.signs[class_num] = signed

    def __str__(self) -> str:
        out = self.name + ";"
        out += ";".join(map(lambda sign: "TRUE" if sign else "FALSE", self.signs))
        return out
