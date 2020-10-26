from dataclasses import dataclass, field


@dataclass
class Canvas(object):
    height: int
    width: int
    fill: bool = False

    def draw_canvas(self):
        draw = "-" * (self.width + 2)
        for _ in range(self.height+1):
            draw += "\n|" + (" " * self.width) + "|"
        draw += "\n"
        draw += "-" * (self.width + 2)
        return draw


if __name__ == "__main__":
    cv = Canvas(20, 20)
    print(cv.draw_canvas())
