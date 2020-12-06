from pico2d import *
import gfw
from gobj import *
from doll import Doll
from enemy import Enemy
from select import Select
from gacha import Gacha
from life import Life
import life_gauge
import enemy_gen

canvas_width = 1280
canvas_height = 720

total_enemies = 12

STATE_IN_GAME, STATE_PAUSED, STATE_GAME_OVER = range(3)
TEXT_COLOR = (255, 255, 255)

DOLL_NAMES = [
"Grizzly", "C96", "K5", "M950A", "PA15",
"RO635", "UMP9", "K2", "M4A1", "HK416", "AK12", "R93", "WA2000"
]
NAME = ''
DAMAGE = ''
RPM = ''
BOUNDARY = ''
ATTACK_FRAME = ''
def enter():
	gfw.world.init(['bg' , 'gacha', 'life', 'select', 'enemy', 'doll'])
	gfw.world.add(gfw.layer.bg, ImageObject('background.png', (640,360)))

	global font_1, font_2
	font_1 = gfw.font.load(res('Maplestory Light.ttf'), 20)
	font_2 = gfw.font.load(res('LCD2N___.TTF'), 20)

	global cross
	cross = gfw.image.load('res/cross.png')

	global gacha
	gacha = Gacha()
	gfw.world.add(gfw.layer.gacha, gacha)

	global life
	life = Life()
	gfw.world.add(gfw.layer.life, life)

	global select
	for name in DOLL_NAMES:
		select = Select(name)
		gfw.world.add(gfw.layer.select, select)
		print(*select.pos)

	life_gauge.load()

	global game_state
	game_state = STATE_IN_GAME
	global game_over_image
	game_over_image = gfw.image.load('res/game_over.png')

	start_game()

	pass
def start_game():
	global game_state
	game_state = STATE_IN_GAME

	#player.reset()
	gfw.world.clear_at(gfw.layer.doll)
	gfw.world.clear_at(gfw.layer.enemy)
	#gfw.world.remove(highscore)

	#music_bg.repeat_play()
def end_game():
	global game_state
	game_state = STATE_GAME_OVER
	#music_bg.stop()
	#highscore.add(player.score)
	#gfw.world.add(gfw.layer.ui, highscore)

def update():
	gfw.world.update()
	enemy_gen.update()
	for o in gfw.world.objects_at(gfw.layer.life):
		if o.life_count == 0:
			end_game()
	global time, frame_index
	
	pass

def draw():
	gfw.world.draw()

	global font_1
	font_1.draw(990, 185, NAME, TEXT_COLOR)
	font_1.draw(1090, 275, 'DAMAGE: ' + str(DAMAGE), TEXT_COLOR)
	font_1.draw(1090, 240, 'RPM: ' + str(RPM), TEXT_COLOR)
	font_1.draw(1090, 205, 'RANGE: ' + str(BOUNDARY), TEXT_COLOR)
	global time, frame_index
	for select in gfw.world.objects_at(gfw.layer.select):
		if select.name == NAME: select.dp = True
		else: select.dp = False

	if capture is not None:
		capture.draw_position()
		cross.draw(640,360)

	if game_state == STATE_GAME_OVER:
		x = get_canvas_width() // 2
		y = get_canvas_height() * 2 // 3
		game_over_image.draw(x, y)
	pass

def handle_event(e):
	if e.type == SDL_QUIT:
		gfw.quit()
		return
	elif e.type == SDL_KEYDOWN:
		if e.key == SDLK_ESCAPE:
			gfw.pop()
		elif e.key == SDLK_RETURN:
			if game_state == STATE_GAME_OVER:
				start_game()

	if handle_mouse(e):
		return
	pass



# capture 가 설정되면 모든 마우스 이벤트는 capture 에게 전달된다
capture = None 
# 이벤트가 처리되었으면 True, 아니면 False 를 리턴한다
def handle_mouse(e):
	if (e.type, e.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
		for select in gfw.world.objects_at(gfw.layer.select):
			if pt_in_rect(mouse_xy(e), select.get_bb()):
				global NAME, DAMAGE, RPM, BOUNDARY, ATTACK_FRAME
				NAME = select.name
				DAMAGE = select.damage
				RPM = select.rpm
				BOUNDARY = select.boundary
				ATTACK_FRAME = select.attack_frame
				if select.can_place:
					global doll
					doll = Doll(select.name, select.num, select.damage, select.rpm, select.boundary, select.attack_frame)
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

	if gacha.handle_event(e):
		return True

	return False
	pass

def exit():
	pass

if __name__ == '__main__':
	gfw.run_main()
