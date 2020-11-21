from pico2d import *
import gfw
from gobj import *

FPS = 2
TEXT_COLOR = (255, 255, 255)

class Select:
	def __init__(self, D_num):
		self.num = D_num
		self.w, self.h = 40, 40
		self.pos = 1000 + (80 * (self.num % 4)), 610 - (80 * (self.num // 4))
		self.image = gfw.image.load('res/character/' + str(self.num) + '_w.png')
		self.frame_index = 0
		self.time = 0
		self.total_count = 1
		self.placed_count = 0
		self.can_place = True
		global count_font
		count_font = gfw.font.load(res('ENCR10B.TTF'), 20)

	def draw(self):
		x,y = self.pos
		x += 25
		y += 20
		sx = self.frame_index * 150
		self.image.clip_draw(sx, 0, 150, 150, *self.pos)
		count_font.draw(x, y, str(self.total_count - self.placed_count), TEXT_COLOR)

	def update(self):
		self.time += 1
		if self.time % FPS == 0:
			self.frame_index = (self.frame_index + 1) % 54
		if (self.total_count - self.placed_count) <= 0: self.can_place = False
		else: self.can_place = True

	def get_bb(self):
		x,y = self.pos
		return x - self.w, y - self.h - 10, x + self.w, y + self.h - 10

	def draw_position(self):
		draw_rectangle(*self.get_bb())
		x,y = self.pos
		x -= 2 * self.w
		y -= 2 * self.h
