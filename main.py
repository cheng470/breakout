import random

WIDTH = 640
HEIGHT = 400
WHITE_COLOR = (255, 255, 255)
BRICK_W = 80
BRICK_H = 20

score = 0
lives = 5
win = False
lost = False

started = False # 小球是否发射
ball = Actor("breakout_ball", (WIDTH//2, HEIGHT-47))
pad = Actor("breakout_paddle", (WIDTH//2, HEIGHT-30))
pad.speed = 5
bricks = []
for i in range(5):
    for j in range(WIDTH//BRICK_W):
        brick = Actor("breakout_brick")
        brick.left = j * BRICK_W
        brick.top = 30 + i * BRICK_H
        bricks.append(brick)

def pad_move():
    if keyboard.right:
        pad.x += pad.speed
    elif keyboard.left:
        pad.x -= pad.speed
    if pad.left < 0:
        pad.left = 0
    elif pad.right > WIDTH:
        pad.right = WIDTH

def ball_move():
    global started, lives
    if not started:
        if keyboard.space:
            dir = 1 if random.randint(0,1) else -1
            ball.vx = 3 * dir
            ball.vy = -3
            started = True
        else:
            ball.x = pad.x
            ball.bottom = pad.top
            return
    if ball.left < 0:
        ball.vx = abs(ball.vx)
    elif ball.right > WIDTH:
        ball.vx = -abs(ball.vx)
    if ball.top < 0:
        ball.vy = abs(ball.vy)
    elif ball.top > HEIGHT:
        started = False
        sounds.miss.play()
        lives -= 1
    ball.x += ball.vx
    ball.y += ball.vy

def collision_ball_pad():
    if not ball.colliderect(pad):
        return
    # 垂直方向反弹
    if ball.y < pad.y:
        ball.vy = -abs(ball.vy)
        sounds.bounce.play()
    # 水平方向反弹
    d = random.randint(0,3)
    if ball.x < pad.x:
        ball.vx = -3-d
    else:
        ball.vx = 3+d

def collision_ball_bricks():
    global score
    n = ball.collidelist(bricks)
    if n == -1:
        return
    brick = bricks[n]
    bricks.remove(brick)
    sounds.collide.play()
    score += 100

    # 如果碰撞位置在砖块的底部和顶部
    if brick.left < ball.x < brick.right:
        ball.vy *= -1
        return
    # 如果碰撞位置在砖块左侧
    if ball.x <= brick.left:
        if ball.vx > 0:
            ball.vx *= -1
        else:
            ball.vy *= -1
        return
    # 如果碰撞位置在砖块右侧
    if ball.x >= brick.right:
        if ball.vx < 0:
            ball.vx *= -1
        else:
            ball.vy *= -1

def check_gameover():
    global win, lost
    if len(bricks) == 0:
        sounds.win.play()
        win = True
    if lives <= 0:
        sounds.fail.play()
        lost = True

def draw():
    screen.fill(WHITE_COLOR)
    ball.draw()
    pad.draw()
    for brick in bricks:
        brick.draw()
    screen.draw.text("Live: " + str(lives) + "  Source: " + str(score), bottomleft=(5, HEIGHT-5), color="black")
    if win:
        screen.draw.text("You Win!", center=(WIDTH//2, HEIGHT//2), fontsize=50, color="red")
    if lost:
        screen.draw.text("You Lost!", center=(WIDTH//2, HEIGHT//2), fontsize=50, color="red")


def update():
    pad_move()
    ball_move()
    collision_ball_pad()
    collision_ball_bricks()
    check_gameover()
