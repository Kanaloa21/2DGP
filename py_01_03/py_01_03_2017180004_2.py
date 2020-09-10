import turtle as t
t.speed(0)

i = 0
while (i <= 5):
	t.penup()
	t.goto(0, i * 100)
	t.pendown()
	t.forward(500)
	i += 1

t.right(90)

j = 5

while (j >= 0):
	t.penup()
	t.goto(j * 100, 500)
	t.pendown()
	t.forward(500)
	j -= 1

t.exitonclick()