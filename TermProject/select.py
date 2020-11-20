from pico2d import *
import gfw
from gobj import *

FPS = 2

class Select:
	def __init__(self, D_num):
		self.num = D_num
		self.w, self.h = 40, 40
		self.pos = 800 + (200 * (self.num % 4)), 610 + (200 * (self.num // 4))
		self.image = gfw.image.load('res/character/' + str(self.num) +'_wait.png')
		self.frame_index = 0
		self.time = 0

	def draw(self):
		sx = self.frame_index * 200
		self.image.clip_draw(sx, 0, 200, 200, *self.pos)

	def update(self):
		self.time += 1
		if self.time % FPS == 0:
			self.frame_index = (self.frame_index + 1) % 54

	def get_bb(self):
		x,y = self.pos
		return x - self.w, y - self.h - 10, x + self.w, y + self.h - 10

	def draw_position(self):
		draw_rectangle(*self.get_bb())
		x,y = self.pos
		x -= 2 * self.w
		y -= 2 * self.h
