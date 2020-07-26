#"Alien Invasion"
#Based on "Code this Game" by Meg Ray
#Coding done by Sensei Reiden
#Utilizes Pygame libraries
#7/26/2020

#NOTE: Some lines are broken up with a "\" at the end. This 
# indicates that the line following the "\" is the continuation 
# of the line before it.

#------------------------------------------------------------------ Import Libraries & Initialization

#Import libraries
import pygame
from pygame import *
from random import randint

#Initialize Pygame
pygame.init()

#Initialize Clock
clock = time.Clock()

#------------------------------------------------------------------ Constant Variables

#Game window parameters
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 600
WINDOW_RES = (WINDOW_WIDTH, WINDOW_HEIGHT)

#Tile parameters
WIDTH = 100
HEIGHT = 100

#Colors
WHITE = (255, 255, 255)

#Rates
SPAWN_RATE = 240
FRAME_RATE = 60

#Counters
STARTING_BUCKS = 20
BUCK_RATE = 180
STARTING_BUCK_BOOSTER = 1
ONE_MINUTE = FRAME_RATE * 60

#Win/lose conditions
MAX_BAD_REVIEWS = 5
WIN_TIME = ONE_MINUTE * 1

#Defined speeds
REG_SPEED = 2
SLOW_SPEED = 1

#Sprite health
ALIEN_HEALTH = 150

#Trap costs
WORMHOLE_COST = 5
METEOR_COST = 4
STARS_COST = 6

#------------------------------------------------------------------ Asset Loading

#Game window
GAME_WINDOW = display.set_mode(WINDOW_RES)
display.set_caption('Alien Invasion')

#Background image
background_img = image.load('Assets/galaxy.jpg')
background_surf = Surface.convert_alpha(background_img)
BACKGROUND = transform.scale(background_surf, WINDOW_RES)

#Alien image
alien_img = image.load('Assets/alien.png')
alien_surf = Surface.convert_alpha(alien_img)
ALIEN = transform.scale(alien_surf, (WIDTH, HEIGHT))

#Wormhole image
wormhole_img = image.load('Assets/wormhole.png')
wormhole_surf = Surface.convert_alpha(wormhole_img)
WORMHOLE = transform.scale(wormhole_surf, (WIDTH, HEIGHT))

#Meteor image
meteor_img = image.load('Assets/Meteor.png')
meteor_surf = Surface.convert_alpha(meteor_img)
METEOR = transform.scale(meteor_surf, (WIDTH, HEIGHT))

#Stars image
stars_img = image.load('Assets/stars.png')
stars_surf = Surface.convert_alpha(stars_img)
STARS = transform.scale(stars_surf,(WIDTH, HEIGHT))

#------------------------------------------------------------------ AlienSprite Class

#Creates instances of enemy type entities that move towards the 
# left side of the screen. Instances also can suffer from trap 
# effects and spwan in random rows. Does not take arguments.
class AlienSprite(sprite.Sprite):

    #METHOD: Sets up enemy instances
    def __init__(self):
        super().__init__()
        self.speed = REG_SPEED
        self.lane = randint(0, 4)
        all_aliens.add(self)
        self.image = ALIEN.copy()
        y = 50 + self.lane * 100
        self.rect = self.image.get_rect(center = (1100, y))
        self.health = ALIEN_HEALTH
    
    #METHOD: Sets up enemy movement
    def update(self, game_window, counters):
        #Erases last sprite image
        game_window.blit(BACKGROUND,\
            (self.rect.x, self.rect.y), self.rect)
        #Moves the sprites
        self.rect.x -= self.speed
        #Destroys sprite when at 0 health or at end
        if self.health <= 0 or self.rect.x <= 100:
            self.kill()
            #Increases bad reviews if enemy reaches end
            if self.rect.x <= 100:
                counters.bad_reviews += 1
        else: #Updates image
            game_window.blit(self.image, (self.rect.x, \
                self.rect.y))

    #METHOD: Applies trap effects to enemies
    def attack(self, tile):
        if tile.trap == SLOW:
            self.speed = SLOW_SPEED
        if tile.trap == DAMAGE:
            self.health -= 1

#------------------------------------------------------------------ Counters Class

#Creates an instance that keeps track of and displays 
# the various counters in the game. Takes alien_bucks, buck_rate, 
# buck_booster, and timer arguments
class Counters(object):

    #METHOD: Sets up instances of counters
    def __init__(self, alien_bucks, buck_rate, buck_booster, timer):
        #Starts the game loop counter at 0
        self.loop_count = 0
        #Sets up the font of the counter on the screen
        self.display_font = font.Font('Assets/pizza_font.ttf', 25)
        #Defines attributes using given arguments
        self.alien_bucks = alien_bucks
        self.buck_rate = buck_rate
        self.buck_booster = buck_booster
        self.bucks_rect = None
        self.timer = timer
        self.timer_rect = None
        self.bad_reviews = 0
        self.bad_rev_rect = None

    #METHOD: Sets the rate that the player earns alien bucks
    def increment_bucks(self):
        #Adds a set number of alien bucks to the player's total 
        # once every BUCK_RATE times the game loop runs
        if self.loop_count % self.buck_rate == 0:
            self.alien_bucks += self.buck_booster
    
    #METHOD: Displays alien bucks total to the screen
    def draw_bucks(self, game_window):
        #Tests if there is a new number of alien bucks
        if bool(self.bucks_rect):
            #Erases old number
            game_window.blit(BACKGROUND, (self.bucks_rect.x, \
                self.bucks_rect.y), self.bucks_rect)
        #Tells program what font & color to use in display
        bucks_surf = self.display_font.render (\
            str(self.alien_bucks), True, WHITE)
        #Sets up a rect to interact with the number
        self.bucks_rect = bucks_surf.get_rect()
        #Places display in the bucks section
        self.bucks_rect.x = WINDOW_WIDTH - 50
        self.bucks_rect.y = WINDOW_HEIGHT - 50
        #Displays new alien bucks total to game window
        game_window.blit(bucks_surf, self.bucks_rect)
    
    #METHOD: Displays bad reviews total to the screen
    def draw_bad_reviews(self, game_window):
        #Tests if there's a new number of bad reviews
        if bool(self.bad_rev_rect):
            #Erases old number
            game_window.blit(BACKGROUND, (self.bad_rev_rect.x, \
                self.bad_rev_rect.y), self.bad_rev_rect)
        #Tells program what font & color to use in display
        bad_rev_surf = self.display_font.render( \
            str(self.bad_reviews), True, WHITE)
        #Sets up a rect to interact with the number
        self.bad_rev_rect = bad_rev_surf.get_rect()
        #Places display in the bad reviews section
        self.bad_rev_rect.x = WINDOW_WIDTH - 150
        self.bad_rev_rect.y = WINDOW_HEIGHT - 50
        #Displays new bad reviews total to game window
        game_window.blit(bad_rev_surf, self.bad_rev_rect)

    #METHOD: Displays timer to the screen
    def draw_timer(self, game_window):
        #Tests if time has passed
        if bool(self.timer_rect):
            #Erases old number
            game_window.blit(BACKGROUND, (self.timer_rect.x, \
                self.timer_rect.y), self.timer_rect)
        #Tells program what font & color to use in display
        timer_surf = self.display_font.render(str( \
            #Displays how much time is left in seconds
            (WIN_TIME - self.loop_count) // FRAME_RATE), \
                True, WHITE)
        #Sets up a rect to interact with the number
        self.timer_rect = timer_surf.get_rect()
        #Places display in the timer section
        self.timer_rect.x = WINDOW_WIDTH - 250
        self.timer_rect.y = WINDOW_HEIGHT - 50
        #Displays new time to game window
        game_window.blit(timer_surf, self.timer_rect)
    
    #METHOD: Increments the loop counter and calls the other 
    # Counters methods
    def update(self, game_window):
        self.loop_count += 1
        self.increment_bucks()
        self.draw_bucks(game_window)
        self.draw_bad_reviews(game_window)
        self.draw_timer(game_window)

#------------------------------------------------------------------ Trap Class

#Creates instances of different trap types. Takes trap_kind, cost, 
# and trap_img arguments
class Trap(object):

    #METHOD: Sets up instances of each kind of trap
    def __init__(self, trap_kind, cost, trap_img):
        self.trap_kind= trap_kind
        self.cost = cost
        self.trap_img = trap_img

#------------------------------------------------------------------ TrapApplicator Class

#Creates an instance that selects and places traps on the play 
# field. Does not take arguments
class TrapApplicator(object):

    #METHOD: Sets up TrapApplicator instances
    def __init__(self):
        self.selected = None

    #METHOD: Selects trap if it is affordable
    def select_trap(self, trap):
        if trap.cost <= counters.alien_bucks:
            self.selected = trap

    #METHOD: Places the selected trap on a specific tile
    def select_tile(self, tile, counters):
        self.selected = tile.set_trap(self.selected, counters)

#------------------------------------------------------------------ BackgroundTile Class

#Parent class for tile types. Takes a rect argument
class BackgroundTile(sprite.Sprite):

    #METHOD: Sets up instances of background tiles
    def __init__(self, rect):
        super().__init__()
        self.trap = None
        self.rect = rect

#------------------------------------------------------------------ PlayTile Subclass

#Subclass of BackgroundTile class. Creates instances of tiles that 
# allow placement of traps. Takes a rect argument.
class PlayTile(BackgroundTile):

    #METHOD: Sets the trap on the selected play tile
    def set_trap(self, trap, counters):
        if bool(trap) and not bool(self.trap):
            counters.alien_bucks -= trap.cost
            self.trap = trap 
            if trap == EARN:
                counters.buck_booster += 1
        #If conditions are not met, nothing happens.
        return None
    
    #METHOD: Draws the trap image to the selected play tile
    def draw_trap(self, game_window, trap_applicator):
        if bool(self.trap):
            game_window.blit(self.trap.trap_img, \
                (self.rect.x, self.rect.y))

#------------------------------------------------------------------ ButtonTile Subclass

#Subclass of BackgroundTile class. Creates instances of tiles that
#  enables selection of traps and highlights when clicked. Takes a 
# rect argument
class ButtonTile(BackgroundTile):

    #METHOD: Enables selection of trap
    def set_trap(self, trap, counters):
        if counters.alien_bucks >= self.trap.cost:
            return self.trap
        else:
            return None

    #METHOD: Highlights the trap button that was clicked
    def draw_trap(self, game_window, trap_applicator):
        if bool(trap_applicator.selected):
            if trap_applicator.selected == self.trap:
                draw.rect(game_window, (238, 190, 47), \
                    (self.rect.x, self.rect.y, WIDTH, HEIGHT), 5)
    
#------------------------------------------------------------------ InactiveTile Subclass

#Subclass of BackgroundTile class. Creates instances of tiles that 
# does nothing when clicked and does not display anything. Takes a 
# rect argument
class InactiveTile(BackgroundTile):

    #METHOD: Do nothing if clicked
    def set_trap(self, trap, counters):
        return None
    
    #METHOD: Do not display anything
    def draw_trap(self, game_window, trap_applicator):
        pass

#------------------------------------------------------------------ Class Instances & Groups

#Group of all Alien instances
all_aliens = sprite.Group()

#Trap type instances
SLOW = Trap('SLOW', WORMHOLE_COST, WORMHOLE)
DAMAGE = Trap('DAMAGE', METEOR_COST, METEOR)
EARN = Trap('EARN', STARS_COST, STARS)

#Instance for TrapApplicator
trap_applicator = TrapApplicator()

#Instance for counters
counters = Counters(STARTING_BUCKS, BUCK_RATE, \
    STARTING_BUCK_BOOSTER, WIN_TIME)

#------------------------------------------------------------------ Background Grid

#Creates an empty list to hold the tile grid
tile_grid = []
#Defines the color of the grid outline
tile_color = WHITE

#Populates the background grid
for row in range(6):
    row_of_tiles = []
    tile_grid.append(row_of_tiles)
    for column in range(11):
        #Creates an invisible rect for each tile
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
                    #Button Tiles are assinged a trap type
                    new_tile.trap = [SLOW, DAMAGE, EARN][column-2]
                else:
                    #Creates InactiveTiles for the rest in row 5
                    new_tile = InactiveTile(rect)
            else:
                #Remaining space turns into PlayTiles
                new_tile = PlayTile(tile_rect)

        #Adds each tile to the correct row_of_tiles list
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

#Displays background image to the screen
GAME_WINDOW.blit(BACKGROUND, (0,0))

#------------------------------------------------------------------ Game Loop

#Defines the conditions for running the loop
game_running = True
program_running = True

#Starts game loop
while game_running:

    #-------------------------------------------------------------- Check for Events

    #Starts loop to check for and handle events
    for event in pygame.event.get():

        #Exits loop when the game window closes
        if event.type == QUIT:
            game_running = False
            program_running = False

        #Sets up the background tiles to respond to mouse clicks
        elif event.type == MOUSEBUTTONDOWN:
            #Gets the (x, y) coordinate where the mouse was 
            # clicked on screen
            coordinates = mouse.get_pos()
            x = coordinates[0]
            y = coordinates[1]

            #Finds the background tile at the location where the 
            # mouse was clicked and change the value of 
            # effect to True
            tile_y = y // 100
            tile_x = x // 100
            trap_applicator.select_tile(tile_grid[tile_y] \
                [tile_x], counters)

    #-------------------------------------------------------------- Spawning Sprites

    #Spawns alien sprites
    if randint(1, SPAWN_RATE) == 1:
        AlienSprite()

    #-------------------------------------------------------------- Collision Detection
    
    #Draws the background grid
    for tile_row in tile_grid:
        for tile in tile_row:
            if bool(tile.trap):
                GAME_WINDOW.blit(BACKGROUND, (tile.rect.x, \
                    tile.rect.y), tile.rect)

    #Sets up detection for collision with background tiles
    for alien in all_aliens:

        #Stores location of enemy's row
        tile_row = tile_grid[alien.rect.y // 100]
        #Stores location of enemy's left side
        vamp_left_side = alien.rect.x // 100
        #Stores location of enemy's right side
        vamp_right_side = (alien.rect.x + \
            alien.rect.width) // 100
        
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
            alien.attack(left_tile)

        #If touching a tile to the right...
        if bool(right_tile):
            #If both sides are not on the same tile...
            if right_tile != left_tile:
                #Attack if there's a trap
                alien.attack(right_tile)

    #-------------------------------------------------------------- Win/Lose Conditions

    #Lose Condition
    if counters.bad_reviews >= MAX_BAD_REVIEWS:
        game_running = False

    #Win Condition
    if counters.loop_count > WIN_TIME:
        game_running = False

    #-------------------------------------------------------------- Update Displays

    #Updates enemies
    for alien in all_aliens:
        alien.update(GAME_WINDOW, counters)

    #Updates traps that have been set
    for tile_row in tile_grid:
        for tile in tile_row:
            tile.draw_trap(GAME_WINDOW, trap_applicator)

    #Updates counters
    counters.update(GAME_WINDOW)

    #Updates all images on the screen
    display.update()

    #Sets the FPS
    clock.tick(FRAME_RATE)

#------------------------------------------------------------------ Endgame Message

#Sets up endgame font
end_font = font.Font('Assets/pizza_font.ttf', 50)

#Tests if either win or lose condition has been met
if program_running:
    #If player lost...
    if counters.bad_reviews >= MAX_BAD_REVIEWS:
        #Ending message would read "Game Over"
        end_surf = end_font.render('Game Over', True, WHITE)
    else: #Otherwise ending message would read "You Win!"
        end_surf = end_font.render('You Win!', True, WHITE)
    #Displays saved message to game window
    GAME_WINDOW.blit(end_surf, (350, 200))
    display.update()

#------------------------------------------------------------------ Endgame Loop

#Enables exit from end game message screen
while program_running:
    for event in pygame.event.get():
        #Listens for QUIT event
        if event.type == QUIT:
            program_running = False
    clock.tick(FRAME_RATE)

#------------------------------------------------------------------ Clean Up

#Quits game
pygame.quit()