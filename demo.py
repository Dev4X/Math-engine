# 8.) if user selects right answer, row*col of operator matrix is +1, else -1
# 9.) We can use this matrix to do ML & work with the engine later on

from Tkinter import *
import random

class Operator(object):
    def __init__(self, canvas):
        self.x = canvas.data.width / 2
        self.y = canvas.data.height / 4

    def drawPlus(self,canvas):
        canvas.create_line(self.x-20,self.y,self.x+20,self.y, fill="black",width=10)
        canvas.create_line(self.x,self.y-20,self.x,self.y+20, fill="black",width=10)

class User(object):
    def __init__(self):
# 2.) Create a user class with answer matrix for each operator (10x10 to start)
        self.n = 10
        matrix = [[0 for x in xrange(self.n)] for y in xrange(self.n)]

class Shape(object):
# 1.) Using Python & Tkinter, create a simple shape class.
    def __init__(self,x,y):
        self.x2, self.y2 = x+10, y+10
        self.x, self.y = x, y

    def draw(self,canvas):
        canvas.create_oval(self.x,self.y,self.x2,self.y2, fill="orange")

def mousePressed(canvas, event):
    canvas.data.mouseX = event.x
    canvas.data.mouseY = event.y
    if(canvas.data.mouseX < canvas.data.width / 2):
        print "Right!"
    else:
        print "Try again"
    redrawAll(canvas)

def redrawAll(canvas):
    canvas.delete(ALL)
    canvas.create_rectangle(0,0,canvas.data.width / 3, canvas.data.height / 2,outline="red",fill="white")
    canvas.create_rectangle(canvas.data.width / 3,0,(2*canvas.data.width) / 3,canvas.data.height / 2,outline="green",fill="white")
    canvas.create_rectangle((2*canvas.data.width)/3,0,canvas.data.width,canvas.data.height/2,outline="red",fill="white")
    canvas.create_rectangle(0,canvas.data.height/2,canvas.data.width/2,canvas.data.height,outline="red",fill="blue")
    canvas.create_rectangle(canvas.data.width/2,canvas.data.height/2,canvas.data.width,canvas.data.height,outline="red",fill="green")
    randomAssign(canvas)
    canvas.data.operator.drawPlus(canvas)

def run():
    root = Tk()
    width, height = 500, 500
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()
    class Struct: pass
    canvas.data = Struct()
    canvas.data.width, canvas.data.height = width, height 
    init(canvas)
    def f(event): mousePressed(canvas, event)
    root.bind("<Button-1>", f)
    root.mainloop()

def init(canvas):
    canvas.create_rectangle(0,0,canvas.data.width / 3, canvas.data.height / 2,outline="red",fill="white")
    canvas.create_rectangle(canvas.data.width / 3,0,(2*canvas.data.width) / 3,canvas.data.height / 2,outline="green",fill="white")
    canvas.create_rectangle((2*canvas.data.width)/3,0,canvas.data.width,canvas.data.height/2,outline="red",fill="white")
    canvas.create_rectangle(0,canvas.data.height/2,canvas.data.width/2,canvas.data.height,outline="red",fill="blue")
    canvas.create_rectangle(canvas.data.width/2,canvas.data.height/2,canvas.data.width,canvas.data.height,outline="red",fill="green")
    canvas.data.user = User()
    canvas.data.operator = Operator(canvas)
    canvas.data.operator.drawPlus(canvas)
    randomAssign(canvas)

def randomAssign(canvas):
# 4.) Randomly select row from matrix, generate that many shapes on left of operator.
# 5.) Randomly select col from matrix, generate that many shapes on right of operator
    n = canvas.data.user.n
    random1 = random.randint(0,n-1)
    random2 = random.randint(0,n-1)
# 7.) Generate answer, display right answer as well as one wrong answer
    answer = random1 + random2
    nonAnswer = random.randint(0,n-1)
    while(nonAnswer == answer):
        nonAnswer = random.randint(0,n-1)
    shapesLeft = [Shape((x*canvas.data.width/3)/(random1+1),((x+1)*canvas.data.height)/2/(random1+1)) for x in xrange(random1)]
    shapesRight = [Shape(canvas.data.width*(2.0/3)+(x*canvas.data.width/3)/(random2+1),((x+1)*canvas.data.height)/2/(random2+1)) for x in xrange(random2)]
    shapesAnswer = [Shape((x*canvas.data.width/2)/(answer+1),(canvas.data.height/2)+((x+1)*canvas.data.height)/2/(answer+1)) for x in xrange(answer)]
    shapesNonAnswer = [Shape(canvas.data.width*(2.0/3)+(x*canvas.data.width/3)/(nonAnswer+1),canvas.data.height/2+((x+1)*canvas.data.height)/2/(nonAnswer+1)) for x in xrange(nonAnswer)]
    drawShapesList(canvas, shapesRight)
    drawShapesList(canvas, shapesLeft)
    drawShapesList(canvas, shapesAnswer)
    drawShapesList(canvas, shapesNonAnswer)

def drawShapesList(canvas, shapesList):
    for shape in shapesList:
        shape.draw(canvas)
    
run()
