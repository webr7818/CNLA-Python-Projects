#Set up game

#Import libraries
import pygame
from pygame import *
from random import randint

#Initialize Pygame
pygame.init()

#Set up clock
clock = time.Clock()

#---------------------------------------------------
#Define constant variables

#Define the parameters of the game window
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 600
WINDOW_RES = (WINDOW_WIDTH, WINDOW_HEIGHT)

#Define the tile parameters
WIDTH = 100
HEIGHT = 100

#Define colors
WHITE = (255, 255, 255)

#Set up rates
SPAWN_RATE = 360
FRAME_RATE = 60

#Define speeds
REG_SPEED = 2
SLOW_SPEED = 1

#---------------------------------------------------
#Load assests

#Create the game window
GAME_WINDOW = display.set_mode(WINDOW_RES)
display.set_caption('Attack of the Vampire Pizzas!')

#Set up the background image
background_img = image.load('Assets/restaurant.jpg')
background_surf = Surface.convert_alpha(background_img)
BACKGROUND = transform.scale(background_surf, WINDOW_RES)

#Set up the enemy image
pizza_img = image.load('Assets/vampire.png')
pizza_surf = Surface.convert_alpha(pizza_img)
VAMPIRE_PIZZA = transform.scale(pizza_surf, (WIDTH, HEIGHT))

#---------------------------------------------------
#Set up class objects

#Create an enemy object
class VampireSprite(sprite.Sprite):

    #Set up enemy instances
    def __init__(self):
        super().__init__()
        self.speed = REG_SPEED
        self.lane = randint(0, 4)
        all_vampires.add(self)
        self.image = VAMPIRE_PIZZA.copy()
        y = 50 + self.lane * 100
        self.rect = self.image.get_rect(center = (1100, y))
    
    #Set up enemy movement
    def update(self, game_window):
        
        #Erase the last sprite image
        game_window.blit(BACKGROUND,\
            (self.rect.x, self.rect.y), self.rect)
        #Move the sprites
        self.rect.x -= self.speed
        #Update the sprite image to the new location
        game_window.blit(self.image, (self.rect.x, self.rect.y))

#Create a background tile object
class BackgroundTile(sprite.Sprite):

    #Set up instances of background tiles
    def __init__(self, rect):
        super().__init__()
        self.effect = False
        self.rect = rect

#---------------------------------------------------
#Create class instances and groups

#Create a group for all the VampireSprite instances
all_vampires = sprite.Group()

#---------------------------------------------------
#Initialize and draw the background grid

#Create empty list to hold tile grid
tile_grid = []

#Define the color of the gird outline
tile_color = WHITE

#Populate the background grid
for row in range(6):
    row_of_tiles = []
    tile_grid.append(row_of_tiles)
    for column in range(11):
        tile_rect = Rect(WIDTH * column, HEIGHT * row,\
            WIDTH, HEIGHT)
        new_tile = BackgroundTile(tile_rect)
        row_of_tiles.append(new_tile)
        draw.rect(BACKGROUND, tile_color,\
            (WIDTH * column, HEIGHT * row, WIDTH, HEIGHT), 1)

#Display the background image to the screen
GAME_WINDOW.blit(BACKGROUND, (0,0))

#---------------------------------------------------
#Game loop

#Define the conditions for running the loop
game_running = True

#Start game loop
while game_running:

    #-----------------------------------------------
    #Check for events

    #Start loop to check for and handle events
    for event in pygame.event.get():

        #Exit loop when the game window closes
        if event.type == QUIT:
            game_running = False

        #Set up the background tiles to respond to mouse clicks
        elif event.type == MOUSEBUTTONDOWN:
            coordinates = mouse.get_pos()
            x = coordinates[0]
            y = coordinates[1]
            tile_y = y // 100
            tile_x = x // 100
            tile_grid[tile_y][tile_x].effect = True
            print('Clicked tile')


    #------------------------------------------------
    #Spawn sprites

    #Spawn vampire pizza sprites
    if randint(1, SPAWN_RATE) == 1:
        VampireSprite()
    #------------------------------------------------
    #Set up collision detection
    
    #Set up detection for collision with background tiles
    for vampire in all_vampires:
        tile_row = tile_grid[vampire.rect.y // 100]
        vamp_left_side = vampire.rect.x // 100
        vamp_right_side = (vampire.rect.x + \
            vampire.rect.width) // 100
        if 0 <= vamp_left_side <= 10:
            left_tile = tile_row[vamp_left_side]
        else:
            left_tile = None
        if 0 <= vamp_right_side <= 10:
            right_tile = tile_row[vamp_right_side]
        else:
            right_tile = None
        if bool(left_tile) and left_tile.effect:
            vampire.speed = SLOW_SPEED
        if bool(right_tile) and right_tile.effect:
            if right_tile != left_tile:
                vampire.speed = SLOW_SPEED
        if vampire.rect.x <= 0:
            vampire.kill()

    #------------------------------------------------
    #Update displays

    #Update enemies
    for vampire in all_vampires:
        vampire.update(GAME_WINDOW)

    #Update all images on the screen
    display.update()

    #Set the FPS
    clock.tick(FRAME_RATE)

#Close main game loop
#----------------------------------------------------

#Clean up game
pygame.quit()