from pico2d import *
import gfw
from gobj import *

LBTN_DOWN = (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT)
LBTN_UP   = (SDL_MOUSEBUTTONUP,   SDL_BUTTON_LEFT)
RBTN_DOWN = (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_RIGHT)
KEYDN_DEL = (SDL_KEYDOWN, SDLK_DELETE)
FPS = 2

MOVE = 24
WAIT = 54
ATTACK = 14

TEXT_COLOR = (255, 255, 255)

class Doll:
	def __init__(self, D_num):
		self.num = D_num
		self.w, self.h = 40, 40
		self.pos = 800 + (200 * (self.num % 4)), 610 + (200 * (self.num // 4))
		self.visible = False
		self.behavior = MOVE
		self.wait = gfw.image.load('res/character/' + str(self.num) +'_wait.png')
		self.move = gfw.image.load('res/character/' + str(self.num) +'_move.png')
		self.attack = gfw.image.load('res/character/' + str(self.num) +'_attack.png')
		self.frame_index = 0
		self.time = 0
		self.mouse_point = None
		global BOUNDARY_LEFT, BOUNDARY_RIGHT, BOUNDARY_DOWN, BOUNDARY_UP
		BOUNDARY_LEFT = 80 // 2
		BOUNDARY_DOWN = 80 // 2
		BOUNDARY_RIGHT = get_canvas_width() - BOUNDARY_LEFT
		BOUNDARY_UP = get_canvas_height() - BOUNDARY_DOWN
		global pos_font
		pos_font = gfw.font.load(res('ENCR10B.TTF'), 15)

	def draw(self):
		if self.visible:
			sx = self.frame_index * 200
			if self.behavior == MOVE:
				self.move.clip_draw(sx, 0, 200, 200, *self.pos)
			elif self.behavior == WAIT:
				self.wait.clip_draw(sx, 0, 200, 200, *self.pos)
			elif self.behavior == ATTACK:
				self.attack.clip_draw(sx, 0, 200, 200, *self.pos)

	def update(self):
		self.time += 1
		if self.time % FPS == 0:
			self.frame_index = (self.frame_index + 1) % self.behavior

	def draw_position(self):
		draw_rectangle(*self.get_bb())
		x,y = self.pos
		x -= 2 * self.w
		y -= 2 * self.h
		pos_font.draw(x, y, str(self.pos), TEXT_COLOR)

	def handle_event(self, e):
		pair = (e.type, e.button)
		if self.mouse_point is None:
			if pair == LBTN_DOWN:
				if pt_in_rect(mouse_xy(e), self.get_bb()):
					self.visible = True
					self.mouse_point = mouse_xy(e)
					return True
			return False

		if pair == LBTN_UP:
			self.mouse_point = None
			self.behavior = WAIT
			x,y = self.pos
			x = x // 80 * 80 + 40
			y = y // 80 * 80 + 50
			#if x < 가 제작 스테이지 또는 선택 스테이지에 놓지 못하도록 한다
			if x <= 0 or x >= 960 or y <= 159 or y >= 720:
				gfw.world.remove(self)
				print("범위 바깥엔 배치할 수 없습니다. 오브젝트 삭제" , gfw.world.count_at(gfw.layer.doll))
			for doll in gfw.world.objects_at(gfw.layer.doll):
				if doll.pos == (x, y):
					gfw.world.remove(self)
					print("이미 배치된 인형이 있습니다. 오브젝트 삭제" , gfw.world.count_at(gfw.layer.doll))
			self.pos = x, y
			return False

		if e.type == SDL_MOUSEMOTION:
			x,y = self.pos
			mx,my = mouse_xy(e)
			px,py = self.mouse_point
			self.pos = x + mx - px, y + my - py
			#print((x,y), (mx,my), (px,py), self.pos)
			self.mouse_point = mx,my
		elif (e.type, e.key) == KEYDN_DEL or (e.type, e.button) == RBTN_DOWN:
			gfw.world.remove(self)
			return False

		return True

	def get_bb(self):
		x,y = self.pos
		return x - self.w, y - self.h - 10, x + self.w, y + self.h - 10
