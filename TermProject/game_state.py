from pico2d import *
import gfw
from gobj import *
from doll import Doll
from enemy import Enemy
from selection import Selection
from gacha import Gacha
from life import Life

import life_gauge
import enemy_gen
import highscore

canvas_width = 1280
canvas_height = 720

total_enemies = 12

STATE_IN_GAME, STATE_PAUSED, STATE_GAME_OVER, STATE_GAME_CLEAR = range(4)

TEXT_COLOR = (255, 255, 255)

DOLL_NAMES = [
"Grizzly", "C96", "K5", "M950A",
"PA15", "RO635", "UMP9", "K2",
"M4A1", "HK416", "AK12", "R93",
"WA2000", "AA12", "AK15", "RPK16"
]
NAME = ''
DAMAGE = ''
RPM = ''
BOUNDARY = ''

def enter():
	gfw.world.init(['bg' , 'gacha', 'life', 'selection', 'enemy', 'doll', 'ui'])
	gfw.world.add(gfw.layer.bg, ImageObject('background.png', (640,360)))

	global shortbutton, shortbutton_pressed
	shortbutton = gfw.image.load(res('ui/shortbutton.png'))
	shortbutton_pressed = gfw.image.load(res('ui/shortbutton_pressed.png'))

	global music_bg
	music_bg = load_music(res('sound/bg.mp3'))
	music_bg.set_volume(10)

	highscore.load()

	global font_1, font_2
	font_1 = gfw.font.load(res('font/Maplestory Light.ttf'), 20)
	font_2 = gfw.font.load(res('font/LCD2N___.TTF'), 20)

	global cross
	cross = gfw.image.load(res('cross.png'))

	global gacha
	gacha = Gacha()
	gfw.world.add(gfw.layer.gacha, gacha)

	global life
	life = Life()
	gfw.world.add(gfw.layer.life, life)

	global selection
	for name in DOLL_NAMES:
		selection = Selection(name)
		gfw.world.add(gfw.layer.selection, selection)

	life_gauge.load()

	global game_state
	game_state = STATE_IN_GAME

	global helper_image
	helper_image = gfw.image.load(res('helper.png'))

	global game_over_image, game_win_image
	game_over_image = gfw.image.load(res('game_over.png'))
	game_win_image = gfw.image.load(res('game_win.png'))

	start_game()

def start_game():
	global game_state
	game_state = STATE_IN_GAME

	gfw.world.clear_at(gfw.layer.doll)
	gfw.world.clear_at(gfw.layer.enemy)
	gfw.world.remove(highscore)

	music_bg.repeat_play()

def pause_game():
	global game_state
	game_state = STATE_PAUSED
	music_bg.pause()

def resume_game():
	global game_state
	game_state = STATE_IN_GAME
	music_bg.resume()

def end_game():
	global game_state
	game_state = STATE_GAME_OVER
	music_bg.stop()
	highscore.add(life.score)
	gfw.world.add(gfw.layer.ui, highscore)

def clear_game():
	global game_state
	game_state = STATE_GAME_CLEAR
	music_bg.stop()
	highscore.add(life.score)
	gfw.world.add(gfw.layer.ui, highscore)

def update():
	global game_state
	if game_state == STATE_IN_GAME:
		gfw.world.update()
		enemy_gen.update()
		for o in gfw.world.objects_at(gfw.layer.life):
			if o.life_count == 0:
				end_game()
			if o.score >= 500:
				clear_game()
		global time, frame_index

def draw():
	gfw.world.draw()

	global font_1
	font_1.draw(990, 185, NAME, TEXT_COLOR)
	font_1.draw(1090, 275, 'DAMAGE: ' + str(DAMAGE), TEXT_COLOR)
	font_1.draw(1090, 240, 'RPM: ' + str(RPM), TEXT_COLOR)
	font_1.draw(1090, 205, 'RANGE: ' + str(BOUNDARY), TEXT_COLOR)

	global shortbutton, shortbutton_pressed
	for selection in gfw.world.objects_at(gfw.layer.selection):
		if selection.name == NAME:
			selection.dp = True
			if selection.num > 4:
				font_x, font_y = 680, 30
				if selection.pressed == True: 
					shortbutton_pressed.draw(717, 30)
					font_1.draw(font_x, font_y - 3, '제작 가능', TEXT_COLOR)
				else: 
					shortbutton.draw(717, 30)
					if selection.mft[0] and selection.mft[1] and selection.mft[2]:
						font_1.draw(font_x, font_y, '제작 가능', TEXT_COLOR)
					else:
						font_1.draw(font_x, font_y, '제작 불가', TEXT_COLOR)
		else:
			selection.dp = False

	if capture is not None:
		capture.draw_position()
		cross.draw(640,360)

	if game_state == STATE_GAME_OVER:
		x = get_canvas_width() // 2
		y = get_canvas_height() // 2
		game_over_image.draw(x, y)

	if game_state == STATE_GAME_CLEAR:
		x = get_canvas_width() // 2
		y = get_canvas_height() // 2
		game_win_image.draw(x, y)

	if game_state == STATE_PAUSED:
		helper_image.draw(640, 360)

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
			elif game_state == STATE_PAUSED:
				resume_game()
		elif e.key == SDLK_p:
			if game_state == STATE_IN_GAME:
				pause_game()

	if handle_mouse(e):
		return

capture = None 

def handle_mouse(e):
	if (e.type, e.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
		if game_state == STATE_PAUSED: resume_game()
		if pt_in_rect(mouse_xy(e), (990, 80, 1050, 130)):
			pause_game()
		for selection in gfw.world.objects_at(gfw.layer.selection):
			if pt_in_rect(mouse_xy(e), selection.get_bb()):
				global NAME, DAMAGE, RPM, BOUNDARY, ATTACK_FRAME
				NAME = selection.name
				DAMAGE = selection.damage
				RPM = selection.rpm
				BOUNDARY = selection.boundary
				if selection.can_place:
					global doll
					doll = Doll(selection.name, selection.num, selection.damage, selection.rpm, selection.boundary, selection.attack_frame)
					gfw.world.add(gfw.layer.doll, doll)
					selection.placed_count += 1
					print(selection.num,"번 Doll 생성, 총", gfw.world.count_at(gfw.layer.doll), "개")

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

	for selection in gfw.world.objects_at(gfw.layer.selection):
		if selection.dp == True:
			if selection.handle_event(e):
				return True

	return False

def exit():
	global music_bg
	del music_bg

if __name__ == '__main__':
	gfw.run_main()
