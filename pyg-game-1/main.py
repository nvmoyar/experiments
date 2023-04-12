# ==============================================================================
# Author: nvmoyar, Jose Ramón Fernandez Junquera
# Assisted by: OpenAI ChatGPT
# Date: 2023-04-11
# Description: A Python game featuring two balls. The controlled ball moves
#              using the arrow keys and gains points when colliding with the
#              random bouncing ball. The game ends when the user reaches 100 points.
# ==============================================================================


import pygame
import random
import time


if __name__ == "__main__":
 
    import pygame
    import random
    import time

    # Initialize Pygame
    pygame.init()

    # Define screen size and colors
    WIDTH, HEIGHT = 800, 600
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PENALIZING_TIME = 10 # SECONDS
    PENALIZING_POINTS = 10 
    PIXEL_SPEED = 10
    REWARD_POINTS = 15

    # Create the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Ball Collision Game')

    # Ball class definition
    class Ball:
        def __init__(self, x, y, radius, color, speed_x, speed_y):
            self.x = x
            self.y = y
            self.radius = radius
            self.color = color
            self.speed_x = speed_x
            self.speed_y = speed_y
            self.fill_alpha = 0  # Added attribute for fill color alpha

        #def draw(self, screen):
        #    pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

        def draw(self, screen):
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius, 2) # Added the width parameter for the contour
            if self.fill_alpha > 0:  # Draw the transparent red fill only if alpha > 0
                fill_surface = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA)
                fill_color = pygame.Color(255, 0, 0, self.fill_alpha)
                pygame.draw.circle(fill_surface, fill_color, (self.radius, self.radius), self.radius)
                screen.blit(fill_surface, (int(self.x) - self.radius, int(self.y) - self.radius))

        def collide(self, other):
            distance = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
            return distance <= self.radius + other.radius - 0.7 * min(self.radius, other.radius)  # Updated condition for more than 70% overlap


    # Random ball
    random_ball = Ball(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), 20, BLUE, random.choice([-10, 10]), random.choice([-10, 10]))

    # Controlled ball
    controlled_ball = Ball(WIDTH // 2, HEIGHT // 2, 20, RED, 0, 0)

    # Clock and timer
    clock = pygame.time.Clock()
    timer = 0
    points = 0
    collision_happened = False

    running = True
    while running:
        dt = clock.tick(60) / 1000
        timer += dt

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            controlled_ball.x -= PIXEL_SPEED
        if keys[pygame.K_RIGHT]:
            controlled_ball.x += PIXEL_SPEED
        if keys[pygame.K_UP]:
            controlled_ball.y -= PIXEL_SPEED
        if keys[pygame.K_DOWN]:
            controlled_ball.y += PIXEL_SPEED

        # Keep controlled ball within screen bounds
        controlled_ball.x = max(controlled_ball.radius, min(controlled_ball.x, WIDTH - controlled_ball.radius))
        controlled_ball.y = max(controlled_ball.radius, min(controlled_ball.y, HEIGHT - controlled_ball.radius))

        # Random ball movement
        random_ball.x += random_ball.speed_x
        random_ball.y += random_ball.speed_y

        if random_ball.x < 0 + random_ball.radius or random_ball.x > WIDTH - random_ball.radius:
            random_ball.speed_x *= -1
        if random_ball.y < 0 + random_ball.radius or random_ball.y > HEIGHT - random_ball.radius:
            random_ball.speed_y *= -1

  
       
        # Check for collisions
        if controlled_ball.collide(random_ball) and not collision_happened:
            points += REWARD_POINTS
            collision_happened = True
            controlled_ball.fill_alpha = int(points / 100 * 255)  # Update the fill_alpha based on the current score
            # controlled_ball.color = YELLOW  # Change the color to yellow
        elif not controlled_ball.collide(random_ball):
            collision_happened = False




        # Update timer
        if timer >= PENALIZING_TIME:
            points -= PENALIZING_POINTS
            timer = 0
            
        # Draw
        screen.fill(WHITE)
        random_ball.draw(screen)
        controlled_ball.draw(screen)

        if points >= 100: 
            font = pygame.font.Font(None, 50)
            win_text = font.render("Congratulations! You won!", True, BLACK)
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.delay(3000)  # Display the message for 3 seconds
        else:
            # Display points
            font = pygame.font.Font(None, 36)
            text = font.render(f'Points: {points}', True, BLACK)
            screen.blit(text, (10, 10))
            pygame.display.flip()

        # End the game if the user reaches 100 points
        if points >= 100:
            break  # Exit the game loop

    pygame.quit()
