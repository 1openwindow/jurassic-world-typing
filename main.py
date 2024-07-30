import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Font
FONT_SIZE = 48
font = pygame.font.Font(None, FONT_SIZE)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Typing Ninja")

# Button class


class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render(self.text, True, BLACK)
        text_x = self.x + (self.width - text_surface.get_width()) // 2
        text_y = self.y + (self.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# Letter class


class Letter:
    def __init__(self, char, x, y, speed):
        self.char = char
        self.x = x
        self.y = y
        self.speed = speed

    def draw(self, screen):
        text_surface = font.render(self.char, True, WHITE)
        screen.blit(text_surface, (self.x, self.y))

    def update(self):
        self.y += self.speed

# Generate a random letter


def generate_letter():
    char = chr(random.randint(ord('A'), ord('Z')))
    x = random.randint(0, SCREEN_WIDTH - FONT_SIZE)
    y = 0
    speed = random.randint(2, 5)
    return Letter(char, x, y, speed)

# Main game function


def main():
    clock = pygame.time.Clock()
    letters = []
    score = 0
    game_started = False

    start_button = Button("Start", SCREEN_WIDTH // 2 - 100,
                          SCREEN_HEIGHT // 2 - 50, 200, 100, GREEN, BLUE)

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif not game_started and start_button.is_clicked(event):
                game_started = True

            if game_started and event.type == pygame.KEYDOWN:
                for letter in letters:
                    if event.unicode.upper() == letter.char:
                        letters.remove(letter)
                        score += 1
                        break

        if game_started:
            # Generate new letters
            if random.random() < 0.02:  # Adjust the rate of letter generation
                letters.append(generate_letter())

            # Update letters
            for letter in letters:
                letter.update()
                if letter.y > SCREEN_HEIGHT:
                    letters.remove(letter)

            # Draw letters
            for letter in letters:
                letter.draw(screen)

            # Draw score
            score_surface = font.render(f"Score: {score}", True, RED)
            screen.blit(score_surface, (10, 10))
        else:
            start_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
