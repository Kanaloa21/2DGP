from pico2d import *
import helper


def handle_event():
    global running, x, y, target_list, pos, done, speed, tmp
    events_list = get_events()
    for e in events_list:
        if e.type == SDL_QUIT:
            running = False
        elif e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                running = False
        elif e.type == SDL_MOUSEBUTTONDOWN:
            pos = x, y
            target_list.append((e.x, get_canvas_height() - e.y - 1))
            tmp = 1
            print(target_list)
            speed += 1


open_canvas()
# hide_cursor()

gra = load_image("grass.png")
ch = load_image("run_animation.png")

running = True
done = True
x, y = 400, 85
target = (x, y)
target_list = [(x, y)]
pos = (x, y)
frame_index = 0
speed = 1
tmp = 0

while running:
    clear_canvas()
    gra.draw(400, 30)
    ch.clip_draw(frame_index * 100, 0, 100, 100, x, y)
    update_canvas()

    handle_event()

    pos, done = helper.move_toward(pos, helper.delta(pos, target_list[0], speed), target_list[0])
    x, y = pos

    if target_list[0] == pos and tmp != 0 and len(target_list) != 1:
        del target_list[0]
    if done:
        speed = 1

    frame_index = (frame_index + 1) % 8
    delay(0.01)

close_canvas()
