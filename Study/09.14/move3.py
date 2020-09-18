from pico2d import *

open_canvas()

gra = load_image('grass.png')
ch = load_image('run_animation.png')

x = 0
frame_index = 0
while x < 800:
	clear_canvas_now()
	gra.draw(400, 30)
	ch.clip_draw(frame_index * 100, 0, 100, 100, x, 85)
	update_canvas()
	# page_fliping
	get_events()
	# for e i in evnt:
	#	print(e)
	x += 3
	#frame_index += 1
	#if frame_index >= 8: frame_index = 0
	# 위의 구조는 if문 사용

	frame_index = (frame_index + 1) % 8
	delay(0.05)

delay(1)

close_canvas()

#game loop
#- logic = update()
# - logic
# - event handring
# - render = draw()