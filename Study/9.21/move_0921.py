from pico2d import *
from gobj import *


def handle_event(): # 함수를 만드는 이유: 추상화, 반복사용
	global running
	evts = get_events()
	for e in evts:
		if e.type == SDL_QUIT:
			running = False
		elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
			running = False


open_canvas()

# type name = UpperCamelCase
# method name = lowerCamelCase
grass = Grass()
team = [ Boy() for i in range(11) ]


# boy = Boy(0, 85, 2)
# b2 = Boy(get_canvas_width(), 200, -2)

running = True

hide_cursor()
while running:
	clear_canvas()

	grass.draw()
	for boy in team:
		boy.draw()

	update_canvas()

	handle_event()
	
	for boy in team:
		boy.update()

	delay(0.02)

close_canvas()

# GameLoop
# rendering = draw
# logic = update

# 이벤트 드리븐 = 내가 주도권 X andorid ios
# - 2가지 종류: 아무 이벤트 발생 -> 나에게 알림
# - 			키가 눌리면 발생 

# 폴링 = 내가 주도, get_events()
# 큐에 쌓인 이벤트를 꺼내옴
# 이벤트는 리스트 형태

# class = abstract(추상)
# object = instance(실체)
# behavior = operation = member function = method
# attribute = data = member variables = state = field
# 캡슐화(encapsulation) = 속성 + 행위 = data + operation on data = variables + functions
# 상속성(inheritance)
# 다형성(polymorphism)
# Object instantiation(객체생성)