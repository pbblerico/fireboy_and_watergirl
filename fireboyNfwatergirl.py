import pygame as pg
from colors import *
from levels import *
from db import *

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
        self.minutes = 0
        self.seconds = 0
        self.paused_time = 0

    def to_clock(self, time_passed):
        self.minutes = time_passed//60
        self.seconds = time_passed%60

        return (self.minutes, self.seconds)

    def draw(self):     
        elapsed_time = (pg.time.get_ticks() - self.start_time) // 1000

        time = self.to_clock(elapsed_time)
        time_txt = str(time[0]).zfill(2) + ":" + str(time[1]).zfill(2)
        timer = create_text_shape(time_txt, font2, YELLOW, size[0]//2, tile_size//2)
        screen.blit(timer[0], timer[1])

class Doors():
    def __init__(self, fire_pos, water_pos):
        self.water = load_img_and_shape(pg.image.load('res/water_door.png'), tile_size, tile_size, water_pos[0] * tile_size, water_pos[1] * tile_size)
        self.fire = load_img_and_shape(pg.image.load('res/fire_door.png'), tile_size, tile_size, fire_pos[0] * tile_size, fire_pos[1] * tile_size)
    
    def opened_door(self, door):
        door = load_img_and_shape(pg.image.load('res/opened_water.png'), tile_size, tile_size, door[1].x, door[1].y)
        return door
    
    def closed_door(self, door, img_path):
        door = load_img_and_shape(pg.image.load(img_path), tile_size, tile_size, door[1].x, door[1].y)
        return door

    def draw(self):
        screen.blit(self.water[0], self.water[1])
        screen.blit(self.fire[0], self.fire[1])

# class Block():
    

class Level():
    def __init__(self,id, level_info):
        self.id = id
        self.tile_list = []
        self.level_info = level_info
        self.jam_taken = False
        map = level_info.get("map")

        wall_img = pg.image.load('res/wall.png')
        # border_img = pg.image.load('res/wall_2.png')
        stone = pg.image.load('res/stone_with_grass.png')

        fire_pos = []
        water_pos = []
        for row in range(len(map)):
            for col in range(len(map[0])):
                tile = map[row][col]
                # print(row, col, map[row][col])
                if tile == 1:
                    img = load_img_and_shape(wall_img, tile_size, tile_size, row * tile_size, col * tile_size)
                elif tile == 2:
                    img = load_img_and_shape(stone, tile_size, tile_size, row * tile_size, col * tile_size)
                elif tile == 3:
                    fire_pos = [row, col]
                elif tile == 4:
                    water_pos = [row, col]

                self.tile_list.append(img)
        self.doors = Doors(fire_pos, water_pos)


    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            # pg.draw.rect(screen, (255, 255, 255), tile[1], 2)
        self.doors.draw()

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
        self.in_air = False
        self.jumped = False
        self.gravity = 0.1
        self.jump_velocity = -5

    def move(self):
        keys = pg.key.get_pressed()
        if keys[self.moving_keys[0]] and self.jumped == False:
            self.vel_y =self.jump_velocity
            self.jump_velocity += self.gravity
            self.jump_velocity = min(0, self.jump_velocity)
            self.jumped = True
            self.in_air = True
        # if keys[self.moving_keys[0]] and self.jumped == True:
        #     return
        if keys[self.moving_keys[0]] == False:
            self.jump_velocity = -5 #resets jump velocity
            self.jumped = False
            self.in_air = False

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

    def upd(self):
        dx = 0
        dy = 0
        # walk_cooldown = 5

		#get keypresses
        key = pg.key.get_pressed()
        if key[self.moving_keys[0]] and self.jumped == False:
            self.vel_y = -5
            self.jumped = True
        if key[self.moving_keys[0]] == False:
            self.jumped = False
        if key[self.moving_keys[2]]:
            dx -= 2
            # self.counter += 1
            self.direction = -1
        if key[self.moving_keys[3]]:
            dx += 2

		#add gravity
        self.vel_y += 0.1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

		#check for collision
        for tile in game.level.tile_list:
			#check for collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
			#check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				#check if below the ground i.e. jumping
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
				#check if above the ground i.e. falling
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0

		#update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > size[1]:
            self.rect.bottom = size[1]
            dy = 0

		#draw player onto screen
        screen.blit(self.img, self.rect)

    def draw(self):
        screen.blit(self.img, self.rect)


class Game():
    def __init__(self, level: Level, fireboy_coordinates, watergirl_coordinates, start_time):
        self.time = Clock(start_time)
        self.level = level
        self.score = 0
        self.finished = [False, False]
        self.fireboy = Player('res/fireboy.png', tile_size, tile_size, tile_size * fireboy_coordinates[0], tile_size * fireboy_coordinates[1], fireboy_moving_keys)
        self.watergirl = Player('res/watergirl.png', tile_size, tile_size, tile_size * watergirl_coordinates[0], tile_size * watergirl_coordinates[1], watergirl_moving_keys)
    
    def draw(self):
        global pause, level_fin

        self.level.draw()
        self.time.draw()

        pause_btn = Button(load_img_and_shape(pause_img, tile_size, tile_size, tile_size//2, tile_size//2, True))
        if pause_btn.draw() and pause == False:
            # self.time.paused_time = pg.time.get_ticks()
            pause = True

        if self.fireboy.rect.colliderect(self.level.doors.fire[1]):
            self.level.doors.fire = self.level.doors.opened_door(self.level.doors.fire)
            self.finished[0] = True
            # print("finished")
        else:
            self.finished[0] = False
            self.level.doors.fire = self.level.doors.closed_door(self.level.doors.fire, 'res/fire_door.png')
        if self.watergirl.rect.colliderect(self.level.doors.water[1]):
            self.level.doors.water = self.level.doors.opened_door(self.level.doors.water)
            self.finished[1] = True
        else:
            self.level.doors.water = self.level.doors.closed_door(self.level.doors.water, 'res/water_door.png')
            self.finished[1] = False
        if pause == False:
            self.fireboy.upd()
            self.watergirl.upd()
        
        if self.finished[0] == self.finished[1] == True:
            pg.time.wait(2000)
            pause = True
            level_fin = True


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
levels = [Level(1,level_one)]

#booleans which monitor the state of app 
run = True
level_one_completed = False
start_menu = True
game_started = False
pause = False
safe_win = False
savedGame = False
level_fin = False


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

def level_finished():
    global pause, level_fin
    save(game.score, game.level.id, game.fireboy.rect.x//tile_size, game.fireboy.rect.y//tile_size, game.level.jam_taken, game.watergirl.rect.x//tile_size, game.watergirl.rect.y//tile_size, game.finished[0] and game.finished[1], game.time.minutes * 60 + game.time.seconds)   
    level_finished_text = create_text_shape("Level finished", font1, YELLOW, size[0]//2, size[1]//3)
    continue_button = Button(create_text_shape("CONTINUE", font2, YELLOW, size[0]//2, size[1]-50))

    if continue_button.draw():
        print('yay')
        pass

    screen.blit(level_finished_text[0], level_finished_text[1])




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
        # time = game.time.to_clock(pg.time.get_ticks() - game.time.start_time // 1000)
        save(game.score, game.level.id, game.fireboy.rect.x//tile_size, game.fireboy.rect.y//tile_size, game.level.jam_taken, game.watergirl.rect.x//tile_size, game.watergirl.rect.y//tile_size, game.finished[0] and game.finished[1], game.time.minutes * 60 + game.time.seconds)
        game_started = False
        safe_win = False
        pause = False
        start_menu = True
        # pass
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

create_table()

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
    elif pause and not safe_win and not level_fin:
        game_paused()
    elif level_fin:
        level_finished()
    elif safe_win:
        save_game()

    # Update the display
    pg.display.update()

pg.quit()