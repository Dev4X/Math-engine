#!/usr/bin/env python2
from Tkinter import *
import random

# GLOBALS
COLORS=['blue','green','red','yellow','gray','white','orange']

class Operator(object):
    def __init__(self, canvas):
        self.x = canvas.data.width / 2
        self.y = canvas.data.height / 4

class Plus(Operator):
    def __init__(self, canvas):
        Operator.__init__(self, canvas)

    def draw(self, canvas):
        canvas.create_line(self.x-20,self.y,self.x+20,self.y, fill="black",width=10)
        canvas.create_line(self.x,self.y-20,self.x,self.y+20, fill="black",width=10)

class Minus(Operator):
    def __init__(self, canvas):
        Operator.__init__(self, canvas)

    def draw(self, canvas):
        canvas.create_line(self.x-20,self.y,self.x+20,self.y, fill="black",width=10)

class User(object):
    def __init__(self):
# 2.) Create a user class with answer matrix for each operator (10x10 to start)
# 9.) We can use this matrix to do ML & work with the engine later on
        self.n = 10
        #TODO auth & read in matrix
        self.matrix = [[[0,0] for x in xrange(self.n)] for y in xrange(self.n)]
        self.score = 0

class Shape(object):
# 1.) Using Python & Tkinter, create a simple shape class.
    def __init__(self,x,y):
        self.x2, self.y2 = x+10, y+10
        self.x, self.y = x, y

    def draw(self,canvas):
        color="black"
   #     if(random.random() > .5):
        canvas.create_oval(self.x,self.y,self.x2,self.y2, fill=color)
   #     else:
    #        canvas.create_rectangle(self.x,self.y,self.x2,self.y2, fill=color)

def mousePressed(canvas, event):
    canvas.data.mouseX = event.x
    canvas.data.mouseY = event.y
    if(canvas.data.mouseX < canvas.data.width / 2):
        correct = checkAnswer(canvas, "left")
    else:
        correct = checkAnswer(canvas, "right")
    if(random.random() > .5):
        canvas.data.adding = True
    else:
        canvas.data.adding = False
    writeMatrix(canvas)
    redrawAll(canvas, correct)

def writeMatrix(canvas):
#TODO CRUD matrix
    matrix = open('matrix', 'w+')
    print >>matrix, canvas.data.user.matrix

def checkAnswer(canvas, side):
# 8.) if user selects right answer, row*col of operator matrix is +1, else -1
    #TODO BUG FROM SIMPLE SELECTION
    row = len(canvas.data.shapesLeft)
    col = len(canvas.data.shapesRight)
    if(canvas.data.singleTop == True):
        print canvas.data.answerSide
        if(len(canvas.data.shapesLeft) == len(canvas.data.shapesAnswerLeft)):
            canvas.data.answerSide = "left"
        else:
            canvas.data.answerSide = "right"
    if(side == canvas.data.answerSide):
        #TODO more complex matrix scoring
        if(canvas.data.adding == 1):
            canvas.data.user.matrix[row][col][0] += 1
        else:
            canvas.data.user.matrix[row][col][1] += 1
        canvas.data.user.score += 1
        correct = 1
    else:
        if(canvas.data.adding == 1):
            canvas.data.user.matrix[row][col][0] -= 1
        else:
            canvas.data.user.matrix[row][col][1] -= 1
        canvas.data.user.score -= 1
        correct = 0
    return correct

def drawSmiley(canvas,correct):
    # eyes
    color=COLORS[random.randint(0,len(COLORS)-1)]
    canvas.create_rectangle((canvas.data.width/2)-25,(5*canvas.data.height/8)-25,\
            (canvas.data.width/2)+25,(5*canvas.data.height/8)+35,fill=color)
    canvas.create_oval((canvas.data.width/2)-15,(5*canvas.data.height/8)-15,\
            (canvas.data.width/2)-8,(5*canvas.data.height/8)-8,fill='black')
    canvas.create_oval((canvas.data.width/2)+15,(5*canvas.data.height/8)-15,\
            (canvas.data.width/2)+8,(5*canvas.data.height/8)-8,fill='black')
    # mouth logic
    if(correct == 1):
        canvas.create_arc((canvas.data.width/2)-15,(5*canvas.data.height/8)+25,\
                (canvas.data.width/2)+15,(5*canvas.data.height/8)+10,\
                start=180,extent=180,width=1,outline="black",fill="black")
    else:
        canvas.create_arc((canvas.data.width/2)-15,(5*canvas.data.height/8)+25,\
                (canvas.data.width/2)+15,(5*canvas.data.height/8)+10,\
                start=0,extent=180,width=1,outline="black",fill="black")
    return canvas

def redrawAll(canvas,correct):
    canvas.delete(ALL)
    color1=COLORS[random.randint(0,len(COLORS)-1)]
    color2=COLORS[random.randint(0,len(COLORS)-1)]
    canvas.create_rectangle(0,0,canvas.data.width / 3, canvas.data.height / 2,\
            outline="white",fill="white")
    canvas.create_rectangle(canvas.data.width / 3,0,(2*canvas.data.width) / 3,\
            canvas.data.height / 2,outline="white",fill="white")
    canvas.create_rectangle((2*canvas.data.width)/3,0,canvas.data.width,\
            canvas.data.height/2,outline="white",fill="white")
    canvas.create_rectangle(0,canvas.data.height/2,canvas.data.width/2,\
            canvas.data.height,fill=color2)
    canvas.create_rectangle(canvas.data.width/2,canvas.data.height/2,\
            canvas.data.width,canvas.data.height,fill=color1)
    canvas.data.shapesLeft, canvas.data.shapesRight, canvas.data.answerSide = \
            randomAssign(canvas)
    drawSmiley(canvas, correct)
    canvas.create_text(10,10,anchor='nw',text=canvas.data.user.score,fill="black")

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

def checkAdditionOrSubtraction(canvas, random1, random2):
    if(canvas.data.adding == 1):
        canvas.data.operator = Plus(canvas)
        answer = random1 + random2
    else:
        canvas.data.operator = Minus(canvas)
        answer = max(random1,random2) - min(random1,random2)
    return answer, canvas

def init(canvas):
    canvas.data.singleTop = True
    canvas.data.user = User()
    canvas.data.adding = True
    canvas.data.operator = Plus(canvas)
    redrawAll(canvas,1)

def generateRandoms(canvas):
# 4.) Randomly select row from matrix, generate that many shapes on left of operator.
# 5.) Randomly select col from matrix, generate that many shapes on right of operator
    n = canvas.data.user.n
    random1 = random.randint(0,n-1)
    random2 = random.randint(0,n-1)
    random3 = random.random()
# 7.) Generate answer, display right answer as well as one wrong answer
    answer, canvas = checkAdditionOrSubtraction(canvas, random1, random2)
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
    shapesLeft, shapesRight, answer = \
            buildShapesList(canvas,random1,random2,answer,answerLeft,answerRight)
    return shapesLeft, shapesRight, answer

def drawNumeral(canvas,x1,y1,text):
    canvas.create_text(x1,y1,\
            anchor='center',text=text,fill='black',font="Arial 45")
    return

def drawNumerals(canvas,random1,random2,answerLeft,answerRight):
    if(canvas.data.adding == 0):
        random1, random2 = max(random1, random2), min(random1, random2)
    canvas.create_text((canvas.data.width/4),(canvas.data.height/4),\
            anchor='center',text=random1,fill='black',font="Arial 45")
    canvas.create_text((3*canvas.data.width/4),(canvas.data.height/4),\
            anchor='center',text=random2,fill='black',font="Arial 45")
    canvas.create_text((canvas.data.width/4),(3*canvas.data.height/4),\
            anchor='center',text=answerLeft,fill='black',font="Arial 45")
    canvas.create_text((3*canvas.data.width/4),(3*canvas.data.height/4),\
            anchor='center',text=answerRight,fill='black',font="Arial 45")
    return

def buildShapesList(canvas,random1,random2,answer,answerLeft,answerRight):
    # not efficient to build list, then check for usage or not
    #TODO move scoring logic outside this function
    canvas.data.shapesAnswerRight =[Shape((2.0*canvas.data.width/(3.0)+((canvas.data.width/12)*(x%2)))\
            ,((x*canvas.data.height)/4/(answerRight))+(2.0*canvas.data.height/3)) \
            for x in xrange(answerRight)]
    canvas.data.shapesAnswerLeft = [Shape(((canvas.data.width/6)+((canvas.data.width/12)*(x%2)))\
            ,((x*canvas.data.height)/4/(answerLeft))+(2.0*canvas.data.height/3)) \
            for x in xrange(answerLeft)]
    shapesAnswerLeft, shapesAnswerRight = canvas.data.shapesAnswerLeft, canvas.data.shapesAnswerRight
    if(canvas.data.adding == 1):
        shapesLeft = [Shape(((canvas.data.width/6)+((canvas.data.width/12)*(x%2)))\
                ,((x*canvas.data.height)/4/(random1))+(canvas.data.height/10)) \
                for x in xrange(random1)]
        shapesRight = [Shape((2.0*canvas.data.width/(3.0)+((canvas.data.width/12)*(x%2)))\
                ,((x*canvas.data.height)/4/(random2))+(canvas.data.height/10)) \
                for x in xrange(random2)]
    else:
        shapesLeft = [Shape(((canvas.data.width/6)+((canvas.data.width/12)*(x%2)))\
                ,((x*canvas.data.height)/4/(max(random1,random2)))+(canvas.data.height/10)) \
                for x in xrange(max(random1,random2))]
        shapesRight = [Shape((2.0*canvas.data.width/(3.0)+((canvas.data.width/12)*(x%2)))\
                ,((x*canvas.data.height)/4/(min(random2,random1)))+(canvas.data.height/10)) \
                for x in xrange(min(random2,random1))]

    # threshold of score to unlock numerals
#    if(canvas.data.user.score < 5):
#        canvas.data.singleTop = True
#        drawNumeral(canvas,canvas.data.width/4,canvas.data.height/4,len(shapesLeft))
#        drawShapesList(canvas, shapesAnswerLeft)
#        drawShapesList(canvas, shapesAnswerRight)
#        #   generate 2 numbers
#        #   one dot pattern
#        #   match
#    elif(canvas.data.user.score < 8):
#        canvas.data.singleTop = False
#        if(random.random() > .5):
#            drawShapesList(canvas, shapesLeft)
#        else:
#            drawShapesList(canvas, shapesRight)
#        drawNumeral(canvas,canvas.data.width/4,3*canvas.data.height/4,len(shapesLeft))
#        drawNumeral(canvas,3*canvas.data.width/4,3*canvas.data.height/4,len(shapesRight))
#        #TODO hybrid between pictures & numbers (answers)
#        #TODO match numbers with pictures
#        #   1. generate one number
#        #   do not draw operator
#        #   instead draw in operator's place
#        #   can use same answer code
#        #   2. generate 2 dot patterns
#        #   3. match them
    if(canvas.data.user.score < 10):
        canvas.data.singleTop = False
        drawShapesList(canvas, shapesRight)
        drawShapesList(canvas, shapesLeft)
        drawShapesList(canvas, shapesAnswerLeft)
        drawShapesList(canvas, shapesAnswerRight)
        canvas.data.operator.draw(canvas)
    elif(canvas.data.user.score < 15):
        canvas.data.singleTop = False
        random1 = random.random()
        if(random1 >= .5):
            drawShapesList(canvas, shapesRight)
            drawShapesList(canvas, shapesAnswerLeft)
            drawShapesList(canvas, shapesAnswerRight)
            drawNumeral(canvas,canvas.data.width/4,canvas.data.height/4,len(shapesLeft))
        else:
            drawShapesList(canvas, shapesLeft)
            drawShapesList(canvas, shapesAnswerLeft)
            drawShapesList(canvas, shapesAnswerRight)
            drawNumeral(canvas,3*canvas.data.width/4,canvas.data.height/4,len(shapesRight))
        canvas.data.operator.draw(canvas)
    else:
        drawNumerals(canvas,random1,random2,answerLeft,answerRight)
        canvas.data.operator.draw(canvas)
    return shapesLeft, shapesRight, answer

def drawShapesList(canvas, shapesList):
    for shape in shapesList:
        shape.draw(canvas)
    
run()
