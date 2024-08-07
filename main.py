import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions (16:9 aspect ratio)
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Font sizes
FONT_SIZE = 72  # Increased font size for letters
font = pygame.font.Font("pixel_font.ttf", FONT_SIZE)
button_font = pygame.font.Font("pixel_font.ttf", 48)  # Font size for button

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Typing Ninja")

# Load background image
background_image = pygame.image.load("pixel_background.png")
background_image = pygame.transform.scale(
    background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load background music
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)  # Play the music indefinitely

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
        text_surface = button_font.render(self.text, True, BLACK)
        screen.blit(text_surface, (self.x + (self.width - text_surface.get_width()) // 2,
                                   self.y + (self.height - text_surface.get_height()) // 2))

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
        self.color = random.choice(
            [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, WHITE])

    def draw(self, screen):
        text_surface = font.render(self.char, True, self.color)
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
                          SCREEN_HEIGHT - 150, 200, 100, GREEN, BLUE)

    while True:
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

        # Draw background
        screen.blit(background_image, (0, 0))

        if game_started:
            # Draw letters
            for letter in letters:
                letter.draw(screen)

            # Draw score
            score_surface = button_font.render(f"Score: {score}", True, RED)
            screen.blit(score_surface, (10, 10))
        else:
            start_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
