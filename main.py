import pgzrun

HEIGHT = 700
WIDTH = 1200

white = (255,255,255)
blue = (0,0,255)

score = 0
direction = 1
enemies = []
bullets = []
speed = 5

ship = Actor("ship")
ship.pos = (WIDTH // 2,HEIGHT - 60)
ship.dead = False
ship.countdown = 90

for x in range(8):
    for y in range(4):
        e = Actor("a-wasp")
        enemies.append(e)
        enemies[-1].x = 100+ 50*x
        enemies[-1].y = 80+ 50*y

def game_over():
    screen.draw.text("GAME OVER", (250,350))

def display_score():
    screen.draw.text(str(score), (50,30))

def on_key_down(key):
    if ship.dead == False:
        if key == keys.SPACE:
            bullet = Actor("bullet")
            bullets.append(bullet)
            bullets[-1].x = ship.x
            bullets[-1].y = ship.y - 50

def on_mouse_down(pos):
    pass

def draw():
    screen.clear()
    screen.fill(blue)
    if ship.dead == False:
        ship.draw()
    for enemy in enemies:
        enemy.draw()
    if len(enemies) == 0:
        game_over()
    for bullet in bullets:
        bullet.draw()
    display_score()

def update():
    global score, direction
    move_down = False
    if ship.dead == False:
        if keyboard.a:
            ship.x -= speed
            if ship.x <= 0:
                ship.x = 0
        elif keyboard.d:
            ship.x += speed
            if ship.x >= WIDTH:
                ship.x = WIDTH
        elif keyboard.w:
            ship.y -= speed
            if ship.y <= 80:
                ship.y = 80
        elif keyboard.s:
            ship.y += speed
            if ship.y >= HEIGHT - 80:
                ship.y = HEIGHT - 80
    if keyboard.space:
        bullet = Actor("bullet")
        bullets.append(bullet)
        bullets[-1].x = ship.x
        bullets[-1].y = ship.y - 50
    for bullet in bullets:
        if bullet.y <= 0:
            bullets.remove(bullet)
        else:
            bullet.y -= 10
    if len(enemies) == 0:
        game_over()
    if len(enemies) > 0 and (enemies[-1].x > WIDTH-80 or enemies[0].x < 80):
        move_down = True
        direction *= -1
    for enemy in enemies:
        enemy.x += 5*direction
        if move_down == True:
            enemy.y += 100
            move_down = False
        if enemy.y >= HEIGHT:
            enemies.remove(enemy)
        #checking if enemy gets hit by bullets
        for bullet in bullets:
            if enemy.colliderect(bullet):
                score += 100
                bullets.remove(bullet)
                enemies.remove(enemy)
                if len(enemies) == 0:
                    game_over()
        if enemy.colliderect(ship):
            ship.dead = True
    if ship.dead:
        ship.countdown -= 1
    if ship.countdown == 0:
        ship.dead = False
        ship.countdown = 90

pgzrun.go() 