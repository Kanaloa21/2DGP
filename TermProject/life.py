from pico2d import *
import gfw
from gobj import *

TEXT_COLOR_1 = (0, 255, 0)
TEXT_COLOR_2 = (255, 255, 255)

class Life():
	def __init__(self):
		self.life_count = 10
		self.text_pos_1 = 1100, 120
		self.text_pos_2 = 1190, 120
		self.text_pos_3 = 1100, 90
		self.text_pos_4 = 1190, 90
		self.text = gfw.font.load(res('font/Maplestory Light.ttf'), 20)
		self.count_text = gfw.font.load(res('font/LCD2N___.TTF'), 25)
		self.score = 0

	def draw(self):
		self.text.draw(*self.text_pos_1, 'LIFE: ', TEXT_COLOR_1)
		self.count_text.draw(*self.text_pos_2, str(self.life_count), TEXT_COLOR_2)
		self.text.draw(*self.text_pos_3, 'SCORE: ', TEXT_COLOR_1)
		self.count_text.draw(*self.text_pos_4, str(self.score), TEXT_COLOR_2)
	def update(self):
		pass
