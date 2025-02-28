import pygame
from game import Game
from display import Display

class Menu:
    def __init__(self):
        # Load a more appealing font
        self.title_font = pygame.font.Font(None, 60)  # Larger font for title
        self.option_font = pygame.font.Font(None, 40)  # Slightly larger font for options
        self.title = "Memory Match Game"
        
        # Store the text for options separately
        self.option_texts = [
            "Easy (4x4)",
            "Medium (6x6)",
            "Hard (8x8)",
            "Light Mode",
            "Dark Mode",
            "Close"
        ]
        
        # Render the options as surfaces
        self.options = [self.option_font.render(text, True, (255, 255, 255)) for text in self.option_texts]
        
        self.selected_mode = "Dark"  # Default mode
        self.hovered_option = None  # Track which option is hovered
        self.background_color = (0, 0, 0)  # Default background color (black for dark mode)
        self.text_color = (255, 255, 255)  # Default text color (white for dark mode)

    def draw(self, screen):
        # Set the background color
        screen.fill(self.background_color)

        # Draw title with the appropriate color
        title_color = (255, 255, 255) if self.selected_mode == "Dark" else (0, 0, 0)
        title_surface = self.title_font.render(self.title, True, title_color)
        screen.blit(title_surface, (300, 50))

        # Draw options with background rectangles
        for i, option in enumerate(self.options):
            option_rect = option.get_rect(center=(400, 150 + i * 50))
            # Change color based on hover
            if self.hovered_option == i:
                pygame.draw.rect(screen, (100, 100, 100), option_rect.inflate(20, 10))  # Darker background on hover
            else:
                # Use a lighter background color based on the selected mode
                background_color = (50, 50, 50) if self.selected_mode == "Dark" else (200, 200, 200)
                pygame.draw.rect(screen, background_color, option_rect.inflate(20, 10))  # Lighter background

            # Render option text with the current text color
            screen.blit(option, option_rect)

    def handle_click(self, pos):
        if 350 <= pos[0] <= 450:  # Adjusted width range for options
            for i in range(len(self.options)):
                if 150 + i * 50 - 20 <= pos[1] <= 150 + i * 50 + 20:  # Adjusted height range for options
                    if i == 0:
                        return 4  # easy
                    elif i == 1:
                        return 6  # medium
                    elif i == 2:
                        return 8  # hard
                    elif i == 3:
                        self.selected_mode = "Light"  # Set to light mode
                        self.background_color = (255, 255, 255)  # Change background to white
                        self.text_color = (0, 0, 0)  # Change text color to black
                        self.options = [self.option_font.render(text, True, self.text_color) for text in self.option_texts]  # Re-render options
                    elif i == 4:
                        self.selected_mode = "Dark"  # Set to dark mode
                        self.background_color = (0, 0, 0)  # Change background to black
                        self.text_color = (255, 255, 255)  # Change text color to white
                        self.options = [self.option_font.render(text, True, self.text_color) for text in self.option_texts]  # Re-render options
                    break
        if 380 <= pos[0] <= 460 and 450 <= pos[1] <= 486:
            pygame.quit()
            exit()
        return None

    def update_hover(self, pos):
        self.hovered_option = None  # Reset hovered option
        if 350 <= pos[0] <= 450:  # Adjusted width range for options
            for i in range(len(self.options)):
                if 150 + i * 50 - 20 <= pos[1] <= 150 + i * 50 + 20:  # Adjusted height range for options
                    self.hovered_option = i  # Set hovered option
                    break

def main():
    pygame.init()
    display = Display(pygame.display.Info().current_w, pygame.display.Info().current_h, fullscreen=True)
    game = None
    menu = Menu()

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game:
                    if game.game_over:
                        game = game.reset()  # Reset the game
                    else:
                        game.handle_click(pygame.mouse.get_pos())
                else:
                    difficulty = menu.handle_click(pygame.mouse.get_pos())
                    if difficulty:
                        game = Game(difficulty, menu.selected_mode)  # Pass the selected mode
            elif event.type == pygame.MOUSEMOTION:
                menu.update_hover(pygame.mouse.get_pos())  # Update hovered option

        display.clear()
        if game:
            game.update()
            game.draw(display.screen)
        else:
            menu.draw(display.screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()