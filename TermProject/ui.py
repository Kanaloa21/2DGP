from pico2d import *
import gfw
from gobj import *
import random

LBTN_DOWN = (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT)
LBTN_UP   = (SDL_MOUSEBUTTONUP,   SDL_BUTTON_LEFT)

TEXT_COLOR = (255, 100, 100)
TEXT_COLOR_2 = (0, 0, 0)

class Ui:
	def __init__(self):
		self.w, self.h = 150, 35
		self.pos = 1120, 680
		self.image = gfw.image.load('res/longbutton.png')
		self.image_pressed = gfw.image.load('res/longbutton_pressed.png')
		self.pressed = False
		self.mouse_point = None
		self.money = 100
		global count_font
		count_font = gfw.font.load(res('Maplestory Light.ttf'), 20)

	def draw(self):
		x,y = self.pos
		if self.pressed:
			y -= 6
			self.image_pressed.draw(x, y)
		else:
			self.image.draw(*self.pos)
		x -= 135
		y += 15
		count_font.draw(x, y, 'Random Unit Gacha -> 10 $!', TEXT_COLOR)
		y -= 25
		txt = 'You have                           ' + str(self.money) + '$'
		count_font.draw(x, y, txt, TEXT_COLOR_2)

	def update(self):
		pass

	def handle_event(self, e):
		pair = (e.type, e.button)
		if self.mouse_point is None:
			if pair == LBTN_DOWN:
				if pt_in_rect(mouse_xy(e), self.get_bb()):
					self.pressed = True
					self.mouse_point = mouse_xy(e)
					if self.money > 0:
						self.money -= 10
						ri = random.randint(0, 4)
						for select in gfw.world.objects_at(gfw.layer.select):
							if select.num == ri:
								select.total_count += 1
					return True
				return False

		if pair == LBTN_UP:
			self.mouse_point = None
			self.pressed = False
			return False
		return True

	def get_bb(self):
		x,y = self.pos
		return x - self.w, y - self.h, x + self.w, y + self.h
