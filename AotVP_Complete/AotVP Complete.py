#Set up game

#Import libraries
import pygame
from pygame import *

#Initialize Pygame
pygame.init()

#---------------------------------------------------
#Define constant variables

#Define the parameters of the game window
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 400
WINDOW_RES = (WINDOW_WIDTH, WINDOW_HEIGHT)

#---------------------------------------------------
#Load assests

#Create window
GAME_WINDOW = display.set_mode(WINDOW_RES)
display.set_caption('Attack of the Vampire Pizzas!')

pizza_img = image.load('Assets/vampire.png')
pizza_surf = Surface.convert_alpha(pizza_img)
VAMPIRE_PIZZA = transform.scale(pizza_surf, (100, 100))
GAME_WINDOW.blit(VAMPIRE_PIZZA, (150, 150))

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