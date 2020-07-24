#CHAPTER 11: Applying Traps
#CNLA Sensei Copy
#NOTE: Do not run program. Current program is missing elements 
# from future chapters.

#Import libraries
import pygame
from pygame import *
from random import randint

#Initialize Pygame
pygame.init()

#Set up clock
clock = time.Clock()

#------------------------------------------------------------
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

#Set up counters
STARTING_BUCKS = 15
BUCK_RATE = 120
STARTING_BUCK_BOOSTER = 1

#Define speeds
REG_SPEED = 2
SLOW_SPEED = 1

#----------------------------------------------------------------
#Load assests

#Create the game window
GAME_WINDOW = display.set_mode(WINDOW_RES)
display.set_caption('Attack of the Vampire Pizzas!')

#Background image
background_img = image.load('Assets/restaurant.jpg')
background_surf = Surface.convert_alpha(background_img)
BACKGROUND = transform.scale(background_surf, WINDOW_RES)

#Vampire Pizza image
pizza_img = image.load('Assets/vampire.png')
pizza_surf = Surface.convert_alpha(pizza_img)
VAMPIRE_PIZZA = transform.scale(pizza_surf, (WIDTH, HEIGHT))

#Garlic image
garlic_img = image.load('Assets/garlic.png')
garlic_surf = Surface.convert_alpha(garlic_img)
GARLIC = transform.scale(garlic_surf, (WIDTH, HEIGHT))

#Pizza Cutter image
cutter_img = image.load('Assets/pizzacutter.png')
cutter_surf = Surface.convert_alpha(cutter_img)
CUTTER = transform.scale(cutter_surf, (WIDTH, HEIGHT))

#Pepperoni
pepperoni_img = image.load('Assets/pepperoni.png')
pepperoni_surf = Surface.convert_alpha(pepperoni_img)
PEPPERONI = transform.scale(pepperoni_surf,(WIDTH, HEIGHT))

#----------------------------------------------------------------
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

#Create an object for tracking the game state-------------------
class Counters(object):

    #Set up instances of counters
    def __init__(self, pizza_bucks, buck_rate, buck_booster):
        #Start the game loop counter at 0
        self.loop_count = 0
        #Set up the look of the counter on the screen
        self.display_font = font.Font('Assets/pizza_font.ttf', 25)

        #Define attributes using given arguments
        self.pizza_bucks = pizza_bucks
        self.buck_rate = buck_rate
        self.buck_booster = buck_booster
        self.bucks_rect = None

    #Set the rate that the player earns pizza bucks
    def increment_bucks(self):
        #Add a set number of pizza bucks to the player's total 
        # once every 120 times the game loop runs
        if self.loop_count % self.buck_rate == 0:
            self.pizza_bucks += self.buck_booster
    
    #Display pizza bucks total on the screen
    def draw_bucks(self, game_window):
        #Erase the last number from the game window
        if bool(self.bucks_rect):
            game_window.blit(BACKGROUND, (self.bucks_rect.x, \
                self.bucks_rect.y), self.bucks_rect)
        bucks_surf = self.display_font.render (\
            str(self.pizza_bucks), True, WHITE)
        
        #Create a rect for bucks_surf
        self.bucks_rect = bucks_surf.get_rect()

        #Place the counter in the middle of the tile on the 
        # bottom-right corner
        self.bucks_rect.x = WINDOW_WIDTH - 50
        self.bucks_rect.y = WINDOW_HEIGHT - 50

        #Display new pizza bucks total to game window
        game_window.blit(bucks_surf, self.bucks_rect)
    
    #Increment the loop counter and call the other Counters methods
    def update(self, game_window):
        self.loop_count += 1
        self.increment_bucks()
        self.draw_bucks(game_window)

#Create a base trap object-----------------------------------------
class Trap(object):

    #Set up instances of each kind of trap
    def __init__(self, trap_kind, cost, trap_img):
        self.trap_kind= trap_kind
        self.cost = cost
        self.trap_img = trap_img

#Create an object that activates traps-----------------------------
class TrapApplicator(object):

    #Set up TrapApplicator instances
    def __init__(self):
        self.selected = None

    #Selects trap if it is affordable
    def select_trap(self, trap):
        if trap.cost <= counters.pizza_bucks:
            self.selected = trap

    #Places the selected trap on a specific tile
    def select_tile(self, tile, counters):
        self.selected = tile.set_trap(self.selected, counters)      #missing set_trap()

#Create a background tile object-----------------------------------
class BackgroundTile(sprite.Sprite):

    #Set up instances of background tiles
    def __init__(self, rect):
        super().__init__()
        self.effect = False
        self.rect = rect

#------------------------------------------------------------------
#Create class instances and groups

#Create a group for all the VampireSprite instances
all_vampires = sprite.Group()

#Create instances for each trap type
SLOW = Trap('SLOW', 5, GARLIC)
DAMAGE = Trap('DAMAGE', 3, CUTTER)
EARN = Trap('EARN', 7, PEPPERONI)

#Instance for TrapApplicator
trap_applicator = TrapApplicatior()

#Create an instance of Counters
counters = Counters(STARTING_BUCKS, BUCK_RATE, \
    STARTING_BUCK_BOOSTER)

#-----------------------------------------------------------------
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
        #Create an invisible rect for each background
        # tile sprite
        tile_rect = Rect(WIDTH * column, HEIGHT * row,\
            WIDTH, HEIGHT)

        #For each column in each row, create a new 
        # background tile sprite
        new_tile = BackgroundTile(tile_rect)

        #Add each background tile sprite to the correct
        # row_of_tiles list
        row_of_tiles.append(new_tile)
        draw.rect(BACKGROUND, tile_color,\
            (WIDTH * column, HEIGHT * row, WIDTH, HEIGHT), 1)

#Display the background image to the screen
GAME_WINDOW.blit(BACKGROUND, (0,0))

#-----------------------------------------------------------------
#Game loop

#Define the conditions for running the loop
game_running = True

#Start game loop
while game_running:

    #------------------------------------------------------------
    #Check for events

    #Start loop to check for and handle events
    for event in pygame.event.get():

        #Exit loop when the game window closes
        if event.type == QUIT:
            game_running = False

        #Set up the background tiles to respond to mouse clicks
        elif event.type == MOUSEBUTTONDOWN:

            #Get the (x, y) coordinate where the mouse was 
            # clicked on screen
            coordinates = mouse.get_pos()
            x = coordinates[0]
            y = coordinates[1]

            #Find the background tile at the location where the 
            # mouse was clicked and change the value of 
            # effect to True
            tile_y = y // 100
            tile_x = x // 100
            trap_applicator.select_tile(tile_grid[tile_y] \
                [tile_x], counters)

    #-----------------------------------------------------------
    #Spawn sprites

    #Spawn vampire pizza sprites
    if randint(1, SPAWN_RATE) == 1:
        VampireSprite()
    #------------------------------------------------------------
    #Set up collision detection
    
    #Set up detection for collision with background tiles
    for vampire in all_vampires:
        #Store vampire positions
        
        #Store the row where the vampire sprite is located
        tile_row = tile_grid[vampire.rect.y // 100]
        #Store the current location of the right edge of 
        # the vampire sprite
        vamp_left_side = vampire.rect.x // 100
        #Store the current location of the right edge of
        # the vampire sprite
        vamp_right_side = (vampire.rect.x + \
            vampire.rect.width) // 100
        
        #---------------------------------------------------------
        #Identify the tiles on the left and right sides
        
        #If the vampire sprite is on the grid, find which 
        # column the left side is on.
        if 0 <= vamp_left_side <= 10:
            left_tile = tile_row[vamp_left_side]
        #Return no column if the vampire sprite is not 
        # on the grid
        else:
            left_tile = None

        #If the vampire sprite is on the grid, find which 
        # column the right side is on.
        if 0 <= vamp_right_side <= 10:
            right_tile = tile_row[vamp_right_side]
        #Return no column if the vampire sprite is not 
        # on the grid
        else:
            right_tile = None

        #---------------------------------------------------------
        #Test for collision

        #Tests if the left side of the vampire pizza is 
        # touching a tile and if that tile has been clicked.
        if bool(left_tile) and left_tile.effect:
            #If true, change the vampire speed to 1.
            vampire.speed = SLOW_SPEED

        #Tests if the right side of the vampire pizza is 
        # touching a tile and if that tile has been clicked.
        if bool(right_tile) and right_tile.effect:
            #Tests if the right and left sides of the sprite 
            # are touching different tiles
            if right_tile != left_tile:
                #If both are true, changes speed to 1.
                vampire.speed = SLOW_SPEED

        #Deletes the vampire sprite when it leaves the screen
        if vampire.rect.x <= 0:
            vampire.kill()

    #------------------------------------------------------------
    #Update displays

    #Update enemies
    for vampire in all_vampires:
        vampire.update(GAME_WINDOW)

    #Update counters
    counters.update(GAME_WINDOW)

    #Update all images on the screen
    display.update()

    #Set the FPS
    clock.tick(FRAME_RATE)

#Close main game loop
#----------------------------------------------------------------

#Clean up game
pygame.quit()