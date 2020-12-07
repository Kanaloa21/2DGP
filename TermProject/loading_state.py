import gfw
from pico2d import *
import game_state
from gobj import res

canvas_width = game_state.canvas_width
canvas_height = game_state.canvas_height

center_x = canvas_width // 2
center_y = canvas_height // 2

def enter():
	global back, bg, fg, index, file
	back = gfw.image.load(res('loading_1280x960.png'))
	bg = gfw.image.load(res('progress_bg.png'))
	fg = gfw.image.load(res('progress_fg.png'))
	index = 0

	global font, display
	font = gfw.font.load(res('font/ENCR10B.TTF'), 30)
	display = ''

	global frame_interval
	frame_interval = gfw.frame_interval
	gfw.frame_interval = 0

def exit():
	global back, bg, fg
	gfw.image.unload(res('loading_1280x960.png'))
	gfw.image.unload(res('progress_bg.png'))
	gfw.image.unload(res('progress_fg.png'))
	del back
	del bg
	del fg

	global frame_interval
	gfw.frame_interval = frame_interval

def update():
	global index, display
	image_count = len(IMAGE_FILES)
	font_count = len(FONT_PAIRS)
	if index < image_count:
		file = IMAGE_FILES[index]
		gfw.image.load(file)
		display = file
	elif index - image_count < font_count:
		file, size = FONT_PAIRS[index - image_count]
		gfw.font.load(file, size)
		display = '%s %dpt' % (file, size)
	else:
		gfw.change(game_state)
		return
	index += 1

def draw():
	back.draw(center_x, center_y)
	image_count = len(IMAGE_FILES)
	font_count = len(FONT_PAIRS)
	progress = index / (image_count + font_count)
	draw_progress(center_x, 300, 680, progress)

	global display
	font.draw(300, 250, display)
	font.draw(300, 350, '%.1f%%' % (progress * 100))

def draw_progress(x, y, width, rate):
	l = x - width // 2
	b = y - bg.h // 2
	draw_3(bg, l, b, width, 3)
	draw_3(fg, l, b, round(width * rate), 3)

def draw_3(img, l, b, width, edge):
	img.clip_draw_to_origin(0, 0, edge, img.h, l, b, edge, img.h)
	img.clip_draw_to_origin(edge, 0, img.w - 2 * edge, img.h, l+edge, b, width - 2 * edge, img.h)
	img.clip_draw_to_origin(img.w - edge, 0, edge, img.h, l+width-edge, b, edge, img.h)

def handle_event(e):
	global player
	# prev_dx = boy.dx
	if e.type == SDL_QUIT:
		gfw.quit()
	elif e.type == SDL_KEYDOWN:
		if e.key == SDLK_ESCAPE:
			gfw.pop()

IMAGE_FILES = [
	"res/background.png",
	"res/cross.png",
	"res/helper.png",
	"res/game_over.png",
	"res/ui/gauge_bg.png",
	"res/ui/gauge_fg.png",
	"res/ui/longbutton.png",
	"res/ui/longbutton_pressed.png",
	"res/ui/shortbutton.png",
	"res/ui/shortbutton_pressed.png",
	"res/character/0_a.png",
	"res/character/0_m.png",
	"res/character/0_w.png",
	"res/character/1_a.png",
	"res/character/1_m.png",
	"res/character/1_w.png",
	"res/character/2_a.png",
	"res/character/2_m.png",
	"res/character/2_w.png",
	"res/character/3_a.png",
	"res/character/3_m.png",
	"res/character/3_w.png",
	"res/character/4_a.png",
	"res/character/4_m.png",
	"res/character/4_w.png",
	"res/character/5_a.png",
	"res/character/5_m.png",
	"res/character/5_w.png",
	"res/character/6_a.png",
	"res/character/6_m.png",
	"res/character/6_w.png",
	"res/character/7_a.png",
	"res/character/7_m.png",
	"res/character/7_w.png",
	"res/character/8_a.png",
	"res/character/8_m.png",
	"res/character/8_w.png",
	"res/character/9_a.png",
	"res/character/9_m.png",
	"res/character/9_w.png",
	"res/character/10_a.png",
	"res/character/10_m.png",
	"res/character/10_w.png",
	"res/character/11_a.png",
	"res/character/11_m.png",
	"res/character/11_w.png",
	"res/character/12_a.png",
	"res/character/12_m.png",
	"res/character/12_w.png",
	"res/character/13_a.png",
	"res/character/13_m.png",
	"res/character/13_w.png",
	"res/character/14_a.png",
	"res/character/14_m.png",
	"res/character/14_w.png",
	"res/character/15_a.png",
	"res/character/15_m.png",
	"res/character/15_w.png",
	"res/enemy/e0_d.png",
	"res/enemy/e0_m.png"
]

FONT_PAIRS = [
	("res/font/ENCR10B.TTF", 10),
	("res/font/LCD2N___.TTF", 10),
	("res/font/Maplestory Light.TTF", 10),

]

if __name__ == '__main__':
	gfw.run_main()
