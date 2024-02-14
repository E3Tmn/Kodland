import random


WIDTH = 400
HEIGHT = 200

play_button = Actor('yellow_button', (200, 50))
music_button = Actor('yellow_button', (200, 100))
exit_button = Actor('yellow_button', (200, 150))

bonus_icon = Actor('tile_0055', (WIDTH - 48, 16))
main_hero = Actor('tile_0040', (16, 16))
main_hero.num_bonus = 0

fon_cell = Actor('tile_0000')
grass_cell = Actor('tile_0007')
flower_cell = Actor('tile_0038')

mode = 'menu'
is_music = False
count = 0

bullets = []
enemies = []
bonuses = []

map = [[random.randint(0, 2) for k in range(35)] for i in range(13)]


def create_bullet(x, y):
    bullet = Actor('tile_0044', (x, y))
    bullets.append(bullet)


def create_enemy():
    x = random.randint(WIDTH, WIDTH + 100)
    y = random.randint(0, HEIGHT)
    enemy = Actor('tile_0053', (x, y))
    if random.randint(0, 7) == 3:
        enemy.bonus = True
    else:
        enemy.bonus = False
    enemies.append(enemy)


def create_bonus():
    x = random.randint(48, WIDTH - 48)
    y = random.randint(48, HEIGHT - 48)
    bonus = Actor('tile_0055', (x, y))
    bonuses.append(bonus)


def map_draw():
    for i, row in enumerate(map):
        for j, cell in enumerate(row):
            if cell == 0:
                fon_cell.left = fon_cell.width * j - 1
                fon_cell.top = fon_cell.height * i - 1
                fon_cell.draw()
            elif cell == 1:
                grass_cell.left = grass_cell.width * j
                grass_cell.top = grass_cell.height * i
                grass_cell.draw()
            elif cell == 2:
                flower_cell.left = flower_cell.width * j
                flower_cell.top = flower_cell.height * i
                flower_cell.draw()


def draw():
    if mode == 'menu':
        screen.clear()
        play_button.draw()
        screen.draw.text('Game', center=(200, 50), color="white", fontsize=36)
        music_button.draw()
        screen.draw.text('Music', center=(200, 100), color="white", fontsize=36)
        exit_button.draw()
        screen.draw.text('Exit', center=(200, 150), color="white", fontsize=36)
    elif mode == 'game':
        screen.clear()
        map_draw()
        main_hero.draw()
        bonus_icon.draw()
        screen.draw.text(f'Points : {count}', center=(64, 16), color="red", fontsize=36)
        screen.draw.text(str(main_hero.num_bonus), center=(WIDTH - 24, 16), color="red", fontsize=36)

        for bullet in bullets:
            bullet.draw()
        for enemy in enemies:
            enemy.draw()
        for bonus in bonuses:
            bonus.draw()
    elif mode == 'game_over':
        screen.clear()
        screen.draw.text('GAME_OVER', center=(200, 150), color="white", fontsize=72)


def on_key_down(key):
    global mode
    if key == keys.W and main_hero.y > 0:
        main_hero.y -= 16
    if key == keys.S and main_hero.y < HEIGHT - main_hero.height:
        main_hero.y += 16
    if key == keys.A and main_hero.x > 0:
        main_hero.image = 'tile_00412'
        main_hero.x -= 16
    if key == keys.D and main_hero.x < WIDTH:
        main_hero.image = 'tile_0041'
        main_hero.x += 16
    if key == keys.SPACE and mode == 'game':
        create_bullet(main_hero.x, main_hero.y)
    if key == keys.SPACE and mode == 'game_over':
        mode = 'menu'


def on_key_up(key):
    if key == keys.D:
        main_hero.image = 'tile_0040'
    if key == keys.A:
        main_hero.image = 'tile_00402'


def on_mouse_down(button, pos):
    global is_music
    global mode

    if mode == 'menu' and button == mouse.LEFT:
        if exit_button.collidepoint(pos):
            quit()
        elif play_button.collidepoint(pos):
            mode = 'game'
        elif music_button.collidepoint(pos) and not is_music:
            sounds.music.play()
            is_music = True
        elif music_button.collidepoint(pos) and is_music:
            sounds.music.stop()
            is_music = False


def update():
    global mode
    global count
    global enemies
    global bullets
    global bonuses

    if len(enemies) < 10:
        create_enemy()

    for bullet in bullets:
        bullet.x += 2
        if bullet.x > WIDTH:
            bullets.remove(bullet)
            continue
        temp = bullet.collidelist(enemies)
        if temp != -1:
            if enemies[temp].bonus:
                create_bonus()
            enemies.pop(temp)
            bullets.remove(bullet)
            count += 1
            create_enemy()

    for enemy in enemies:
        enemy.x -= 2
        if enemy.x < 0:
            enemies.remove(enemy)
            create_enemy()

    temp = main_hero.collidelist(bonuses)
    if temp != -1 and mode == 'game':
        bonuses.pop(temp)
        main_hero.num_bonus += 1

    temp = main_hero.collidelist(enemies)
    if temp != -1 and mode == 'game':
        mode = 'game_over'
        count = 0
        enemies = []
        bullets = []
        bonuses = []
        for i in range(10):
            create_enemy()
        main_hero.pos = (16, 16)
        main_hero.num_bonus = 0
