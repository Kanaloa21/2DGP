import random
from pico2d import *
import gfw
from gobj import *
import life_gauge

TEXT_COLOR = (255, 255, 255)
class Enemy:
	TARGET_POSITIONS = [(760, 560), (760, 320), (200, 320), (200, 560), (920, 560)]
	ACTIONS = ['Move', 'Dead']
	FPS = 2
	MOVE = 24	# 150*24 = 3600
	DEAD = 26	# 150*26 = 3900
	def __init__(self, E_num, level):
		self.num = E_num
		self.w, self.h = 40, 40
		self.pos = -40, 560
		self.delta = 0, 0
		self.action = Enemy.MOVE
		self.target_index = 0
		self.target = Enemy.TARGET_POSITIONS[self.target_index]
		self.move = gfw.image.load(res('enemy/e' + str(0) +'_m.png'))
		self.dead = gfw.image.load(res('enemy/e' + str(0) +'_d.png'))
		self.frame_index = 0
		self.time = 0
		self.flip = True
		self.level = level
		self.max_life = level * 100
		self.life = self.max_life
		self.once = True
		global pos_font
		pos_font = gfw.font.load(res('font/ENCR10B.TTF'), 15)

	def set_target(self):
		x,y = self.pos
		tx,ty = self.target
		dx, dy = tx - x, ty - y
		distance = math.sqrt(dx**2 + dy**2)
		if distance <= 0.01: 
			if self.target_index <= 3:
				self.target_index += 1
				self.target = Enemy.TARGET_POSITIONS[self.target_index]
			else: 
				for life in gfw.world.objects_at(gfw.layer.life):
					life.life_count -= 1
				self.remove()
			return
		self.delta = dx / distance, dy / distance

	def draw(self):
		sx = self.frame_index * 150
		if self.action == Enemy.MOVE:
			if self.flip:
				self.move.clip_composite_draw(sx, 0, 150, 150, 0, 'h',*self.pos, 150, 150)
			else: 
				self.move.clip_composite_draw(sx, 0, 150, 150, 0, ' ',*self.pos, 150, 150)
		else:
			if self.flip:
				self.dead.clip_composite_draw(sx, 0, 150, 150, 0, 'h',*self.pos, 150, 150)
			else: 
				self.dead.clip_composite_draw(sx, 0, 150, 150, 0, ' ',*self.pos, 150, 150)
		#self.draw_position()
		x, y = self.pos
		gy = y - 150 // 2
		rate = self.life / self.max_life
		if self.life > 0:
			life_gauge.draw(x, gy, 60, rate)

	def update(self):
		self.time += 1
		if self.time % self.FPS == 0:
			self.frame_index = (self.frame_index + 1) % self.action
		if self.action == Enemy.MOVE:
			self.set_target()
			x, y = self.pos
			dx, dy = self.delta
			self.pos = x + dx, y + dy
		#print(*self.pos)

		filp_list = [1, 2]
		if self.target_index in filp_list: 
			self.flip = False
		else: 
			self.flip = True

		if self.life <= 0:
			self.action = Enemy.DEAD
			if self.once == True:
				self.frame_index = 0 	# 프레임 초기화
				self.once = False
			if self.frame_index == Enemy.DEAD - 1:
				print('적 사망', self.num)
				for gacha in gfw.world.objects_at(gfw.layer.gacha):
					gacha.money += 1 * self.level
				for life in gfw.world.objects_at(gfw.layer.life):
					life.score += 1 * self.level // 2 + 1
				self.remove()

	def remove(self):
		gfw.world.remove(self)

	def get_bb(self):
		x,y = self.pos
		return x - self.w, y - self.h - 40, x + self.w, y + self.h - 40

	def draw_position(self):
		draw_rectangle(*self.get_bb())
		x,y = self.pos
		x -= 2 * self.w
		y -= 2 * self.h
		#pos_font.draw(x, y, str(self.pos), TEXT_COLOR)