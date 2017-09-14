import tkinter # built-in Python graphics library
import random
import math

game_objects = []

class Shape():
    def __init__(self, x, y):
        '''Create a new circle at the given x,y point with a random speed, color, and size.'''

        self.x = x
        self.y = y
        self.x_speed = random.randint(-5,5)
        self.y_speed = random.randint(-5,5)
        # this creates a random hex string between #000000 and #ffffff
        # we draw it with an outline, so we'll be able to see it on a white background regardless
        self.color = '#{0:0>6x}'.format(random.randint(00,16**6))
        self.size = random.randint(5,75)

    def update(self, canvas):
        '''Update current location by speed.'''

        self.x += self.x_speed
        self.y += self.y_speed

        global game_objects
        for obj in game_objects:
            if(self.x <= 0 or self.x >= int(canvas['width'])-self.size):
                self.x_speed = -self.x_speed
            if(self.y <= 0 or self.y >= int(canvas['height'])-self.size):
                self.y_speed = -self.y_speed
                
            if((abs((obj.x+obj.size/2)-(self.x+self.size/2))**2 + abs((obj.y+obj.size/2)-(self.y+self.size/2))**2)**.5 <= sum([self.size, obj.size])/2):
                temp_x, temp_y = self.x_speed, self.y_speed
                self.x_speed, self.y_speed = obj.x_speed, obj.y_speed
                obj.x_speed, obj.y_speed = temp_x, temp_y
                
class Circle(Shape):
    def draw(self, canvas):
        '''Draw self on the canvas.'''

        canvas.create_oval(self.x, self.y, self.x + self.size, self.y + self.size,
                           fill=self.color, outline="black")

class Square(Shape):
    def draw(self, canvas):
        '''Draw self on the canvas.'''

        canvas.create_rectangle(self.x, self.y, self.x + self.size, self.y + self.size,
                           fill=self.color, outline="black")


def addShape(event):
    '''Add a new circle where the user clicked.'''

    global game_objects
    options = [Circle(event.x, event.y), Square(event.x, event.y)]
    game_objects.append(random.choice(options))


def reset(event):
    '''Clear all game objects.'''

    global game_objects
    game_objects = []


def draw(canvas):
    '''Clear the canvas, have all game objects update and redraw, then set up the next draw.'''

    canvas.delete(tkinter.ALL)

    global game_objects
    for game_object in game_objects:
        game_object.update(canvas)
        game_object.draw(canvas)

    delay = 33 # milliseconds, so about 30 frames per second
    canvas.after(delay, draw, canvas) # call this draw function with the canvas argument again after the delay

# this is a standard Python thing: definitions go above, and any code that will actually
# run should go into the __main__ section. This way, if someone imports the file because
# they want to use the functions or classes you've defined, it won't start running your game
# automatically
if(__name__ == '__main__'):

    # create the graphics root and a 400x400 canvas
    root = tkinter.Tk()
    canvas = tkinter.Canvas(root, width=400, height=400)
    canvas.pack()
    
    # if the user presses a key or the mouse, call our handlers
    root.bind('<Key-r>', reset)
    root.bind('<Button-1>', addShape)

    # start the draw loop
    draw(canvas)

    root.mainloop() # keep the window open

