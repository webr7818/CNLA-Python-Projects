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
        self.speed = 2
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

#---------------------------------------------------
#Create class instances and groups

#Create a group for all the VampireSprite instances
all_vampires = sprite.Group()

#---------------------------------------------------
#Initialize and draw the background grid

#Define the color of the gird outline
tile_color = WHITE

#Populate the background grid
for row in range(6):
    for column in range(11):
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

    #------------------------------------------------
    #Spawn sprites

    #Spawn vampire pizza sprites
    if randint(1, SPAWN_RATE) == 1:
        VampireSprite()
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