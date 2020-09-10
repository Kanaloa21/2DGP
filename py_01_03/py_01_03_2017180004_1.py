import turtle as t

t.speed(0)
t.penup()

xpos = -280
ypos = 200

def pen_reset():
	t.pendown()
	t.setheading(0)

def draw_giyeok():
	t.goto(xpos, ypos)
	pen_reset()
	t.forward(100)
	t.left(225)
	t.forward(140)
	t.penup()

def draw_i():
	t.goto(xpos + 130, ypos + 20)
	pen_reset()
	t.right(90)
	t.forward(140)
	t.penup()

def draw_under_mieum():
	t.goto(xpos + 130, ypos - 140)
	pen_reset()
	t.right(90)
	for i in range(4):
		 t.forward(80)
		 t.right(90)
	t.penup()

def draw_jieut():
	t.goto(xpos, ypos)
	pen_reset()
	t.forward(100)
	t.backward(50)
	t.left(235)
	t.forward(100)
	t.backward(100)
	t.left(70)
	t.forward(100)
	t.penup()

def draw_ae():
	draw_i()
	draw_eo()
	t.penup()

def draw_ieung():
	t.goto(xpos + 80, ypos)
	pen_reset()
	t.left(180)
	t.circle(50)
	t.penup()

def draw_ueo():
	draw_u()
	draw_eo()
	t.penup()

def draw_u():
	t.goto(xpos + 40, ypos - 130)
	pen_reset()
	t.forward(100)
	t.backward(50)
	t.right(90)
	t.forward(50)
	t.penup()

def draw_eo():
	t.goto(xpos + 170, ypos + 20)
	pen_reset()
	t.right(90)
	t.forward(140)
	t.backward(70)
	t.right(90)
	t.forward(40)
	t.penup()

def draw_under_nieun():
	t.goto(xpos + 50, ypos - 160)
	pen_reset()
	t.right(90)
	t.forward(40)
	t.left(90)
	t.forward(120)
	t.penup()


t.colormode(255)
t.pencolor(0, 255, 255)
t.pensize(5)

draw_giyeok()
draw_i()
draw_under_mieum()

xpos += 180

draw_jieut()
draw_ae()

xpos += 180

draw_ieung()
draw_ueo() 
draw_under_nieun()

t.exitonclick()