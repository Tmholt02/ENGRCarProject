# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Thomas Holt
# Section:      464
# Assignment:   Car Lab
# Date:         11/23/2021

import turtle


class Instruction:

    def set_distance(self, dist_str: str, unit: str):
        self.dist = float(dist_str)
        if unit == "mi":
            self.dist *= 5280

    def set_time(self, time_str: str, unit: str):
        self.time = float(time_str)
        if unit == "min":
            self.time *= 60

    def __init__(self, string: str):
        self.lines: list
        self.dist: float = 0
        self.time: float = 0
        self.angle: int = 0
        self.cardinal_angle: bool = False

        self.lines = string.split('\n')
        if self.lines[-1] == "":
            del self.lines[-1]

        print("--------\n" + string + "\n--------")

        # This will be used to determine distance and time
        line_last = self.lines[-1].split(' ')

        # If there are time units
        if len(line_last) == 4:
            line_last[2] = line_last[2].replace('(', "")
            line_last[3] = line_last[3].replace(')', "")
            self.set_time(line_last[0], line_last[1])
            self.set_distance(line_last[2], line_last[3])

        # If there arent time units
        else:
            print(line_last)
            self.set_distance(line_last[0], line_last[1])

        # Parse Angle from the first
        line1 = self.lines[0].split(' ')

        if line1[0] == "Turn":
            if line1[1] == "right":
                self.angle = -90
            elif line1[1] == "left":
                self.angle = 90

        elif line1[0] == "Slight":
            if line1[1] == "right":
                self.angle = -45
            elif line1[1] == "left":
                self.angle = 45

        elif line1[0] == "Head":
            self.cardinal_angle = True
            if line1[1] == "north":
                self.angle = 90
            elif line1[1] == "northeast":
                self.angle = 45
            elif line1[1] == "east":
                self.angle = 0
            elif line1[1] == "southeast":
                self.angle = -45
            elif line1[1] == "south":
                self.angle = -90
            elif line1[1] == "southwest":
                self.angle = -135
            elif line1[1] == "west":
                self.angle = 180
            elif line1[1] == "northwest":
                self.angle = 135

    def __str__(self):
        return f"[{self.dist=}, {self.time=}, {self.angle=}, {self.cardinal_angle=}]"


######################################################################################


def main():
    frame = turtle.Screen()
    artist = turtle.Turtle()
    artist.setheading(90)

    file = open("Easterwood2Coulter.txt", 'r')
    instructions = []

    for instruction_string in file.read().split("\n\n"):
        instructions.append(Instruction(instruction_string))
        print()

    for i in instructions:
        print(i.lines)
        if i.cardinal_angle:
            artist.setheading(i.angle)
        else:
            artist.left(i.angle)
        artist.forward(i.dist / 200)

    input()


if __name__ == "__main__":
    main()
