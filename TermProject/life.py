from pico2d import *
import gfw
from gobj import *

TEXT_COLOR_1 = (50, 255, 50)
TEXT_COLOR_2 = (255, 255, 255)

class Life():
	def __init__(self):
		self.life_count = 10
		self.text_pos_1 = 985, 105
		self.text_pos_2 = 1140, 105
		self.text = gfw.font.load(res('Maplestory Light.ttf'), 40)
		self.life_text = gfw.font.load(res('LCD2N___.TTF'), 40)

	def draw(self):
		self.text.draw(*self.text_pos_1, 'LIFE', TEXT_COLOR_1)
		self.life_text.draw(*self.text_pos_2, str(self.life_count), TEXT_COLOR_2)

	def update(self):
		pass
