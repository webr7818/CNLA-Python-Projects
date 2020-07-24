#"Attack of the Vampire Pizzas!"
#Based on "Code this Game" by Meg Ray
#Coding done by Sensei Reiden
#Utilizes Pygame libraries
#7/23/2020

#------------------------------------------------------------ Import Libraries & Initialization

#Import libraries
import pygame
from pygame import *
from random import randint

#Initialize Pygame
pygame.init()

#Set up clock
clock = time.Clock()

#------------------------------------------------------------ Constant Variables

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
SPAWN_RATE = 20
FRAME_RATE = 60

#Set up counters
STARTING_BUCKS = 15
BUCK_RATE = 120
STARTING_BUCK_BOOSTER = 1

#Define speeds
REG_SPEED = 2
SLOW_SPEED = 1

#---------------------------------------------------------------- Asset Loading

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

#----------------------------------------------------------------- VampireSprite Subclass
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
        self.health = 100
    
    #Set up enemy movement
    def update(self, game_window, counters):
        
        #Erase the last sprite image
        game_window.blit(BACKGROUND,\
            (self.rect.x, self.rect.y), self.rect)
        #Move the sprites
        self.rect.x -= self.speed
        #Destroys sprite when at 0 health
        if self.health <= 0 or self.rect.x <= 100:
            self.kill()
        else: #Updates image
            game_window.blit(self.image, (self.rect.x, \
                self.rect.y))

    #Apply trap effects to enemies
    def attack(self, tile):
        if tile.trap == SLOW:
            self.speed = SLOW_SPEED
        if tile.trap == DAMAGE:
            self.health -= 1

#------------------------------------------------------------------- Counters Class
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

#------------------------------------------------------------------ Trap Class
class Trap(object):

    #Set up instances of each kind of trap
    def __init__(self, trap_kind, cost, trap_img):
        self.trap_kind= trap_kind
        self.cost = cost
        self.trap_img = trap_img

#------------------------------------------------------------------ TrapApplicator Class
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
        self.selected = tile.set_trap(self.selected, counters)

#------------------------------------------------------------------ BackgroundTile Class
class BackgroundTile(sprite.Sprite):

    #Sets up instances of background tiles
    def __init__(self, rect):
        super().__init__()
        self.trap = None
        self.rect = rect

#------------------------------------------------------------------ PlayTile Subclass
class PlayTile(BackgroundTile): #Sets up tiles in the play area

    #Set the trap on the selected play tile
    def set_trap(self, trap, counters):
        if bool(trap) and not bool(self.trap):
            counters.pizza_bucks -= trap.cost
            self.trap = trap 
            if trap == EARN:
                counters.buck_booster += 1
        #If conditions are not met, nothing happens.
        return None
    
    #Draw the trap image to the selected play tile
    def draw_trap(self, game_window, trap_applicator):
        if bool(self.trap):
            game_window.blit(self.trap.trap_img, \
                (self.rect.x, self.rect.y))

#--------------------------------------------------------------------- ButtonTile Subclass
class ButtonTile(BackgroundTile): #Sets up trap tiles

    #Enables selection of trap
    def set_trap(self, trap, counters):
        if counters.pizza_bucks >= self.trap.cost:
            return self.trap
        else:
            return None

    #Highlights the trap button that was clicked
    def draw_trap(self, game_window, trap_applicator):
        if bool(trap_applicator.selected):
            if trap_applicator.selected == self.trap:
                draw.rect(game_window, (238, 190, 47), \
                    (self.rect.x, self.rect.y, WIDTH, HEIGHT), 5)
    
#---------------------------------------------------------------------- InactiveTile Subclass
class InactiveTile(BackgroundTile): #Sets up non-interactive tiles

    #Do nothing if clicked
    def set_trap(self, trap, counters):
        return None
    
    #Do not display anything
    def draw_trap(self, game_window, trap_applicator):
        pass

#---------------------------------------------------------------------- Class Instances & Groups

#Create a group for all the VampireSprite instances
all_vampires = sprite.Group()

#Create instances for each trap type
SLOW = Trap('SLOW', 5, GARLIC)
DAMAGE = Trap('DAMAGE', 3, CUTTER)
EARN = Trap('EARN', 7, PEPPERONI)

#Instance for TrapApplicator
trap_applicator = TrapApplicator()

#Create an instance of Counters
counters = Counters(STARTING_BUCKS, BUCK_RATE, \
    STARTING_BUCK_BOOSTER)

#----------------------------------------------------------------- Background Grid

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
        tile_rect = Rect(WIDTH * column, HEIGHT * row, \
            WIDTH, HEIGHT)

        #Creates InactiveTiles for the first two columns
        if column <= 1:
            new_tile = InactiveTile(tile_rect)
        else:
            #Tests for bottom row
            if row == 5:
                #Tests for tiles in columns 2, 3, and 4
                if 2 <= column <= 4:
                    new_tile = ButtonTile(tile_rect)
                    #Each button is assigned the corresponding 
                    # data type
                    new_tile.trap = [SLOW, DAMAGE, EARN][column-2]
                else:
                    #Creates InactiveTiles for the rest in row 5
                    new_tile = InactiveTile(rect)
            else:
                #Remaining space turns into PlayTiles
                new_tile = PlayTile(tile_rect)

        #Add each background tile sprite to the correct
        # row_of_tiles list
        row_of_tiles.append(new_tile)

        #Tests if tile is one of 3 buttons
        if row == 5 and 2 <= column <= 4:
            #Displays correct image on each button
            BACKGROUND.blit(new_tile.trap.trap_img, \
                (new_tile.rect.x, new_tile.rect.y))
        
        #Displays the background image anywhere else
        if column != 0 and row != 5:
            if column != 1:
                draw.rect(BACKGROUND, tile_color,\
                    (WIDTH * column, HEIGHT * row, \
                        WIDTH, HEIGHT), 1)

#Display the background image to the screen
GAME_WINDOW.blit(BACKGROUND, (0,0))

#----------------------------------------------------------------- Game Loop

#Define the conditions for running the loop
game_running = True

#Start game loop
while game_running:

    #------------------------------------------------------------ Check for Events

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

    #----------------------------------------------------------- Spawning Sprites

    #Spawn vampire pizza sprites
    if randint(1, SPAWN_RATE) == 1:
        VampireSprite()

    #------------------------------------------------------------ Collision Detection
    
    #Draws the background grid
    for tile_row in tile_grid:
        for tile in tile_row:
            if bool(tile.trap):
                GAME_WINDOW.blit(BACKGROUND, (tile.rect.x, \
                    tile.rect.y), tile.rect)

    #Set up detection for collision with background tiles
    for vampire in all_vampires:
        
        #Stores location of enemy's row
        tile_row = tile_grid[vampire.rect.y // 100]
        #Stores location of enemy's left side
        vamp_left_side = vampire.rect.x // 100
        #Stores location of enemy's right side
        vamp_right_side = (vampire.rect.x + \
            vampire.rect.width) // 100
        
        #If left side is on the grid...
        if 0 <= vamp_left_side <= 10:
            #Store tile to the left
            left_tile = tile_row[vamp_left_side]
        else: #Otherwise return no column
            left_tile = None

        #If right side is on the grid...
        if 0 <= vamp_right_side <= 10:
            #Store tile to the right
            right_tile = tile_row[vamp_right_side]
        else: #Otherwise return no column
            right_tile = None

        #If touching a tile to the left...
        if bool(left_tile):
            #Attack if there's a trap
            vampire.attack(left_tile)

        #If touching a tile to the right...
        if bool(right_tile):
            #If both sides are not on the same tile...
            if right_tile != left_tile:
                #Attack if there's a trap
                vampire.attack(right_tile)

    #------------------------------------------------------------ Update Displays

    #Update enemies
    for vampire in all_vampires:
        vampire.update(GAME_WINDOW, counters)

    #Update traps that have been set
    for tile_row in tile_grid:
        for tile in tile_row:
            tile.draw_trap(GAME_WINDOW, trap_applicator)

    #Update counters
    counters.update(GAME_WINDOW)

    #Update all images on the screen
    display.update()

    #Set the FPS
    clock.tick(FRAME_RATE)

#---------------------------------------------------------------- End of Loop

#Game clean up
pygame.quit()