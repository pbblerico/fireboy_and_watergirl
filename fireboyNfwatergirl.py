import pygame as pg
from colors import *

pg.init()

font1 = pg.font.SysFont("Verdana", 36)
font2 = pg.font.SysFont("Verdana", 28)

size = (800, 600)
pg.display.set_caption("Fireboy and Watergirl")
screen = pg.display.set_mode(size)


def drawTextFun(text: str, font: pg.font.Font, color: tuple, centerx: int, centery: int):
    txt = font.render(text, True, color)
    txt_rect = txt.get_rect(center=(centerx, centery))

    return (txt, txt_rect)

tile_size = 40

def drawGrid():
    for i in range(0, 20):
        for j in range(0, 14):
            if(i != 0 and i != 19 and j != 0):
                # tile = drawImg(wall_img, tile_size, tile_size, i * tile_size, j * tile_size)
                pass
            else:
                tile = draw_img(wall_img, tile_size, tile_size, i * tile_size, j * tile_size)
            
            screen.blit(tile[0], tile[1])
    for i in range(1, 19):
        tile = draw_img(stone, tile_size, tile_size, i * tile_size, 14 * tile_size)
        screen.blit(tile[0], tile[1])
    # for l in range(0, 20):
    #     pg.draw.line(screen, WHITE, (0, l * tile_size), (size[0], l * tile_size))
    #     pg.draw.line(screen, WHITE, (l * tile_size, 0), (l * tile_size, size[1]))	
levelOne = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,2,0,0,2,0,0,2],
    [1,0,0,0,0,0,0,0,2,0,0,2,0,0,2],
    [1,0,0,0,0,2,0,0,2,0,0,2,0,0,2],
    [1,0,0,0,0,2,0,0,2,0,0,2,0,0,2],
    [1,0,0,0,0,2,0,0,2,0,0,0,0,0,2],
    [1,0,0,0,0,2,0,0,2,1,0,0,0,0,2],
    [1,0,0,0,0,2,0,0,0,2,0,0,0,0,2],
    [1,0,0,0,0,2,0,0,0,2,0,0,0,0,2],
    [1,0,0,0,0,2,0,0,0,2,0,0,0,0,2],
    [1,0,0,0,0,2,0,0,0,2,0,0,0,0,2],
    [1,0,0,0,0,2,0,0,0,2,0,0,0,0,2],
    [1,0,0,0,0,2,0,0,0,2,0,0,0,0,2],
    [1,0,0,0,0,2,0,0,0,2,0,0,0,0,2],
    [1,0,0,0,0,2,0,0,0,2,0,0,0,0,2],
    [1,0,0,0,0,2,0,0,0,2,0,0,0,0,2],
    [1,0,0,0,2,1,0,0,0,0,0,0,0,0,2],
    [1,0,0,0,2,1,0,0,0,0,0,0,0,2,1],
    [1,0,0,0,2,1,0,0,0,0,0,0,2,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

def draw_img(image: pg.surface.Surface, size_x: int, size_y: int, pos_x: int, pos_y: int, center: bool = False):
    img = pg.transform.scale(image, (size_x, size_y))
    img_rect = img.get_rect()
    if(center == False):
        img_rect.x = pos_x
        img_rect.y = pos_y
    else:
        img_rect.centerx = pos_x
        img_rect.centerx = pos_y
    tile = (img, img_rect)	

    return tile

def drawPause():
    screen.blit(pauseBtn[0], pauseBtn[1])

class Level():
    def __init__(self, level_info):
        self.tile_list = []

        wall_img = pg.image.load('res/wall.png')
        # border_img = pg.image.load('res/wall_2.png')
        stone = pg.image.load('res/stone_with_grass.png')
        for row in range(len(level_info)):
            for col in range(len(level_info[0])):
                tile = level_info[row][col]
                print(row, col, level_info[row][col])
                if tile == 1:
                    img = draw_img(wall_img, tile_size, tile_size, row * tile_size, col * tile_size)  
                elif tile == 2:
                    img = draw_img(stone, tile_size, tile_size, row * tile_size, col * tile_size)

                self.tile_list.append(img)
                    

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            # pg.draw.rect(screen, (255, 255, 255), tile[1], 2)             



class Player():
    def __init__(self, img_path: str, size_x: int, size_y: int, pos_x: int, pos_y: int, moving_keys: list):
        super().__init__()
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
        self.direction = [False, False]
    
    def move(self):
        keys = pg.key.get_pressed()
        if keys[self.moving_keys[0]] and self.jumped == False:
            self.vel_y = -15
            self.jumped = True
        if keys[self.moving_keys[0]] == False:
            self.jumped = False

        if keys[self.moving_keys[3]] != keys[self.moving_keys[2]]:
            if keys[self.moving_keys[3]]:
                self.direction[1] = True
                self.direction[0] = False
                self.vel_x = round(self.vel_x, 2) + self.acceleration
            else:
                self.direction[0] = True
                self.direction[1] = False
                self.vel_x = round(self.vel_x, 2) - self.acceleration
        if keys[self.moving_keys[2]] == keys[self.moving_keys[3]]:
            if(self.vel_x > 0):
                self.vel_x = max(round(self.vel_x, 2) - self.acceleration, 0)
            else: 
                self.vel_x = min(round(self.vel_x, 2) + self.acceleration, 0)

    def update(self):
        self.move()

        # dy = 0

        # self.vel_y += 1
        # if self.vel_y > 10:
        #     self.vel_y = 10
        # dy += self.vel_y

       

        # self.rect.y += dy

        self.vel_x = min(max(self.vel_x, self.vel_x_min), self.vel_x_max)
        # if self.rect.bottom > size[1]:
        #     self.rect.bottom = size[1]
        #     dy = 0
        
        # for tile in lvl1.tile_list:
		# 	#check for collision in x direction
        #     if tile[1].colliderect(self.rect.x + self.vel_x, self.rect.y, self.width, self.height):
        #         self.vel_x = 0
       
        self.rect.x += self.vel_x
        # if(self.direction[1]):
        #     self.rect.x += self.vel_x
        # else:
        #     self.rect.x -= self.vel_x
        
        self.rect.x = max(0, self.rect.x)
        self.rect.x = min(self.rect.x, size[0] - self.width)

       

        self.draw()

    def draw(self):
        screen.blit(self.img, self.rect)

run = True
levelOneCompleted = False
startMenu = True
gameStarted = False
pause = False
savedGame = False
start_btn = pg.Rect(250, 200, 200, 50)
playDraw = drawTextFun("PLAY", font2, YELLOW, size[0]//2, size[1]//3*2)
instructionsDraw = drawTextFun("INSTRUCTIONS", font2, YELLOW, playDraw[1].centerx, playDraw[1].centery+50)
statsDraw = drawTextFun("STATISTIC", font2, YELLOW, playDraw[1].centerx, instructionsDraw[1].centery+50)
continueDraw = drawTextFun("CONTINUE", font2, YELLOW, playDraw[1].centerx, instructionsDraw[1].centery+50)

lvl1 = Level(levelOne)

fireboy_moving_keys = [pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT]
watergirl_moving_keys = [pg.K_w, pg.K_s, pg.K_a, pg.K_d]
fireboy = Player('res/fireboy.png', tile_size, tile_size, tile_size, tile_size * 13, fireboy_moving_keys)
watergirl = Player('res/watergirl.png', tile_size, tile_size, tile_size, tile_size * 12, watergirl_moving_keys)

def welcome():
    fireboyDraw = drawTextFun("FIREBOY", font1, WELCOME_FIREBOY, size[0]//4, size[1]//3)

    andDraw = drawTextFun("&", font2, YELLOW, size[0]//2, size[1]//3)

    watergirlDraw = drawTextFun("WATERGIRL", font1, WELCOME_WATERGIRL, andDraw[1].centerx+( andDraw[1].centerx-fireboyDraw[1].centerx), size[1]//3)

    if(savedGame == True):
        continueDraw = drawTextFun("CONTINUE", font2, YELLOW, playDraw[1].centerx, playDraw[1].centery+50)
        global instructionsDraw 
        global statsDraw
        instructionsDraw = drawTextFun("INSTRUCTIONS", font2, YELLOW, playDraw[1].centerx, continueDraw[1].centery+50)
        statsDraw = drawTextFun("STATISTIC", font2, YELLOW, playDraw[1].centerx, instructionsDraw[1].centery+50)
        screen.blit(continueDraw[0], continueDraw[1])


    screen.blit(fireboyDraw[0], fireboyDraw[1])
    screen.blit(watergirlDraw[0], watergirlDraw[1])
    screen.blit(andDraw[0], andDraw[1])
    screen.blit(playDraw[0], playDraw[1])
    screen.blit(instructionsDraw[0], instructionsDraw[1])
    screen.blit(statsDraw[0], statsDraw[1])

def mainMenu():
    screen.blit(levelOneDraw[0], levelOneDraw[1])
    screen.blit(levelTwoDraw[0], levelTwoDraw[1])
    
def showTimer():
    elapsed_time = (pg.time.get_ticks() - start_time) // 1000
    timer = drawTextFun(toClock(elapsed_time), font2, YELLOW, size[0]//2, tile_size//2)
    screen.blit(timer[0], timer[1])

def toClock(time_passed):
    minutes = time_passed//60
    seconds = time_passed%60

    curTimer = str(minutes).zfill(2) + ":" + str(seconds).zfill(2)

    return curTimer



levelOneDraw = drawTextFun("Level 1", font1, YELLOW, size[0]//2, size[1]//3)
if(levelOneCompleted == False):
    levelTwoDraw =  drawTextFun("Level 2", font1, DARK_YELLOW, size[0]//2, levelOneDraw[1].centery+50)
else:
    levelTwoDraw =  drawTextFun("Level 2", font1, YELLOW, size[0]//2, levelOneDraw[1].centery+50)


start_time = 0

pause_img = pg.image.load('res/pause_2.png')
wall_img = pg.image.load('res/wall.png')
border_img = pg.image.load('res/wall_2.png')
stone = pg.image.load('res/stone_with_grass.png')

pauseBtn = draw_img(pause_img, tile_size, tile_size, tile_size//2, tile_size//2, True)

while(run):
    for i in pg.event.get():
        if i.type == pg.QUIT:
            run = False
        elif i.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            if(gameStarted == False):
                if playDraw[1].collidepoint(mouse_pos):
                    print("start")
                    startMenu = False
                    pause = False
                    start_time = pg.time.get_ticks()
                if levelOneDraw[1].collidepoint(mouse_pos):
                    gameStarted = True
                    print("level 1")
                if levelTwoDraw[1].collidepoint(mouse_pos) and levelOneCompleted == True:
                    print("level 2")
            if pauseBtn[1].collidepoint(mouse_pos):
                    pause = True   
                    
        # # pg.draw.rect(screen,WHITE, start_btn)
        # screen.blit(playTxt, play_rect)
        # print(type(font1))
    screen.fill(BLACK)
    if(startMenu != False):
        welcome()
    elif(startMenu == False and gameStarted == False):
        mainMenu()
    elif(startMenu == False and gameStarted == True):
        # drawGrid()
        lvl1.draw()
        drawPause()
        showTimer()
        fireboy.update()
        watergirl.update()

    if(pause == True):
        print(pause)    

    # Update the display
    pg.display.update()

pg.quit()