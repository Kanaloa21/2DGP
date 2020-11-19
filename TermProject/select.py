from pico2d import *
import gfw
from gobj import *
FPS = 2
class Select:
	def __init__(self, D_num):
		self.pos = 1000, 600
		self.image = gfw.image.load('res/character/' + str(D_num) +'_wait.png')
		self.frame_index = 0
		self.time = 0

	def draw(self):
		sx = self.frame_index * 200
		self.image.clip_draw(sx, 0, 200, 200, *self.pos)

	def update(self):
		self.time += 1
		if self.time % FPS == 0:
			self.frame_index = (self.frame_index + 1) % 54
