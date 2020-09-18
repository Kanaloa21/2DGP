from pico2d import *
import os
tmp = os.getcwd()
print(tmp)
tmp = os.listdir()
print(tmp)


def handle_event(): # 함수를 만드는 이유: 추상화, 반복사용
	global running, dx, x, y
	# 쓰기의 경우 local 변수로 동작, 읽기는 가능
	# global 사용으로 전역 변수로 지정
	evts = get_events()
	for e in evts:
		if e.type == SDL_QUIT:
			running = False
		elif e.type == SDL_KEYDOWN:
			if e.key == SDLK_ESCAPE:
				running = False
			elif e.key == SDLK_LEFT:
				dx -= 1 	#이건 global로 설정 안하면 초기화 안된 지역변수로 간주함
			elif e.key == SDLK_RIGHT:
				dx += 1
			print('keydown', dx)
		elif e.type == SDL_KEYUP:
			if e.key == SDLK_LEFT:
				dx += 1
			elif e.key == SDLK_RIGHT:
				dx -= 1
			print('keyup', dx)
		elif e.type == SDL_MOUSEMOTION:
			x, y = e.x, get_canvas_height() - e.y - 1
			print('(%d, %d)' %(x, y))


open_canvas()

gra = load_image("grass.png")
ch = load_image("run_animation.png")

running = True
x, y = 400, 85
dx = 0
fidx = 0
hide_cursor()
while running:
	clear_canvas()
	gra.draw(400, 30)
	ch.clip_draw(fidx * 100, 0, -100, -100, x, y)
	update_canvas()

	handle_event()
	
	x += dx * 5
	fidx = (fidx + 1) % 8

	delay(0.01)

close_canvas()

# GameLoop
# rendering = draw
# logic = update

# 이벤트 드리븐 = 내가 주도권X andorid ios
# - 2가지 종류: 아무 이벤트 발생 -> 나에게 알림
# - 			키가 눌리면 발생 

# 폴링 = 내가 주도, get_events()
# 큐에 쌓인 이벤트를 꺼내옴
# 이벤트는 리스트 형태

