from pico2d import *
import gfw
from gobj import *

LBTN_DOWN = (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT)
LBTN_UP   = (SDL_MOUSEBUTTONUP,   SDL_BUTTON_LEFT)
RBTN_DOWN = (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_RIGHT)
KEYDN_DEL = (SDL_KEYDOWN, SDLK_DELETE)
FPS = 2

MOVE = 14
WAIT = 54
ATTACK = 24

TEXT_COLOR = (255, 255, 255)

class Doll:
	def __init__(self, D_num):
		self.w, self.h = 200, 200
		self.pos = 800 + (self.w * (D_num % 4)), 600 + (self.h * (D_num // 4))
		self.visible = False
		self.state = MOVE
		self.wait = gfw.image.load('res/character/' + str(D_num) +'_wait.png')
		self.move = gfw.image.load('res/character/' + str(D_num) +'_move.png')
		self.fire = gfw.image.load('res/character/' + str(D_num) +'_attack.png')
		self.frame_index = 0
		self.time = 0
		self.mouse_point = None

	def draw(self):
		if self.visible:
			sx = self.frame_index * 200
			self.move.clip_draw(sx, 0, 200, 200, *self.pos)
	
	def update(self):
		self.time += 1
		if self.time % FPS == 0:
			self.frame_index = (self.frame_index + 1) % self.state

	def draw_position(self):
		draw_rectangle(*self.get_bb())
		x,y = self.pos
		x -= 2 * self.w
		y -= 2 * self.h
		#pos_font.draw(x, y, str(self.pos), TEXT_COLOR)

	def handle_event(self, e):
		pair = (e.type, e.button)
		if self.mouse_point is None:
			if pair == LBTN_DOWN:
				self.visible = True
				if pt_in_rect(mouse_xy(e), self.get_bb()):
					self.mouse_point = mouse_xy(e)
					return True
			return False

		if pair == LBTN_UP:
			self.mouse_point = None
			return False

		if e.type == SDL_MOUSEMOTION:
			x,y = self.pos
			mx,my = mouse_xy(e)
			px,py = self.mouse_point
			self.pos = x + mx - px, y + my - py
			# print((x,y), (mx,my), (px,py), self.pos)
			self.mouse_point = mx,my
		elif (e.type, e.key) == KEYDN_DEL or (e.type, e.button) == RBTN_DOWN:
			gfw.world.remove(self)
			return False

		return True

	def get_bb(self):
		x,y = self.pos
		return x - self.w, y - self.h, x + self.w, y + self.h