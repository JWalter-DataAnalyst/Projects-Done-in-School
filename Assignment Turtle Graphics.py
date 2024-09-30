'''Use turtle graphics and Python to create a graphical landscape. 
1) The bottom half of the screen should be green.
2) The top half of the screen should be blue.
3) Draw grey mountains in the background using triangles.  Create at least 3 mountains of varying sizes.
4) Draw an orange truck with black tires in the foreground.
5) Draw your initials in the bottom right corner.
6) Include these instructions as comments at the beginning of your program.  Also comment each section, i.e. draw mountain, draw truck, etc.
Attach your .py file to Blackboard.  Make sure you attach your .py file and not the .pyproj file.  If you attach the wrong file you will get zero credit.
Don't forget the instructions as comments as well as code comments or you will loose points.'''

#Importing turtle will allow me to start using the commands associated with them
import turtle

#This is for our background as we need one half blue and another green so filling the whole thing blue will remove some of the work
turtle.bgcolor('blue')
turtle.setup(795, 640)
turtle.showturtle
turtle.speed(4)

#this section is for the bottom layer so we can have grass 
turtle.fillcolor('green')
turtle.begin_fill()
turtle.pensize(10)
turtle.pencolor('green')
turtle.pendown
turtle.goto(-390, 0)
turtle.goto(-390, -310)
turtle.goto(390, -310)
turtle.goto(390, 1)
turtle.goto(0,0)
turtle.end_fill()

#this section will be for the grey mountains in the back for the right most mountain
turtle.pencolor('grey')
turtle.fillcolor('grey')
turtle.begin_fill()
turtle.pensize(10)
turtle.penup()
turtle.goto(150,0)
turtle.goto(300, 100)
turtle.goto(400, 0)
turtle.penup()
turtle.goto(0, 0)
turtle.end_fill()

#this section is for the middle mountain
turtle.pencolor('grey')
turtle.fillcolor('grey')
turtle.begin_fill()
turtle.pensize(10)
turtle.goto(120, 0)
turtle.goto(0, 200)
turtle.goto(-20, 0)
turtle.penup()
turtle.goto(0, 0)
turtle.end_fill()

#this section is for the left most mountain
turtle.pencolor('grey')
turtle.fillcolor('grey')
turtle.begin_fill()
turtle.pensize(10)
turtle.goto(-100, 0)
turtle.goto(-370, 250)
turtle.goto(-300, 0)
turtle.penup()
turtle.goto(0, 0)
turtle.end_fill()

#this starts the body of our car
turtle.pensize(5)
turtle.pencolor('orange')
turtle.fillcolor('orange')
turtle.begin_fill()
turtle.pendown()
turtle.goto(100, 0)
turtle.goto(100, -25)
turtle.goto(180, -25)
turtle.goto(180, -60)
turtle.goto(100, -60)
turtle.penup()
turtle.penup()
turtle.pencolor('orange')
turtle.fillcolor('orange')
turtle.goto(100, -60)
turtle.pendown()
turtle.goto(-10, -60)
turtle.end_fill()
turtle.penup()
turtle.pencolor('orange')
turtle.fillcolor('orange')
turtle.begin_fill()
turtle.goto(-10, -60)
turtle.pendown()
turtle.goto(-40, -60)
turtle.goto(-40, -30)
turtle.goto(-20, -30)
turtle.goto(-20, 0)
turtle.goto(10, 0)
turtle.end_fill()

#this is the front tire
turtle.penup()
turtle.pencolor('black')
turtle.goto(-10, -90)
turtle.pendown()
turtle.fillcolor('black')
turtle.begin_fill()
turtle.circle(15)
turtle.goto(-10, -60)
turtle.end_fill()

#this is the back tire
turtle.penup()
turtle.pencolor('black')
turtle.goto(100, -90)
turtle.pendown()
turtle.fillcolor('black')
turtle.begin_fill()
turtle.circle(15)
turtle.end_fill()

#this is for the car window
turtle.penup()
turtle.pencolor('white')
turtle.goto(5, -10)
turtle.pendown()
turtle.fillcolor('white')
turtle.begin_fill()
turtle.goto(40, -10)
turtle.goto(40, -40)
turtle.goto(-10, -40)
turtle.goto(-10, -10)
turtle.goto(5, -10)
turtle.end_fill()
turtle.penup()

#this section is for the initals 
#the first section will be for the "J"
turtle.goto(260, -200)
turtle.pendown()
turtle.pencolor('black')
turtle.right(90)
turtle.forward(70)
turtle.right(90)
turtle.forward(30)
turtle.right(90) 
turtle.forward(30)
turtle.penup()

#this section is for the "W"
turtle.goto(300, -200)
turtle.pendown()
turtle.right(180) 
turtle.forward(70)
turtle.left(160)
turtle.forward(50)
turtle.right(140)
turtle.forward(50)
turtle.left(160)
turtle.forward(70)

#Now to hide the turtle to make the picture look better
turtle.hideturtle()
turtle.done()