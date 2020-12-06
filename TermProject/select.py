from pico2d import *
import gfw
from gobj import *

FPS = 2
TEXT_COLOR = (255, 255, 255)

doll_data = {}
# name, num, damage, rpm, boundary
def load():
	with open(res('dolls.json')) as f:
		data = json.load(f)
		for name in data:
			doll_data[name] = tuple(data[name])

class Select:
	def __init__(self, name):
		load()
		self.name = name
		self.data = doll_data[name]
		self.num = self.data[0]
		self.damage = self.data[1]
		self.rpm = self.data[2]
		self.boundary = self.data[3]
		self.attack_frame = self.data[4]
		self.w, self.h = 40, 40
		self.pos = 1000 + (80 * (self.num % 4)), 610 - (80 * (self.num // 4))
		self.image = gfw.image.load('res/character/' + str(self.num) + '_w.png')
		self.frame_index = 0
		self.time = 0
		self.total_count = 1
		self.placed_count = 0
		self.can_place = True
		self.dp = False
		global count_font
		count_font = gfw.font.load(res('ENCR10B.TTF'), 20)

	def draw(self):
		x,y = self.pos
		x += 25
		y += 20
		sx = self.frame_index * 150
		self.image.clip_draw(sx, 0, 150, 150, *self.pos)
		if self.dp:
			self.image.clip_draw(sx, 0, 150, 150, 1030, 270)
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
