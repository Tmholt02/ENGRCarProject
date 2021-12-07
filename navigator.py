# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Thomas Holt, Austin Wheeler, Jacob Kimbrough, Tanner Kotara
# Section:      464
# Assignment:   Car Lab
# Date:         12/07/2021

"""This is the legendary navigation software!"""

import turtle
import tkinter as tk


######################################################################################


class Instruction:
    """Stores and interprets instructions that appear in
    formatted input files."""

    def set_distance(self, dist_str: str, unit: str):
        """Reassigns the value of dist to what is in the parameters.
        if the unit is 'mi', it will be converted to ft

        :param str dist_str: magnitude of the new distance
        :param str unit: original unit
        """

        self.dist = float(dist_str)
        if unit == "mi":
            self.dist *= 5280

    def set_time(self, time_str: str, unit: str):
        """Reassigns the value of time to what is in the parameters.
        if the unit is 'min', it will be converted to seconds

        :param time_str: magnitude of the new time
        :param unit: original unit
        """

        self.time = float(time_str)
        if unit == "min":
            self.time *= 60

    def __init__(self, string: str):
        """Initialize a new Instruction

        :param string: Instructions based on a single
                       entry from an instruction file
        """

        self.lines: list
        self.dist: float = 0
        self.time: float = 0
        self.angle: int = 0
        self.cardinal_angle: bool = False

        self.lines = string.strip('\n').split('\n')

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


class Main:
    """This class stores data used by the tkinter frame's wigets.
    It also serves as the starting point of the program
    """

    __root:          tk.Tk
    __canvas:        tk.Canvas
    __screen:        turtle.TurtleScreen
    __start_button:  tk.Button
    __text:          tk.Text
    __label:         tk.Label
    __next_button:   tk.Button
    __artist:        turtle.RawTurtle
    __instructions:  list
    __busy:          bool = False
    __press_cnt:     int

    @classmethod
    def main(cls):
        """Launch the navigation software. This will make a new window
        and populate it with its widgets to take first input from the user.
        The __start_button will launch the next section IF the file is found.
        Otherwise, nothing will happen.
        """

        # Initialize the frame root
        cls.__root = tk.Tk()
        cls.__root.title("Navigation Software Pro Edition")
        cls.__root.configure(background='black')
        cls.__root.resizable(height=False, width=False)

        # Text box for reading file name
        cls.__text = tk.Text(cls.__root, width=30, height=1)
        cls.__text.pack(side=tk.LEFT)

        # This button will trigger the second part, and will read the text
        cls.__start_button = tk.Button(cls.__root, text="  Start  ", command=cls.__setup)
        cls.__start_button.pack(side=tk.RIGHT)

        # Start the window
        cls.__root.mainloop()

    @classmethod
    def __setup(cls):
        """Set up the navigation portion of the program. If the file isn't found,
        nothing will happen. This populates the __root with new content. The
        __next_button will display the next navigational step with both a turtle
        and a helpful message.
        """
        # Try to open the file. If we cant, its a lie, move on
        file_name = "unread_file"
        try:
            file_name = cls.__text.get("1.0", "end-1c")
            file = open(file_name, 'r')
        except FileNotFoundError:
            print("ERROR! " + file_name + " not found")
            return

        # Get rid of some old stuff
        cls.__start_button.destroy()
        cls.__text.destroy()

        # This is where the turtle will draw
        cls.__canvas = tk.Canvas(cls.__root)
        cls.__canvas.config(width=800, height=600)
        cls.__canvas.pack(side=tk.TOP)

        # This is where the turtle will exist
        cls.__screen = turtle.TurtleScreen(cls.__canvas)
        cls.__screen.bgcolor("grey")

        # Next button displays next step using the next method.
        # Keep track of presses
        cls.__press_cnt = 0
        cls.__next_button = tk.Button(cls.__root, text="  Next  ", command=cls.__next)
        cls.__next_button.pack(side=tk.LEFT)

        # This will display instructions
        cls.__label = tk.Label(cls.__root, text="...",
                               font=("Comic Sans MS", 9, "normal"),
                               background="black",
                               foreground="white")
        cls.__label.pack(side=tk.RIGHT)

        # Put an artist into the screen
        cls.__artist = turtle.RawTurtle(cls.__screen, shape="classic")

        # Read all instructions from the file
        cls.__instructions = []
        for instruction_string in file.read().split("\n\n"):
            cls.__instructions.append(Instruction(instruction_string))

        # Configure our artist to where they need to be and how to draw
        cls.__artist.penup()
        cls.__artist.goto(-100, +100)
        cls.__artist.pendown()
        cls.__artist.pensize(2)

    @classmethod
    def __next(cls):
        """Display the following instruction for the user to see. Updates the
        turtle and the label"""
        # Makeshift thread safety. busy is True if this method is in use
        # We also shouldn't execute if we're out of instructions to follow
        if cls.__busy or cls.__press_cnt >= len(cls.__instructions):
            return

        # We are using this method
        cls.__busy = True

        # Find the correct instruction and increment the counter
        # Display the new instruction
        instruction = cls.__instructions[cls.__press_cnt]
        cls.__label.config(text="\n".join(instruction.lines))
        cls.__press_cnt += 1

        # Turn according to visible data
        if instruction.cardinal_angle:
            cls.__artist.setheading(instruction.angle)
        else:
            cls.__artist.left(instruction.angle)

        # Move the appropriate distance
        cls.__artist.forward(instruction.dist / 200)

        # We're done here, another thread may use this
        cls.__busy = False


######################################################################################


# This is a script
if __name__ == "__main__":
    Main.main()
