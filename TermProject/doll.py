from pico2d import *
import gfw
from gobj import *

LBTN_DOWN = (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT)
LBTN_UP   = (SDL_MOUSEBUTTONUP,   SDL_BUTTON_LEFT)
RBTN_DOWN = (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_RIGHT)
KEYDN_DEL = (SDL_KEYDOWN, SDLK_DELETE)
FPS = 2

ATTACK = 20 # 150*20 = 3000
MOVE = 24	# 150*24 = 3600
WAIT = 54	# 150*54 = 8100

TEXT_COLOR = (255, 255, 255)

class Doll:
	def __init__(self, D_num):
		self.num = D_num
		self.w, self.h = 40, 40
		self.pos = 1000 + (80 * (self.num % 4)), 610 - (80 * (self.num // 4))
		self.visible = False
		self.behavior = MOVE
		self.wait = gfw.image.load('res/character/' + str(self.num) +'_w.png')
		self.move = gfw.image.load('res/character/' + str(self.num) +'_m.png')
		self.attack = gfw.image.load('res/character/' + str(self.num) +'_a.png')
		self.frame_index = 0
		self.time = 0
		self.mouse_point = None
		self.palced_done = False
		self.lockon = None
		self.flip = 'h'
		self.once = True
		global pos_font
		pos_font = gfw.font.load(res('ENCR10B.TTF'), 15)

	def draw(self):
		if self.visible:
			sx = self.frame_index * 150
			if self.behavior == MOVE:
				self.move.clip_composite_draw(sx, 0, 150, 150, 0, self.flip,*self.pos, 150, 150)
			elif self.behavior == WAIT:
				self.wait.clip_composite_draw(sx, 0, 150, 150, 0, self.flip,*self.pos, 150, 150)
			elif self.behavior == ATTACK:
				self.attack.clip_composite_draw(sx, 0, 150, 150, 0, self.flip,*self.pos, 150, 150)

	def update(self):
		self.time += 1
		if self.time % FPS == 0:
			self.frame_index = (self.frame_index + 1) % self.behavior

		self.attack_range()
		if self.lockon != -1 and self.frame_index == 0:
			for e in gfw.world.objects_at(gfw.layer.enemy):
				if e.num == self.lockon:
					e.life -= 10
				if e.num <= 0:
					self.lockon = -1
					self.behavior = WAIT

	def attack_range(self):
		distance = 100000
		for e in gfw.world.objects_at(gfw.layer.enemy):
			x, y = self.pos
			ex, ey = e.pos
			dx, dy = x - ex, y - ey
			distance = math.sqrt(dx**2 + dy**2)
			break
		if distance <= 145:
			self.behavior = ATTACK
			self.lockon = e.num
			if ex < x: self.flip = 'h'
			else: self.flip = ' '
		elif self.behavior != MOVE:
			self.behavior = WAIT
			self.lockon = -1
	
	
		

	def draw_position(self):
		draw_rectangle(*self.get_bb())
		x,y = self.pos
		x -= 2 * self.w
		y -= 2 * self.h
		pos_font.draw(x, y, str(self.pos), TEXT_COLOR)

	def handle_event(self, e):
		pair = (e.type, e.button)
		if self.mouse_point is None:
			if pair == LBTN_DOWN:
				if pt_in_rect(mouse_xy(e), self.get_bb()) and self.palced_done == False:
					self.visible = True
					self.mouse_point = mouse_xy(e)
					return True
				elif pt_in_rect(mouse_xy(e), self.get_bb()) and self.palced_done == True:
					self.remove()
					for select in gfw.world.objects_at(gfw.layer.select):
						if select.num == self.num:
							select.placed_count -= 1
					print("오브젝트 되돌림" , gfw.world.count_at(gfw.layer.doll))
					return True

			if pair == RBTN_DOWN:
				if pt_in_rect(mouse_xy(e), self.get_bb()) and self.palced_done == True:
					
					for select in gfw.world.objects_at(gfw.layer.select):
						if select.num == self.num:
							select.placed_count -= 1
							select.total_count -= 1
					for ui in gfw.world.objects_at(gfw.layer.ui):
						ui.money += 5
					print("오브젝트 판매" , gfw.world.count_at(gfw.layer.doll))
					self.remove()
			return False

		if pair == LBTN_UP:
			self.mouse_point = None
			self.behavior = WAIT
			x,y = self.pos
			x = x // 80 * 80 + 40
			y = y // 80 * 80 + 50
			if x <= 0 or x >= 960 or y <= 159 or y >= 720:
				for select in gfw.world.objects_at(gfw.layer.select):
					if select.num == self.num:
						select.placed_count -= 1
						print("범위 바깥엔 배치할 수 없습니다. 오브젝트 삭제" , gfw.world.count_at(gfw.layer.doll))
				self.remove()
				return False
			for doll in gfw.world.objects_at(gfw.layer.doll):
				if doll.pos == (x, y):
					for select in gfw.world.objects_at(gfw.layer.select):
						if select.num == self.num:
							select.placed_count -= 1
							print("이미 배치된 인형이 있습니다. 오브젝트 삭제" , gfw.world.count_at(gfw.layer.doll))
					self.remove()
			self.pos = x, y
			self.palced_done = True
			return False

		if e.type == SDL_MOUSEMOTION:
			x,y = self.pos
			mx,my = mouse_xy(e)
			px,py = self.mouse_point
			self.pos = x + mx - px, y + my - py
			#print((x,y), (mx,my), (px,py), self.pos)
			self.mouse_point = mx,my

#		elif (e.type, e.key) == KEYDN_DEL or (e.type, e.button) == RBTN_DOWN:
#			gfw.world.remove(self)
#			return False

		return True

	def get_bb(self):
		x,y = self.pos
		return x - self.w, y - self.h - 10, x + self.w, y + self.h - 10

	def remove(self):
		gfw.world.remove(self)
