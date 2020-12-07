import json
import gfw
from pico2d import *
from gobj import *

LBTN_DOWN = (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT)
LBTN_UP   = (SDL_MOUSEBUTTONUP,   SDL_BUTTON_LEFT)
RBTN_DOWN = (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_RIGHT)
KEYDN_DEL = (SDL_KEYDOWN, SDLK_DELETE)

ATTACK = 20 # 150*20 = 3000
MOVE = 24	# 150*24 = 3600
WAIT = 54	# 150*54 = 8100

TEXT_COLOR = (255, 255, 255)

class Doll:
	def __init__(self, name, num, damage, rpm, boundary, attack_frame):
		self.name = name
		self.num = num
		self.damage = damage
		self.rpm = rpm
		self.boundary = boundary
		self.ATTACK = attack_frame
		self.w, self.h = 40, 40
		self.pos = 1000 + (80 * (self.num % 4)), 610 - (80 * (self.num // 4))
		self.visible = False
		self.behavior = MOVE
		self.wait = gfw.image.load(res('character/' + str(self.num) +'_w.png'))
		self.move = gfw.image.load(res('character/' + str(self.num) +'_m.png'))
		self.attack = gfw.image.load(res('character/' + str(self.num) +'_a.png'))
		self.frame_index = 0
		self.time = 0
		self.mouse_point = None
		self.palced_done = False
		self.lockon = -1
		self.flip = 'h'
		global sound_rifle, sound_shot, sound_snipe
		sound_rifle = load_wav(res('sound/rifle.wav'))
		sound_rifle.set_volume(3)
		sound_shot = load_wav(res('sound/shot.wav'))
		sound_shot.set_volume(10)
		sound_snipe = load_wav(res('sound/snipe.wav'))
		sound_snipe.set_volume(10)
		
	def draw(self):
		if self.visible:
			sx = self.frame_index * 150
			if self.behavior == MOVE:
				self.move.clip_composite_draw(sx, 0, 150, 150, 0, self.flip,*self.pos, 150, 150)
			elif self.behavior == WAIT:
				self.wait.clip_composite_draw(sx, 0, 150, 150, 0, self.flip,*self.pos, 150, 150)
			elif self.behavior == self.ATTACK:
				self.attack.clip_composite_draw(sx, 0, 150, 150, 0, self.flip,*self.pos, 150, 150)

	def update(self):
		self.time += gfw.delta_time
		frame = self.time * self.rpm
		self.frame_index = int(frame) % self.behavior

		self.attack_range()

		if self.lockon != -1 and self.frame_index == 10:
			for e in gfw.world.objects_at(gfw.layer.enemy):
				if e.num == self.lockon:
					if e.life > 0:
						e.life -= self.damage
						global sound_rifle, sound_shot, sound_snipe
						if self.num <= 4:
							sound_shot.play()
						elif self.num == 11 or self.num == 12 or self.num == 13:
							sound_snipe.play()
						else: 
							sound_rifle.play()
					elif e.life <= 0:
						e.life = 0
						self.lockon = -1
						self.behavior = WAIT

	def attack_range(self):
		global dis_sq
		target_num = -1
		e_pos = 0, 0
		for e in gfw.world.objects_at(gfw.layer.enemy):
			dis_sq = distance_sq(self.pos, e.pos)
			if dis_sq <= self.boundary**2:
				target_num = e.num
				e_pos = e.pos
				break
		if dis_sq <= self.boundary**2 and self.behavior != MOVE:
			if self.behavior == WAIT:
				self.frame_index = 0
			self.behavior = self.ATTACK
			self.lockon = target_num
			self.flip = self.do_flip(e_pos[0], self.pos[0])

		elif self.behavior != MOVE:
			self.behavior = WAIT
			self.lockon = -1

	def do_flip(self, ex, x):
		if ex < x: return 'h'
		else: return ' '

	def draw_position(self):
		draw_rectangle(*self.get_bb())

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
					for selection in gfw.world.objects_at(gfw.layer.selection):
						if selection.num == self.num:
							selection.placed_count -= 1
					print("오브젝트 되돌림" , gfw.world.count_at(gfw.layer.doll))
					return True

			if pair == RBTN_DOWN:
				if pt_in_rect(mouse_xy(e), self.get_bb()) and self.palced_done == True:
					
					for selection in gfw.world.objects_at(gfw.layer.selection):
						if selection.num == self.num:
							selection.placed_count -= 1
							selection.total_count -= 1
					for gacha in gfw.world.objects_at(gfw.layer.gacha):
						gacha.money += 5
					print("오브젝트 판매" , gfw.world.count_at(gfw.layer.doll))
					self.remove()
			return False

		if pair == LBTN_UP:
			self.mouse_point = None
			self.behavior = WAIT
			x,y = self.pos
			x = x // 80 * 80 + 40
			y = y // 80 * 80 + 50
			if x <= 0 or x >= 960 or y <= 159 or y >= 720 or y == 530 or (x >= 200 and x <= 760 and y == 290) or (x == 200 and y >= 350 and y <= 450) or (x == 760 and y >= 350 and y <= 450) :
				for selection in gfw.world.objects_at(gfw.layer.selection):
					if selection.num == self.num:
						selection.placed_count -= 1
						print("범위 바깥엔 배치할 수 없습니다. 오브젝트 삭제" , gfw.world.count_at(gfw.layer.doll))
				self.remove()
				return False
			for doll in gfw.world.objects_at(gfw.layer.doll):
				if doll.pos == (x, y):
					for selection in gfw.world.objects_at(gfw.layer.selection):
						if selection.num == self.num:
							selection.placed_count -= 1
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
			self.mouse_point = mx,my

		return True

	def get_bb(self):
		x,y = self.pos
		return x - self.w, y - self.h - 10, x + self.w, y + self.h - 10

	def remove(self):
		gfw.world.remove(self)
