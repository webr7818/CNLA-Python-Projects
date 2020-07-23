#Set up game

#Import libraries
import pygame
from pygame import *

#Initialize Pygame
pygame.init()

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
#Initialize and draw the background grid

#Define the color of the gird outline
tile_color = WHITE

#Populate the background grid
for row in range(6):
    for column in range(11):
        draw.rect(BACKGROUND, tile_color, (WIDTH * column,\
        HEIGHT * row, WIDTH, HEIGHT), 1)

#Display the background image to the screen
GAME_WINDOW.blit(BACKGROUND, (0,0))
#Display the enemy image to the screen
GAME_WINDOW.blit(VAMPIRE_PIZZA, (900, 400))

#---------------------------------------------------
#Start main game loop

#Game loop
game_running = True
while game_running:

    #-----------------------------------------------
    #Check for events

    #Checking for and handling events
    for event in pygame.event.get():

        #Exit loop on quit
        if event.type == QUIT:
            game_running = False

    #--------------------------------------------
    #Update display.
    display.update()

#Close main game loop
#----------------------------------------------------

#Clean up game
pygame.quit()