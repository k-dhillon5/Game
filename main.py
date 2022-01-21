import pygame
import random
import math

#from pygame.display import init, update

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (50, 50, 255)
LIGHTBLUE = (0, 176, 240)
r = random.randrange(0, 256)
b = random.randrange(0, 256)
g = random.randrange(0, 256)
color = (r, g, b)
print(color)
pygame.init()

# Set the width and height of the screen [width, height]

width = 800
height = 500
screen = pygame.display.set_mode([width, height])

pygame.display.set_caption("Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# circle variables
circleX = 100
circleY = 100
radius = 10


class Ball(pygame.sprite.Sprite):
    speed = 6
    x = 0
    y = 180

    direction = 200
    width = 10
    height = 10

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(LIGHTBLUE)
        self.rect = self.image.get_rect()

        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

    def bounce(self, diff):
        self.direction = (180 - self.direction) % 360
        self.direction -= diff

    def update(self):
        direction_radians = math.radians(self.direction)

        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)

        self.rect.x = self.x
        self.rect.y = self.y

    # bounce off the top of the screen
        if self.y <= 0:
            self.bounce(0)
            self.y = 1

    # bounce off of left of screen
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1

    # bounce of of the right of the screen

        if self.x > self.screenwidth - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = self.screenwidth - self.width - 1

    # ball missed  the platform
        if self.y > 500:
            return "game over"
        else:
            return "game"


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = 75
        self.y = 15
        self.image = pygame.Surface([self.x, self.y])
        self.image.fill(WHITE)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()

        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        self.rect.x = 0
        self.rect.y = self.screenheight-self.y

    def update(self):

        pos = pygame.mouse.get_pos()
        # Set the left side of the player bar to the mouse position
        self.rect.x = pos[0]

        # off the right side of the screen
        if self.rect.x > self.screenwidth - self.x:
            self.rect.x = self.screenwidth - self.x


pygame.init()
screen = pygame.display.set_mode([800, 500])

block_width = 50
block_height = 20


class Block(pygame.sprite.Sprite):

    def __init__(self, color, x, y):

        # Call the parent class (Sprite) constructor
        super().__init__()

        # size
        self.image = pygame.Surface([block_width, block_height])

        # color
        self.image.fill(color)

        # dimensions
        self.rect = self.image.get_rect()

        # vector
        self.rect.x = x
        self.rect.y = y


# draw the font onto the screen
font = pygame.font.Font(None, 35)
# instructions
display_instructions = True
instruction_page = 1

# gamestate
game_state = "instructions"

# Instructions Function


def run_instructions():
    print("instructions")
    global instruction_page
    global done
    global game_state

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            instruction_page += 1
            if instruction_page == 3:
                game_state = "game"

    # set the screen background
    screen.fill(BLACK)
    if instruction_page == 1:
        # draw instructions, page 1
        text = font.render("PLATFORM GAME", True, WHITE)
        screen.blit(text, [300, 200])

        text = font.render("Click to play", True, WHITE)
        screen.blit(text, [325, 400])

    if instruction_page == 2:
        # draw instructions, page 2
        text = font.render(
            "Use the your mouse to control the platform. ", True, BLUE)
        screen.blit(text, [10, 230])
        text = font.render(
            "Use this platform to bounce the ball and hit the floating objects", True, BLUE)
        screen.blit(text, [10, 255])

        text = font.render("to make them all disapear!", True, BLUE)
        screen.blit(text, [10, 280])


# Game Function
background = pygame.Surface(screen.get_size())
blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()
allsprites = pygame.sprite.Group()


platform1 = Platform(50, 100)
allsprites.add(platform1)

all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(platform1)

ball = Ball()
allsprites.add(ball)
balls.add(ball)

# number of block to create
blocknum = 20
top = 10
for row in range(5):
    for column in range(0, blocknum):
        block = Block(color, column * (block_width + 2) + 1, top)
        blocks.add(block)
        allsprites.add(block)

    top += block_height + 2


def run_game():
    print("game")
    global done
    global game_state

    # --- Main event loop

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if not done:
        # Update the player and ball positions
        platform1.update()
        game_state = ball.update()

    if pygame.sprite.spritecollide(platform1, balls, False):
        diff = (platform1.rect.x + platform1.x/2) - \
            (ball.rect.x + ball.width/2)

        ball.rect.y = screen.get_height() - platform1.rect.y - ball.rect.y - 1
        ball.bounce(diff)

    deadblocks = pygame.sprite.spritecollide(ball, blocks, True)

    if len(deadblocks) > 0:
        ball.bounce(0)

    if len(blocks) == 0:
        done = True

    screen.fill(BLACK)
    allsprites.draw(screen)


def game_over():
    print("Game Over")
    global done
    global game_state

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            ball.y = 200
            done = True

    # set the screen background
    screen.fill(BLACK)
    # draw instructions, page 1
    text = font.render("Game Over", True, RED)
    screen.blit(text, [300, 200])

    text = font.render("Click to end game", True, WHITE)
    screen.blit(text, [260, 400])


# -------- Main Program Loop -----------
while not done:
    if game_state == "instructions":
        run_instructions()
    elif game_state == "game":
        run_game()
    elif game_state == "game over":
        game_over()

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
