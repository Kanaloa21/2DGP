from pico2d import *
import gfw
from gobj import *
from doll import Doll
from select import Select

canvas_width = 1280
canvas_height = 720

def enter():
	gfw.world.init(['bg', 'select', 'doll'])
	gfw.world.add(gfw.layer.bg, ImageObject('background.png', (640,360)))
	
	global select
	select = Select(1)
	gfw.world.add(gfw.layer.select, select)

	global doll
	doll = Doll(1)
	gfw.world.add(gfw.layer.doll, doll)
	pass

def update():
	gfw.world.update()
	pass

def draw():
	gfw.world.draw()
	if capture is not None:
		capture.draw_position()
	pass

def handle_event(e):
	if e.type == SDL_QUIT:
		gfw.quit()
		return
	elif e.type == SDL_KEYDOWN:
		if e.key == SDLK_ESCAPE:
			gfw.pop()
			return

	if handle_mouse(e):
		return

# capture 가 설정되면 모든 마우스 이벤트는 capture 에게 전달된다
capture = None 
# 이벤트가 처리되었으면 True, 아니면 False 를 리턴한다
def handle_mouse(e):
	global capture
	if capture is not None:
		# capture 가 풀리기를 원하면 False 가 리턴된다
		holding = capture.handle_event(e)
		if not holding:
			capture = None
		return True
	for doll in gfw.world.objects_at(gfw.layer.doll):
		if doll.handle_event(e):
			capture = doll
			return True

	return False

def exit():
	pass

if __name__ == '__main__':
	gfw.run_main()
