import random
from pico2d import *

class Grass:
	def __init__(self):		
		self.image = load_image("../res/grass.png")
	
	def draw(self):
		self.image.draw(400, 30)


class Boy:
	def __init__(self):
		self.image = load_image("../res/animation_sheet.png")
		self.x = random.randint(0, 300)  
		self.y = random.randint(0, 100) + 85
		self.dx = random.random() # 0.0f ~ 1.0f
		self.dy = random.random() # 0.0f ~ 1.0f
		self.frame_index = random.randint(0, 7)
		self.action = random.randint(0, 3)

	def draw(self):
		self.image.clip_draw(self.frame_index * 100, self.action * 100 , 100, 100, self.x, self.y)

	def update(self):
		self.x += self.dx
		self.y += self.dy

		self.frame_index = (self.frame_index + 1) % 8

		if self.x % 100 == 0:
			self.action = (self.action + 1) % 4

if __name__ == '__main__':
	print("I am main")
else:
	print("I am imported")
print("My name is " + __name__)
