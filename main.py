import random
import pyglet
from pyglet.window import key

# -------------------------------------------------------------------------------------------------------

window = pyglet.window.Window(fullscreen=True, caption="Play Snake!")

xc = window.width // 2
yc = window.height // 2

fps = pyglet.window.FPSDisplay(window=window)

# -------------------------------------------------------------------------------------------------------

score = 0
length = 3

top_wall = pyglet.shapes.Rectangle(x=xc, y=yc + 510, width=1020, height=1, color=(255, 255, 255))
top_wall.anchor_x = 510

bottom_wall = pyglet.shapes.Rectangle(x=xc, y=yc - 510, width=1020, height=1, color=(255, 255, 255))
bottom_wall.anchor_x = 510

right_wall = pyglet.shapes.Rectangle(x=xc + 510, y=yc, width=1020, height=1, color=(255, 255, 255))
right_wall.anchor_x = 510
right_wall.rotation = 90

left_wall = pyglet.shapes.Rectangle(x=xc - 510, y=yc, width=1020, height=1, color=(255, 255, 255))
left_wall.anchor_x = 510
left_wall.rotation = 90

# -------------------------------------------------------------------------------------------------------

cell_size = 20
tail = [(24 * cell_size, 25 * cell_size), (23 * cell_size, 25 * cell_size)]
food_x, food_y = 25 * cell_size, 20 * cell_size


def cell(x, y, size, color = (255, 255, 255, 1)):
    img = pyglet.image.create(width=size - 2, height=size - 2, pattern=pyglet.image.SolidColorImagePattern(color))
    img.anchor_x = 9
    img.anchor_y = 9
    img.blit(x, y)


def food_pos():
    global food_x, food_y
    food_x = (xc - 500) + random.randint(0, 50) * cell_size
    food_y = (yc - 500) + random.randint(0, 50) * cell_size
    for n in tail:
        if n[0] == food_x or n[1] == food_x:
            food_pos()
        else:
            pass


def food_place(x, y, size, color = (255, 0, 0, 1)):
    img = pyglet.image.create(width=size, height=size, pattern=pyglet.image.SolidColorImagePattern(color))
    img.anchor_x = size // 2
    img.anchor_y = size // 2
    img.blit(x, y)

def text(string, x, y):
    label = pyglet.text.Label(f"{string}",
                                font_size=24,
                                x=x, y=y,
                                anchor_x="left", anchor_y="bottom")
    label.color = (100, 100, 100, 255)
    label.draw()

# -------------------------------------------------------------------------------------------------------

bearing = 0
snake_dx = xc
snake_dy = yc


@window.event
def on_key_press(symbol, modifiers):
    global bearing

    if symbol == key.UP or symbol == key.W and bearing != 90:
        bearing = 270
    
    elif symbol == key.DOWN or symbol == key.S and bearing != 270:
        bearing = 90
    
    elif symbol == key.LEFT or symbol == key.A and bearing != 0:
        bearing = 180
    
    elif symbol == key.RIGHT or symbol == key.D and bearing != 180:
        bearing = 0

# -------------------------------------------------------------------------------------------------------

def update(dt):
    global snake_dx, snake_dy
    global food_x, food_y
    global score, length

    # Adds a new tail cell behind the head cell
    tail.append((snake_dx, snake_dy))

    # Changes head cell direction by using bearings
    if bearing == 0:
        snake_dx += cell_size
    
    elif bearing == 90:
        snake_dy -= cell_size

    elif bearing == 180:
        snake_dx -= cell_size

    elif bearing == 270:
        snake_dy += cell_size
    
    # Detects if player collides with food
    if snake_dx == food_x and snake_dy == food_y:
        score += 1
        length += 1
        food_pos()
    
    # Removes the new tail cell if we didn't eat any food
    else:
        tail.pop(0)
    
    # Checks if head collided with tail
    for coords in tail:
        if coords == (snake_dx, snake_dy):
            pyglet.app.exit()

    # Checks if head is out of bounds (hits wall)
    if snake_dx == xc - (26 * cell_size):
        pyglet.app.exit()
    
    if snake_dx == xc + (26 * cell_size):
        pyglet.app.exit()
    
    if snake_dy == yc - (26 * cell_size):
        pyglet.app.exit()
    
    if snake_dy == yc + (26 * cell_size):
        pyglet.app.exit()

# -------------------------------------------------------------------------------------------------------

@window.event
def on_draw():
    window.clear()
    fps.draw()

    #Draw score and length
    text(f"Length: {length}", 5, yc*2 - 36)
    text(f"Score: {score}", 5, yc*2 - 74)


    # Draw border
    top_wall.draw()
    bottom_wall.draw()
    right_wall.draw()
    left_wall.draw()

    # Draws player cells and food cell
    food_place(food_x, food_y, cell_size)
    for coords in tail:
        cell(coords[0], coords[1], cell_size)
    cell(snake_dx, snake_dy, cell_size)

# -------------------------------------------------------------------------------------------------------

pyglet.clock.schedule_interval(update, 1/15)
pyglet.app.run()
