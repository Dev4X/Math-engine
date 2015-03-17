#!/usr/bin/env python2
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
# 9.) We can use this matrix to do ML & work with the engine later on
# @TODO CRUD matrix
        self.n = 10
        self.matrix = [[0 for x in xrange(self.n)] for y in xrange(self.n)]

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
        correct = checkAnswer(canvas, "left")
    else:
        correct = checkAnswer(canvas, "right")
    redrawAll(canvas, correct)

def checkAnswer(canvas, side):
# 8.) if user selects right answer, row*col of operator matrix is +1, else -1
    row = len(canvas.data.shapesLeft)
    col = len(canvas.data.shapesRight)
    if(side == canvas.data.answerSide):
        canvas.data.user.matrix[row][col] += 1
        correct = 1
        #@TODO smiley feedback
        #@TODO comparing against next answer, not previous
    else:
        canvas.data.user.matrix[row][col] -= 1
        correct = 0
    return correct

def drawSmiley(canvas,correct):
    # eyes
    canvas.create_oval((canvas.data.width/2)-15,(3*canvas.data.height/8)-15,(canvas.data.width/2)-8,(3*canvas.data.height/8)-8,fill='black')
    canvas.create_oval((canvas.data.width/2)+15,(3*canvas.data.height/8)-15,(canvas.data.width/2)+8,(3*canvas.data.height/8)-8,fill='black')
    # mouth logic
    if(correct == 1):
        canvas.create_arc((canvas.data.width/2)-15,(3*canvas.data.height/8)+25,(canvas.data.width/2)+15,(3*canvas.data.height/8)+10,start=180,extent=180,width=2,outline="black")
    else:
        canvas.create_arc((canvas.data.width/2)-15,(3*canvas.data.height/8)+25,(canvas.data.width/2)+15,(3*canvas.data.height/8)+10,start=0,extent=180,width=2,outline="black")
    return canvas

def redrawAll(canvas,correct):
    canvas.delete(ALL)
    canvas.create_rectangle(0,0,canvas.data.width / 3, canvas.data.height / 2,outline="red",fill="white")
    canvas.create_rectangle(canvas.data.width / 3,0,(2*canvas.data.width) / 3,canvas.data.height / 2,outline="green",fill="white")
    canvas.create_rectangle((2*canvas.data.width)/3,0,canvas.data.width,canvas.data.height/2,outline="red",fill="white")
    canvas.create_rectangle(0,canvas.data.height/2,canvas.data.width/2,canvas.data.height,outline="red",fill="blue")
    canvas.create_rectangle(canvas.data.width/2,canvas.data.height/2,canvas.data.width,canvas.data.height,outline="red",fill="green")
    canvas.data.shapesLeft, canvas.data.shapesRight, canvas.data.answerSide = randomAssign(canvas)
    canvas.data.operator.drawPlus(canvas)
    drawSmiley(canvas, correct)

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
    canvas.data.user = User()
    canvas.data.operator = Operator(canvas)
    redrawAll(canvas,1)

def generateRandoms(canvas):
# 4.) Randomly select row from matrix, generate that many shapes on left of operator.
# 5.) Randomly select col from matrix, generate that many shapes on right of operator
    n = canvas.data.user.n
    random1 = random.randint(0,n-1)
    random2 = random.randint(0,n-1)
    random3 = random.random()
# 7.) Generate answer, display right answer as well as one wrong answer
    answer = random1 + random2
    nonAnswer = random.randint(0,(2*n)-1)
    while(nonAnswer == answer):
        nonAnswer = random.randint(0,(2*n)-1)
    return random1, random2, answer, nonAnswer, random3

def randomAssign(canvas):
    random1, random2, answer, nonAnswer, random3 = generateRandoms(canvas)
    if(random3 > .5):
        answerLeft = answer
        answerRight = nonAnswer
        answer = "left"
    else:
        answerLeft = nonAnswer
        answerRight = answer
        answer = "right"
        #@TODO threshold of score to unlock numerals
    shapesLeft = [Shape((x*canvas.data.width/3)/(random1+1),((x+1)*canvas.data.height)/2/(random1+1)) for x in xrange(random1)]
    shapesRight = [Shape(canvas.data.width*(2.0/3)+(x*canvas.data.width/3)/(random2+1),((x+1)*canvas.data.height)/2/(random2+1)) for x in xrange(random2)]
    shapesAnswerLeft = [Shape((x*canvas.data.width/2)/(answerLeft+1),(canvas.data.height/2)+((x+1)*canvas.data.height)/2/(answerLeft+1)) for x in xrange(answerLeft)]
    shapesAnswerRight = [Shape(canvas.data.width*(1.0/2)+(x*canvas.data.width/2)/(answerRight+1),canvas.data.height/2+((x+1)*canvas.data.height)/2/(answerRight+1)) for x in xrange(answerRight)]
    drawShapesList(canvas, shapesRight)
    drawShapesList(canvas, shapesLeft)
    drawShapesList(canvas, shapesAnswerLeft)
    drawShapesList(canvas, shapesAnswerRight)
    return shapesLeft, shapesRight, answer

def drawShapesList(canvas, shapesList):
    for shape in shapesList:
        shape.draw(canvas)
    
run()
