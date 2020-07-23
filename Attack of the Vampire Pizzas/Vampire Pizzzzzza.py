#Import Libraries
import pygame
from pygame import*

#Initialize pygame
pygame.init()

#Define constant variables
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 400
WINDOW_RES = ((WINDOW_WIDTH, WINDOW_HEIGHT))

#Create window
GAME_WINDOW = display.set_mode(WINDOW_RES)
display.set_caption('Attack of the Vampire Pizzas!')
 
#---------------------------------------------------
#Start Main Game Loop
game_running = True
#Game Loop
while game_running:
    #Check for events
    for event in pygame.event.get():
        #Exit loop on quit
        if event.type == QUIT:
            game_running = False
    display.update()

#End of main game loop
#----------------------------------------------------
#Clean up game
pygame.quit()