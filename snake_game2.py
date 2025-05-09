import pygame
import time
import random

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Define colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Set game window dimensions
DIS_WIDTH = 800
DIS_HEIGHT = 600

# Create the display
dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption("Snake Game by Poornima")

# Initialize clock
clock = pygame.time.Clock()

# Define snake properties
SNAKE_BLOCK = 20
BASE_SNAKE_SPEED = 15

# Initialize fonts
font_style = pygame.font.SysFont("arial", 50)
score_font = pygame.font.SysFont("arial", 35)

# Load sounds
try:
    eat_sound = pygame.mixer.Sound("eat.wav")
    game_over_sound = pygame.mixer.Sound("game_over.wav")
except pygame.error as e:
    print(f"Error loading sound files: {e}")
    eat_sound = None
    game_over_sound = None

# Load images
try:
    snake_head_img = pygame.image.load("snake_head.png")
    snake_body_img = pygame.image.load("snake_body.png")
    food_img = pygame.image.load("food.png")
    
    # Scale images to match SNAKE_BLOCK size
    snake_head_img = pygame.transform.scale(snake_head_img, (SNAKE_BLOCK, SNAKE_BLOCK))
    snake_body_img = pygame.transform.scale(snake_body_img, (SNAKE_BLOCK, SNAKE_BLOCK))
    food_img = pygame.transform.scale(food_img, (SNAKE_BLOCK, SNAKE_BLOCK))
except pygame.error as e:
    print(f"Error loading image files: {e}")
    snake_head_img = None
    snake_body_img = None
    food_img = None

# Get user input
user_name = input("Please, what is your name? ")
print("Welcome to Snake Crash!")
print(f"Thanks, {user_name}!")

# Draw the snake
def our_snake(snake_block, snake_list):
    for index, x in enumerate(snake_list):
        if snake_head_img and snake_body_img:
            if index == len(snake_list) - 1:
                dis.blit(snake_head_img, (x[0], x[1]))
            else:
                dis.blit(snake_body_img, (x[0], x[1]))
        else:
            # Fallback to rectangles if images fail to load
            pygame.draw.rect(dis, BLACK, [x[0], x[1], snake_block, snake_block])

# Display the score
def your_score(score):
    value = score_font.render(f"Your Score: {score}", True, YELLOW)
    dis.blit(value, [0, 0])

# Display a message
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [DIS_WIDTH / 6, DIS_HEIGHT / 3])

# Game loop
def gameLoop():
    game_over = False
    game_close = False

    # Initialize snake position
    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2

    # Initialize movement
    x1_change = 0
    y1_change = 0

    # Initialize snake list and length
    snake_list = []
    length_of_snake = 1

    # Initialize food position
    foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 20.0) * 20.0
    foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 20.0) * 20.0

    while not game_over:
        while game_close:
            dis.fill(BLUE)
            message("You Lost! Press Q to Quit or C to Play Again", RED)
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

        # Check boundaries
        if x1 >= DIS_WIDTH or x1 < 0 or y1 >= DIS_HEIGHT or y1 < 0:
            game_close = True
            if game_over_sound:
                pygame.mixer.Sound.play(game_over_sound)

        # Update snake position
        x1 += x1_change
        y1 += y1_change

        # Draw background
        dis.fill(BLUE)

        # Draw food
        if food_img:
            dis.blit(food_img, (foodx, foody))
        else:
            # Fallback to rectangle if image fails to load
            pygame.draw.rect(dis, GREEN, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])

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

        # Check for food collision
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 20.0) * 20.0
            foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 20.0) * 20.0
            length_of_snake += 1
            if eat_sound:
                pygame.mixer.Sound.play(eat_sound)

        # Draw snake and score
        our_snake(SNAKE_BLOCK, snake_list)
        your_score(length_of_snake - 1)

        # Update display
        pygame.display.update()

        # Adjust speed based on score
        snake_speed = BASE_SNAKE_SPEED + (length_of_snake // 5)
        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Start the game
gameLoop()