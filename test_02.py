# Добавляем главного героя и двигаем его
import sqlite3
import datetime as dt
import sys
import pygame

pygame.init()
size = width, height = 1125, 700
se = wi, het = 125, 80
tile_size = 75
offset = 75
FPS = 50
PLAYER_UP = pygame.USEREVENT + 1
PLAYER_DOWN = pygame.USEREVENT + 2
PLAYER_LEFT = pygame.USEREVENT + 3
PLAYER_RIGHT = pygame.USEREVENT + 4
dd = 0
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
diamond_group = pygame.sprite.Group()
win = pygame.image.load('pics/' + "save.jpg")
monster_group = pygame.sprite.Group()
monster, player, level_size_x, level_size_y = [1,1,1,1]
startcoord = [0, 0]
def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, color_key=None):
    fullname = 'pics/' + name
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Невозможно загрузить картинку:', fullname)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image




player_image = load_image('herogreen3.png', -1)
tile_images = [load_image('background2.png', -1), load_image('ston2.png', -1),
               load_image('mushroom1.png', -1), load_image('star.png', -1)]
diamond_image = [load_image('star.png', -1)]
monster_image = [load_image('monster.png', -1)]


class Stars(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(diamond_group, all_sprites)
        self.image = diamond_image[0]
        self.rect = self.image.get_rect().move(
            tile_size * pos_x, tile_size * pos_y + offset)
        self.colvostars = 3
        self.time = str(dt.datetime.now().strftime("%d-%B-%y %H:%M:%S"))

    def update(self):
        if pygame.sprite.spritecollideany(self, player_group):
            self.kill()

            self.colvostars -= 1
            self.con = sqlite3.connect("froggame.sqlite")  # Подключение к БД
            self.cur = self.con.cursor()
            self.colvolive = ((self.cur.execute("""SELECT* FROM frog_piece""")).fetchall())[-1][1]
            self.cur.execute(
                f"INSERT INTO frog_piece (colvo_stars, colvo_live, time) VALUES('{self.colvostars}', '{self.colvolive}', '{self.time}')""")
            self.con.commit()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_num, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_num]
        self.image_boom = load_image('herogreen2.png', -1)
        self.rect = self.image.get_rect().move(
            tile_size * pos_x, tile_size * pos_y + offset)


class Monster(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(monster_group, all_sprites)
        self.image = monster_image[0]
        self.rect = self.image.get_rect().move(
            tile_size * pos_x, tile_size * pos_y + offset)
        self.ddt = 1
        self.dd = 0
        self.step = 2
        self.colvostars = 3
        self.time = str(dt.datetime.now().strftime("%d-%B-%y %H:%M:%S"))
        self.colvolive = 3

    def update(self):
        if self.ddt == 1:
            self.rect.x -= self.step
            self.dd += 1
            if self.dd == 100:
                self.ddt = 2
        if self.ddt == 2:
            self.dd -= 1
            self.rect.x += self.step
            if self.dd == 1:
                self.ddt = 1






class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_size * pos_x, tile_size * pos_y + offset)
        self.a = 0
        self.step = 3
        self.yyy = pos_y
        self.colvostars = 3
        self.time = str(dt.datetime.now().strftime("%d-%B-%y %H:%M:%S"))


    def table(self):
        self.con = sqlite3.connect("froggame.sqlite")  # Подключение к БД
        self.cur = self.con.cursor()
        colvolive = ((cur.execute("""SELECT* FROM frog_piece""")).fetchall())[-1][1]
        colvolive -= 1
        self.cur.execute(
            f"INSERT INTO frog_piece (colvo_stars, colvo_live, time) VALUES('{self.colvostars}', '{colvolive}', '{self.time}')""")
        self.con.commit()




    def left(self):
        if pygame.sprite.spritecollideany(self, monster_group):
            self.rect = self.image.get_rect().move(
                tile_size * 4, tile_size * 5 + offset)
            self.image = load_image('herogreen2.png', -1)

            self.table()

        elif pygame.sprite.spritecollideany(self, tiles_group):
            self.rect.x += 5

        elif not (pygame.sprite.spritecollideany(self, tiles_group)):
            self.rect.x -= self.step

    def right(self):
        if pygame.sprite.spritecollideany(self, tiles_group):
            print('ffff')
            self.rect.x -= 5

        elif pygame.sprite.spritecollideany(self, monster_group):
            self.rect = self.image.get_rect().move(
                tile_size * 6, tile_size * 5 + offset)
            self.image = load_image('herogreen2.png', -1)

            self.table()

        else:
            self.rect.x += self.step

    def up(self):
        if pygame.sprite.spritecollideany(self, tiles_group):
            print('ffff')
            self.rect.y += self.step

        elif pygame.sprite.spritecollideany(self, monster_group):
            self.rect = self.image.get_rect().move(
                tile_size * 6, tile_size * 5 + offset)
            self.image = load_image('herogreen2.png', -1)

            self.table()
        else:
            self.rect.y -= self.step

    def down(self):
        if pygame.sprite.spritecollideany(self, tiles_group):
            print('ffff')
            self.rect.y -= self.step
        elif pygame.sprite.spritecollideany(self, monster_group):
            self.rect = self.image.get_rect().move(
                tile_size * 6, tile_size * 5 + offset)
            self.image = load_image('herogreen2.png', -1)

            self.table()
        else:
            self.rect.y += self.step


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def load_level(screen, level_num):
    tile_type = {'.': 0, 'X': 1, 'T': 2, '$': 3, '@': 10, 'f':6}
    new_player, x, y = None, None, None
    new_monster, x, y = None, None, None
    all_sprites.empty()
    tiles_group.empty()
    player_group.empty()
    diamond_group.empty()
    monster_group.empty()
    startcord = []


    filename = f"data/level_{level_num:02d}.txt"






    with open(filename, 'r') as mapFile:
        level = [[tile_type[s] for s in line.strip()] for line in mapFile]
    for y in range(len(level)):
        for x in range(len(level[y])):
            screen.blit(tile_images[0], (tile_size * x, tile_size * y + offset))

            if level[y][x] == 10:
                startcord = [x, y]
                new_player = Player(x, y)
            elif level[y][x] == 6:
                new_monster = Monster(x, y)
            elif level[y][x] == 3:
                Stars(x, y)
            elif level[y][x]:
                Tile(level[y][x], x, y)

    return startcord, new_monster, new_player, len(level[0]), len(level)  # Возвращаем героя и размер уровня в клетках

def draw_level(screen):
    screen.fill('black')
    screen.blit(win, (0, 0))

def start_screen():
    intro_text = ["Правила игры",
                  "Клавиши со стрелками перемещают героя,",
                  "Ваша задача собрать все бонусы"]

    load_level(screen, 0)  # в загрузку уровня запихаем заставку, что бы он ее нам нарисовал
    tiles_group.draw(screen)   # тайтлы, входяище в группу отрисовываем на заставке
    font30 = pygame.font.Font(None, 30)  #создаем два шрифта
    font90 = pygame.font.Font(None, 90)

    string_rendered = font90.render('Моя игра', 1, 'yellow')
    rect = string_rendered.get_rect()  #узнаем размер по ширине
    rect.centerx = width // 2
    rect.y = 10
    screen.blit(string_rendered, rect)   #рисуем на ходсте шрифт в определенных координатах
    text_coord = offset + 130

    for line in intro_text:  #по строчке перебирать будем всю надпись
        string_rendered = font30.render(line, 1, pygame.Color('black'))
        rect = string_rendered.get_rect()
        text_coord += 10
        rect.top = text_coord
        rect.centerx = width // 2
        text_coord += rect.height
        screen.blit(string_rendered, rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return

        pygame.display.flip()
        clock.tick(FPS)



def end_screen():
    screen.fill((0,0,0))
    intro_text = ["КОНЕЦ ИГРЫ",
                  "Не расстраивайтесь,",
                  "Вы всегда можете попробовать снова"]

    load_level(screen, 0)  # в загрузку уровня запихаем заставку, что бы он ее нам нарисовал
    tiles_group.draw(screen)   # тайтлы, входяище в группу отрисовываем на заставке
    font30 = pygame.font.Font(None, 30)  #создаем два шрифта
    text_coord = offset + 130

    for line in intro_text:  #по строчке перебирать будем всю надпись
        string_rendered = font30.render(line, 1, pygame.Color('black'))
        rect = string_rendered.get_rect()
        text_coord += 10
        rect.top = text_coord
        rect.centerx = width // 2
        text_coord += rect.height
        screen.blit(string_rendered, rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                running = False
                pygame.quit()
                return
        pygame.display.flip()
        clock.tick(FPS)


def winend_screen():
    screen.fill((0,0,0))
    intro_text = ["КОНЕЦ ИГРЫ",
                  "Поздравляем,",
                  "Вы победили и можете начать снова"]

    load_level(screen, 0)  # в загрузку уровня запихаем заставку, что бы он ее нам нарисовал
    tiles_group.draw(screen)   # тайтлы, входяище в группу отрисовываем на заставке
    font30 = pygame.font.Font(None, 30)  #создаем два шрифта
    text_coord = offset + 130

    for line in intro_text:  #по строчке перебирать будем всю надпись
        string_rendered = font30.render(line, 1, pygame.Color('black'))
        rect = string_rendered.get_rect()
        text_coord += 10
        rect.top = text_coord
        rect.centerx = width // 2
        text_coord += rect.height
        screen.blit(string_rendered, rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                running = False
                pygame.quit()
                return
        pygame.display.flip()
        clock.tick(FPS)




start_screen()
camera = Camera()
running = True
startcoord, monster, player, level_size_x, level_size_y = load_level(screen, 1)


con = sqlite3.connect("froggame.sqlite")  # Подключение к БД
cur = con.cursor()
time = str(dt.datetime.now().strftime("%d-%B-%y %H:%M:%S"))
cur.execute(
f"INSERT INTO frog_piece (colvo_stars, colvo_live, time) VALUES('{3}', '{3}', '{time}')""")
con.commit()



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:


            con = sqlite3.connect("froggame.sqlite")  # Подключение к БД
            cur = con.cursor()
            time = str(dt.datetime.now().strftime("%d-%B-%y %H:%M:%S"))
            cur.execute(
                f"INSERT INTO frog_piece (time) VALUES('{time}')""")
            cur.execute(
                f"INSERT INTO history (timeend) VALUES('{time}')""")
            cur.execute(
                f"INSERT INTO frog_piece (colvo_stars, colvo_live, time) VALUES('{3}', '{3}', '--')""")
            con.commit()

            running = False
        if event.type == PLAYER_LEFT:
            player.left()
        if event.type == PLAYER_RIGHT:
            player.right()
        if event.type == PLAYER_UP:
            player.up()
        if event.type == PLAYER_DOWN:
            player.down()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.left()
                pygame.time.set_timer(PLAYER_LEFT, 50)
            elif event.key == pygame.K_RIGHT:
                player.right()
                pygame.time.set_timer(PLAYER_RIGHT, 50)
            elif event.key == pygame.K_UP:
                player.up()
                pygame.time.set_timer(PLAYER_UP, 50)
            elif event.key == pygame.K_DOWN:
                player.down()
                pygame.time.set_timer(PLAYER_DOWN, 50)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                pygame.time.set_timer(PLAYER_LEFT, 0)
            elif event.key == pygame.K_RIGHT:
                pygame.time.set_timer(PLAYER_RIGHT, 0)
            elif event.key == pygame.K_UP:
                pygame.time.set_timer(PLAYER_UP, 0)
            elif event.key == pygame.K_DOWN:
                pygame.time.set_timer(PLAYER_DOWN, 0)

    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    draw_level(screen)  #отрисовать спрайты
    all_sprites.draw(screen)  #отрисовать все спрайты
    all_sprites.update()  #обновить все спрайты



    con = sqlite3.connect("froggame.sqlite")  # Подключение к БД
    cur = con.cursor()
    colvolive = ((cur.execute("""SELECT* FROM frog_piece""")).fetchall())[-1][1]
    colvostars = ((cur.execute("""SELECT* FROM frog_piece""")).fetchall())[-2][1]
    con.commit()


    if colvolive == 0:
        end_screen()
    if colvostars == 0:
        winend_screen()


    intro_text = f"Количество жизней:{colvolive} "
    text_coord = offset + 130
    font60 = pygame.font.Font(None, 60)
    string_rendered = font60.render(intro_text, 1, pygame.Color('black'))
    rect = string_rendered.get_rect()
    text_coord -= 170
    rect.top = text_coord
    rect.centerx = width - width // 1.3
    text_coord += rect.height
    screen.blit(string_rendered, rect)

    pygame.display.flip()
    clock.tick(50)


con = sqlite3.connect("froggame.sqlite")  # Подключение к БД
cur = con.cursor()
cur.execute(
f"INSERT INTO frog_piece (colvo_stars, colvo_live, time) VALUES('{3}', '{3}', '{time}')""")
con.commit()

pygame.quit()
