import pygame
import random
import math
import sys
# Initialize Pygame and mixer


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()

# Define Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Display Dimensions
DIS_WIDTH = 800
DIS_HEIGHT = 600

# Create Display
dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Snake Game by Poornima')

# Clock to control game speed
clock = pygame.time.Clock()

# Snake Block Size and Speed
SNAKE_BLOCK = 20
BASE_SNAKE_SPEED = 10

# Font Style
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)
font = pygame.font.SysFont('Arial', 24)
player_name = input("Please Enter you name: ")



# Load sounds with error handling
try:
    eat_sound = pygame.mixer.Sound("mamge.mp3")
    eat_sound.play()
    
    game_over_sound = pygame.mixer.Sound("game_over.wav")
except pygame.error as e:
    print(f"Error loading sound files: {e}")
    eat_sound = None
    game_over_sound = None

# Draw star for food
def draw_star(surface, color, center, size):
    x, y = center
    points = [
        (x, y - size),
        (x + size // 3, y - size // 3),
        (x + size, y),
        (x + size // 3, y + size // 3),
        (x, y + size),
        (x - size // 3, y + size // 3),
        (x - size, y),
        (x - size // 3, y - size // 3)
    ]
    pygame.draw.polygon(surface, color, points)

# Draw snake with custom shapes
def our_snake(snake_block, snake_list):
    for index, x in enumerate(snake_list):
        if index == len(snake_list) - 1:
            # Draw snake head as a yellow circle with an eye
            pygame.draw.circle(dis, YELLOW, (x[0] + snake_block // 2, x[1] + snake_block // 2), snake_block // 2)
            pygame.draw.circle(dis, BLACK, (x[0] + snake_block // 3, x[1] + snake_block // 3), 2)
        else:
            # Draw body as a green rectangle with a border
            pygame.draw.rect(dis, GREEN, [x[0], x[1], snake_block, snake_block])
            pygame.draw.rect(dis, (0, 100, 0), [x[0], x[1], snake_block, snake_block], 2)
    
    
    
    # display the name of the current play
    
def draw_player_name(name):
    text_surface = font.render(f"Player: {name}", True, YELLOW)
    text_width = text_surface.get_width()
    dis.blit(text_surface, (DIS_WIDTH - text_width , 10))

# Display score
def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, YELLOW) 
    dis.blit(value, [0, 0])
    draw_player_name(player_name)
 

# Display message
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [DIS_WIDTH / 6, DIS_HEIGHT / 3])
    
    
        
# Game loop
def gameLoop():
    game_over = False
    game_close = False

    # Starting Position
    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2

    # Movement
    x1_change = 0
    y1_change = 0

    # Snake List and Length
    snake_list = []
    length_of_snake = 1

    # Food Position
    foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 20.0) * 20.0
    foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 20.0) * 20.0

    while not game_over:
        while game_close:
            dis.fill(BLUE)
            message("You Lost! Press Q-Quit or C-Play Again", RED)
            your_score(length_of_snake - 1)
            
            
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        # Reset game state
                        x1 = DIS_WIDTH / 2
                        y1 = DIS_HEIGHT / 2
                        x1_change = 0
                        y1_change = 0
                        snake_list = []
                        length_of_snake = 1
                        foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 20.0) * 20.0
                        foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 20.0) * 20.0
                        game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

        # Check Boundaries
        if x1 >= DIS_WIDTH or x1 < 0 or y1 >= DIS_HEIGHT or y1 < 0:
            game_close = True
            if game_over_sound:
                pygame.mixer.Sound.play(game_over_sound)

        # Update snake position
        x1 += x1_change
        y1 += y1_change
        dis.fill(BLUE)

        # Draw food as a pulsing red star
        pulse = (math.sin(pygame.time.get_ticks() / 500) + 1) / 2
        star_size = SNAKE_BLOCK // 2 + int(pulse * 2)
        draw_star(dis, RED, (foodx + SNAKE_BLOCK // 2, foody + SNAKE_BLOCK // 2), star_size)

        # Update snake
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check for self-collision
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True
                if game_over_sound:
                    pygame.mixer.Sound.play(game_over_sound)

        # Draw snake and score
        our_snake(SNAKE_BLOCK, snake_list)
        your_score(length_of_snake - 1)

        # Check if snake eats food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 20.0) * 20.0
            foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 20.0) * 20.0
            length_of_snake += 1
            if eat_sound:
                pygame.mixer.Sound.play(eat_sound)

        # Update display
        pygame.display.update()

        # Adjust speed based on score
        snake_speed = BASE_SNAKE_SPEED + (length_of_snake // 5)
        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Start the game
gameLoop()