import json
from pico2d import *
import gfw
from gobj import *

TEXT_COLOR = (255, 255, 255)
TEXT_COLOR_2 = (0, 0, 255)
TEXT_COLOR_3 = (255, 0, 0)

doll_data = {}
reicpe_data = {}

LBTN_DOWN = (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT)
LBTN_UP   = (SDL_MOUSEBUTTONUP,   SDL_BUTTON_LEFT)

def load():
	with open(res('json/dolls.json')) as f:
		data = json.load(f)
		for name in data:
			doll_data[name] = tuple(data[name])

def reicpes_load():
	with open(res('json/reicpes.json')) as f:
		data = json.load(f)
		for name in data:
			reicpe_data[name] = tuple(data[name])

class Selection:
	def __init__(self, name):
		load()
		reicpes_load()
		self.name = name
		self.data = doll_data[name]
		self.num = self.data[0]
		self.damage = self.data[1]
		self.rpm = self.data[2]
		self.boundary = self.data[3]
		self.attack_frame = self.data[4]
		self.w, self.h = 40, 40
		self.pos = 1000 + (80 * (self.num % 4)), 610 - (80 * (self.num // 4))
		self.image = gfw.image.load(res('character/' + str(self.num) + '_w.png'))
		self.frame_index = 0
		self.time = 0
		if self.num <= 4:
			self.total_count = 1
		else:
			self.total_count = 0
			self.reicpe = reicpe_data[name]
		self.mft = [True, True, True] # 3개 전부 TRUE여야 제작 가능
		self.placed_count = 0
		self.can_place = True
		self.dp = False
		self.pressed = False
		self.mouse_point = None
		global count_font, sound_reload
		count_font = gfw.font.load(res('font/Maplestory Light.ttf'), 20)
		sound_reload = load_wav(res('sound/reload.wav'))
		sound_reload.set_volume(50)

	def draw(self):
		x,y = self.pos
		x += 25
		y += 20
		sx = self.frame_index * 150
		self.image.clip_draw(sx, 0, 150, 150, *self.pos)
		count_font.draw(x, y, str(self.total_count - self.placed_count), TEXT_COLOR)
		if self.dp:
			self.image.clip_draw(sx, 0, 150, 150, 1030, 270)
			if self.num > 4:
				#draw_rectangle(655, 10, 780, 50)
				self.image.clip_draw(sx, 0, 150, 150, 720, 115)
				for o in gfw.world.objects_at(gfw.layer.selection):
					if o.num == self.reicpe[0]:
						o.image.clip_draw(sx, 0, 150, 150, 225, 90)
						
						if (o.total_count - o.placed_count) >= self.reicpe[1]:
							count_font.draw(225 + 25, 90 + 20, str(self.reicpe[1]), TEXT_COLOR_2)
							self.mft[0] = True
						else:
							count_font.draw(225 + 25, 90 + 20, str(self.reicpe[1]), TEXT_COLOR_3)
							self.mft[0] = False
					if o.num == self.reicpe[2]:
						o.image.clip_draw(sx, 0, 150, 150, 375, 90)
						if (o.total_count - o.placed_count) >= self.reicpe[3]:
							count_font.draw(375 + 25, 90 + 20, str(self.reicpe[3]), TEXT_COLOR_2)
							self.mft[1] = True
						else: 
							count_font.draw(375 + 25, 90 + 20, str(self.reicpe[3]), TEXT_COLOR_3)
							self.mft[1] = False
					if o.num == self.reicpe[4]:
						o.image.clip_draw(sx, 0, 150, 150, 515, 90)
						if (o.total_count - o.placed_count) >= self.reicpe[5]:
							count_font.draw(515 + 25, 90 + 20, str(self.reicpe[5]), TEXT_COLOR_2)
							self.mft[2] = True
						else: 
							count_font.draw(515 + 25, 90 + 20, str(self.reicpe[5]), TEXT_COLOR_3)
							self.mft[2] = False

	def update(self):
		self.time += 1
		if self.time % 2 == 0:
			self.frame_index = (self.frame_index + 1) % 54
		if (self.total_count - self.placed_count) <= 0: self.can_place = False
		else: self.can_place = True

	def handle_event(self, e):
		pair = (e.type, e.button)
		if self.mouse_point is None:
			if pair == LBTN_DOWN :
				if self.num > 4 :
					if pt_in_rect(mouse_xy(e), (655, 10, 780, 50)) and self.mft[0] and self.mft[1] and self.mft[2]:
						print("누름!")
						self.pressed = True
						global sound_reload
						sound_reload.play()
						self.mouse_point = mouse_xy(e)
						for o in gfw.world.objects_at(gfw.layer.selection):
							if o.num == self.reicpe[0]:
								o.total_count -= self.reicpe[1]
							if o.num == self.reicpe[2]:
								o.total_count -= self.reicpe[3]
							if o.num == self.reicpe[4]:
								o.total_count -= self.reicpe[5]
						self.total_count += 1
						return True
				return False
		if pair == LBTN_UP:
			self.mouse_point = None
			self.pressed = False
			return False
		return True

	def get_bb(self):
		x,y = self.pos
		return x - self.w, y - self.h - 10, x + self.w, y + self.h - 10

	def draw_position(self):
		draw_rectangle(*self.get_bb())
