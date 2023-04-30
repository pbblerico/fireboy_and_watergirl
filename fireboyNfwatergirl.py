import pygame as pg
from colors import *
from levels import *

#initializing py game
pg.init()


#fonts which will be used 
font1 = pg.font.SysFont("Verdana", 36)
font2 = pg.font.SysFont("Verdana", 28)


#define the screen
size = (800, 600)
pg.display.set_caption("Fireboy and Watergirl")
screen = pg.display.set_mode(size) 



#class which implements all clickable elements
class Button():
    def __init__(self, body: tuple):
        self.img = body[0] #interface of the button
        self.rect = body[1] #rectangle of the button
        self.clicked = False

    def draw(self):
        #boolean value which is monitoring whether button is clicked
        action = False

		#mouse position
        pos = pg.mouse.get_pos()

		#check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        #unclick
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

		#draw button
        screen.blit(self.img, self.rect)

        #returns state of the button, if activated action will be performed later
        return action
    
class Clock():
    def __init__(self, start_time):
        self.start_time = start_time
        self.paused_time = 0

    def to_clock(self, time_passed):
        mins = time_passed//60
        secs = time_passed%60

        return (mins, secs)

    def draw(self):     
        elapsed_time = (pg.time.get_ticks() - self.start_time) // 1000

        time = self.to_clock(elapsed_time)
        time_txt = str(time[0]).zfill(2) + ":" + str(time[1]).zfill(2)
        timer = create_text_shape(time_txt, font2, YELLOW, size[0]//2, tile_size//2)
        screen.blit(timer[0], timer[1])



class Level():
    def __init__(self, level_info):
        self.tile_list = []
        self.level_info = level_info
        map = level_info.get("map")

        wall_img = pg.image.load('res/wall.png')
        # border_img = pg.image.load('res/wall_2.png')
        stone = pg.image.load('res/stone_with_grass.png')

        for row in range(len(map)):
            for col in range(len(map[0])):
                tile = map[row][col]
                print(row, col, map[row][col])
                if tile == 1:
                    img = load_img_and_shape(wall_img, tile_size, tile_size, row * tile_size, col * tile_size)
                elif tile == 2:
                    img = load_img_and_shape(stone, tile_size, tile_size, row * tile_size, col * tile_size)

                self.tile_list.append(img)


    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            # pg.draw.rect(screen, (255, 255, 255), tile[1], 2)

class Player():
    def __init__(self, img_path: str, size_x: int, size_y: int, pos_x: int, pos_y: int, moving_keys: list):
        self.img = pg.transform.scale(pg.image.load(img_path), (size_x, size_y))
        self.moving_keys = moving_keys
        self.rect = self.img.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.vel_y = 0
        self.vel_x = 0
        self.vel_x_max = 1.5
        self.vel_x_min = -2
        self.acceleration = 0.2
        self.jumped = False

    def move(self):
        keys = pg.key.get_pressed()
        if keys[self.moving_keys[0]] and self.jumped == False:
            self.vel_y = -15
            self.jumped = True
        if keys[self.moving_keys[0]] == False:
            self.jumped = False

        if keys[self.moving_keys[3]] != keys[self.moving_keys[2]]:
            if keys[self.moving_keys[3]]:
                self.vel_x = round(self.vel_x, 2) + self.acceleration
            else:
                self.vel_x = round(self.vel_x, 2) - self.acceleration
        if keys[self.moving_keys[2]] == keys[self.moving_keys[3]]:
            if(self.vel_x > 0):
                self.vel_x = max(round(self.vel_x, 2) - self.acceleration, 0)
            else:
                self.vel_x = min(round(self.vel_x, 2) + self.acceleration, 0)

    def update(self):
        self.move()

        self.vel_x = min(max(self.vel_x, self.vel_x_min), self.vel_x_max)

        self.rect.x += self.vel_x

        self.rect.x = max(0, self.rect.x)
        self.rect.x = min(self.rect.x, size[0] - self.width)

        self.draw()

    def draw(self):
        screen.blit(self.img, self.rect)


class Game():
    def __init__(self, level: Level, fireboy_coordinates, watergirl_coordinates, start_time):
        self.time = Clock(start_time)
        self.level = level
        self.fireboy = Player('res/fireboy.png', tile_size, tile_size, tile_size * fireboy_coordinates[0], tile_size * fireboy_coordinates[1], fireboy_moving_keys)
        self.watergirl = Player('res/watergirl.png', tile_size, tile_size, tile_size * watergirl_coordinates[0], tile_size * watergirl_coordinates[1], watergirl_moving_keys)
    
    def draw(self):
        global pause

        self.level.draw()
        self.time.draw()

        pause_btn = Button(load_img_and_shape(pause_img, tile_size, tile_size, tile_size//2, tile_size//2, True))
        if pause_btn.draw() and pause == False:
            # self.time.paused_time = pg.time.get_ticks()
            pause = True

        if pause == False:
            self.fireboy.update()
            self.watergirl.update()


#creates rectangle of the given text and returns tuple of text itself and the rect
def create_text_shape(text: str, font: pg.font.Font, color: tuple, centerx: int, centery: int):
    txt = font.render(text, True, color)
    txt_rect = txt.get_rect(center=(centerx, centery))

    return (txt, txt_rect)


tile_size = 40

#loads image and creates rectangle of the given text and returns tuple of text image and the rect
def load_img_and_shape(image: pg.surface.Surface, size_x: int, size_y: int, pos_x: int, pos_y: int, center: bool = False):
    img = pg.transform.scale(image, (size_x, size_y))
    img_rect = img.get_rect()
    if(center == False): #some pictures needed to be placed according to central coordinates, False by default
        img_rect.x = pos_x
        img_rect.y = pos_y
    else:
        img_rect.centerx = pos_x
        img_rect.centerx = pos_y
    tile = (img, img_rect)	

    return tile

fireboy_moving_keys = [pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT]
watergirl_moving_keys = [pg.K_w, pg.K_s, pg.K_a, pg.K_d]
# lvl_1 = Level(level_one)
levels = [Level(level_one)]

#booleans which monitor the state of app 
run = True
level_one_completed = False
start_menu = True
game_started = False
pause = False
safe_win = False
savedGame = False


def welcome():
    global start_menu, run

    fireboy_text = create_text_shape("FIREBOY", font1, WELCOME_FIREBOY, size[0]//3, size[1]//3)
    and_text = create_text_shape("&", font2, YELLOW, size[0]//2, size[1]//3)
    watergirl_text = create_text_shape("WATERGIRL", font1, WELCOME_WATERGIRL, and_text[1].centerx+(and_text[1].centerx-fireboy_text[1].centerx), size[1]//3)

    play_button = Button(create_text_shape("PLAY", font2, YELLOW, size[0]//2, size[1]//3*2))
    instructions_button = Button(create_text_shape("INSTRUCTIONS", font2, YELLOW, play_button.rect.centerx, play_button.rect.centery+50))
    stats_button = Button(create_text_shape("STATISTIC", font2, YELLOW, play_button.rect.centerx, instructions_button.rect.centery+50))
    exit_button = Button(create_text_shape("EXIT", font2, YELLOW, play_button.rect.centerx, stats_button.rect.centery+50))

    if play_button.draw():
        start_menu = False
        print("start")
    if instructions_button.draw():
        pass
    if stats_button.draw():
        pass
    if exit_button.draw():
        run = False

    screen.blit(fireboy_text[0], fireboy_text[1])
    screen.blit(watergirl_text[0], watergirl_text[1])
    screen.blit(and_text[0], and_text[1])


def main_menu():
    global level_one_completed, game_started, game
    level_one_button = Button(create_text_shape("Level 1", font1, YELLOW, size[0]//2, size[1]//3))

    level_two_color = YELLOW if level_one_completed else DARK_YELLOW
    level_two_button = Button(create_text_shape("Level 2", font1, level_two_color, size[0]//2, level_one_button.rect.centery+50))

    continue_color = YELLOW if level_one_completed else DARK_YELLOW
    continue_button = Button(create_text_shape("CONTINUE", font2, continue_color, size[0]//2, size[1]-50))

    if level_one_button.draw():
        game = Game(levels[0], levels[0].level_info.get("fireboy_coordinates"), levels[0].level_info.get("watergirl_coordinates"), pg.time.get_ticks())
        game_started = True
    if level_two_button.draw() and level_one_completed:
        pass
    if continue_button.draw() and level_one_completed:
        pass

def game_paused():
    global pause, safe_win

    pause_text = create_text_shape("PAUSE", font1, YELLOW, size[0]//2, size[1]//4)
    resume_button = Button(create_text_shape("RESUME", font2, YELLOW, size[0]//2, size[1]//2))
    exit_button = Button(create_text_shape("EXIT", font2, YELLOW, size[0]//2, resume_button.rect.centery+50))

    if resume_button.draw():
        pause = False
    if exit_button.draw():
        safe_win = True
    game.time.draw()

    screen.blit(pause_text[0], pause_text[1])

def save_game():
    global pause, game_started, safe_win, start_menu

    save_text = create_text_shape("SAVE?", font1, YELLOW, size[0]//2, size[1]//4)
    yes_button = Button(create_text_shape("YES", font2, YELLOW, save_text[1].centerx - 50, save_text[1].centery + 50))
    no_button = Button(create_text_shape("NO", font2, YELLOW, save_text[1].centerx + 50, save_text[1].centery + 50))
    go_back = Button(load_img_and_shape(go_back_img, tile_size, tile_size, tile_size//2, tile_size//2, True))

    screen.blit(save_text[0], save_text[1])
    if yes_button.draw():
        pass
    if no_button.draw():
        game_started = False
        safe_win = False
        pause = False
        start_menu = True
    if go_back.draw():
        safe_win = False


game = Game(levels[0].level_info.get("map"), levels[0].level_info.get("fireboy_coordinates"), levels[0].level_info.get("watergirl_coordinates"), pg.time.get_ticks())

go_back_img = pg.image.load('res/go_back.png')
pause_img = pg.image.load('res/pause_2.png')
wall_img = pg.image.load('res/wall.png')
border_img = pg.image.load('res/wall_2.png')
stone = pg.image.load('res/stone_with_grass.png')


while(run):
    for i in pg.event.get():
        if i.type == pg.QUIT:
            run = False

    screen.fill(BLACK)
    if start_menu:
        welcome()
    elif game_started == False:
        main_menu()
    elif game_started and not pause:
        game.draw()
    elif pause and not safe_win:
        game_paused()
    elif safe_win:
        save_game()
        # game.draw()
        # screen.fill(pg.Color(0, 0, 0, 128))
#         # drawGrid()
#         lvl1.draw()
#         # drawPause()
#         showTimer()
#         fireboy.update()
#         watergirl.update()
# #
#     if(pause == True):
#         print(pause)

    # Update the display
    pg.display.update()

pg.quit()