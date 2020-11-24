from pico2d import *
import gfw
from gobj import *
from doll import Doll
from enemy import Enemy
from select import Select
from ui import Ui
import life_gauge
import enemy_gen

canvas_width = 1280
canvas_height = 720
total_enemies = 12

def enter():
	gfw.world.init(['bg' , 'ui', 'select', 'enemy', 'doll'])
	gfw.world.add(gfw.layer.bg, ImageObject('realbackground.png', (640,360)))
	global cross
	cross = gfw.image.load('res/cross.png')

	global ui
	ui = Ui()
	gfw.world.add(gfw.layer.ui, ui)

	global select
	for i in range(5):
		select = Select(i)
		gfw.world.add(gfw.layer.select, select)
		print(*select.pos)

	life_gauge.load()
	pass

def update():
	gfw.world.update()
	enemy_gen.update()

	pass

def draw():
	gfw.world.draw()
	if capture is not None:
		capture.draw_position()
		cross.draw(640,360)
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
	pass

# capture 가 설정되면 모든 마우스 이벤트는 capture 에게 전달된다
capture = None 
# 이벤트가 처리되었으면 True, 아니면 False 를 리턴한다
def handle_mouse(e):
	if (e.type, e.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
		for select in gfw.world.objects_at(gfw.layer.select):
			if pt_in_rect(mouse_xy(e), select.get_bb()) & select.can_place :
				global doll
				doll = Doll(select.num)
				gfw.world.add(gfw.layer.doll, doll)
				select.placed_count += 1
				print(select.num,"번 Doll 생성, 총", gfw.world.count_at(gfw.layer.doll), "개")

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

	if ui.handle_event(e):
		return True

	return False
	pass

def exit():
	pass

if __name__ == '__main__':
	gfw.run_main()
