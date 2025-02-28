import pygame
import random
import time
import os

pygame.init()
pygame.mixer.init()

class Card:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.revealed = False
        self.matched = False
        self.width = 80
        self.height = 120
        self.back_color = (200, 200, 200)
        self.flip_progress = 0
        self.flipping = False

    def draw(self, screen):
        if self.flipping:
            progress = self.flip_progress / 10
            if progress < 0.5:
                color = self.back_color
                width = int(self.width * (1 - progress * 2))
            else:
                color = self.color
                width = int(self.width * ((progress - 0.5) * 2))
            height = self.height
            pygame.draw.rect(screen, color, (self.x + (self.width - width) // 2, self.y, width, height))
        elif self.matched or self.revealed:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.back_color, (self.x, self.y, self.width, self.height))

        # border
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)

    def flip(self):
        self.flipping = True
        self.flip_progress = 0

    def update_flip(self):
        if self.flipping:
            self.flip_progress += 1
            if self.flip_progress >= 10:
                self.flipping = False
                self.revealed = not self.revealed

class Game:
    def __init__(self, size, mode):
        self.rows = size
        self.cols = size
        self.cards = []
        self.width = 80
        self.height = 120
        self.generate_cards()
        self.first_card = None
        self.second_card = None
        self.can_click = True
        self.score = 0
        self.moves = 0
        self.start_time = time.time()
        self.font = pygame.font.Font(None, 36)
        self.game_over = False

        # Set colors based on mode
        if mode == "Light":
            self.background_color = (255, 255, 255)  # White background for light mode
            self.text_color = (0, 0, 0)  # Black text for light mode
        else:  # Dark mode
            self.background_color = (0, 0, 0)  # Black background for dark mode
            self.text_color = (255, 255, 255)  # White text for dark mode

        # Sounds
        self.flip_sound = pygame.mixer.Sound(os.path.join('sounds', 'flip.mp3'))
        self.match_sound = pygame.mixer.Sound(os.path.join('sounds', 'match.mp3'))
        self.no_match_sound = pygame.mixer.Sound(os.path.join('sounds', 'failed.mp3'))

        # Close button properties
        self.close_button_rect = pygame.Rect(700, 10, 80, 40)  # (x, y, width, height)

    def generate_cards(self):
        colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
            (255, 0, 255), (0, 255, 255), (255, 128, 0), (128, 0, 255),
            (0, 128, 255), (128, 255, 0), (255, 0, 128), (0, 255, 128),
            (128, 128, 0), (128, 0, 128), (0, 128, 128), (192, 192, 192)
        ]
        num_pairs = (self.rows * self.cols) // 2
        if num_pairs > len(colors):
            raise ValueError("Not enough colors to generate pairs for the grid size.")
        
        random_colors = random.sample(colors, num_pairs) * 2  # Create pairs
        random.shuffle(random_colors)

        for i in range(self.rows):
            for j in range(self.cols):
                color = random_colors.pop()
                x = j * (self.width + 10) + 50
                y = i * (self.height + 10) + 150
                self.cards.append(Card(color, x, y))

    def draw(self, screen):
        # Set the background color
        screen.fill(self.background_color)

        # Draw cards
        for card in self.cards:
            card.draw(screen)

        # Draw score & time
        score_text = self.font.render(f"Score: {self.score}", True, self.text_color)
        moves_text = self.font.render(f"Moves: {self.moves}", True, self.text_color)
        time_text = self.font.render(f"Time: {int(time.time() - self.start_time)}s", True, self.text_color)

        screen.blit(score_text, (10, 10))
        screen.blit(moves_text, (10, 50))
        screen.blit(time_text, (10, 90))

        # Draw "Close" button
        pygame.draw.rect(screen, (200, 0, 0), self.close_button_rect)  # Red button
        close_text = self.font.render("Close", True, self.text_color)
        screen.blit(close_text, (self.close_button_rect.x + 10, self.close_button_rect.y + 10))

        # Game Over Screen
        if self.game_over:
            overlay = pygame.Surface((800, 600))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            game_over_text = self.font.render("Game Over!", True, self.text_color)
            final_score_text = self.font.render(f"Final Score: {self.score}", True, self.text_color)
            play_again_text = self.font.render("Click to Return to Menu", True, self.text_color)

            screen.blit(game_over_text, (350, 250))
            screen.blit(final_score_text, (350, 300))
            screen.blit(play_again_text, (300, 350))

    def handle_click(self, pos):
        if not self.can_click or self.game_over:
            return

        # Check if Close button is clicked
        if self.close_button_rect.collidepoint(pos):
            pygame.quit()
            exit()  # Close the game

        for card in self.cards:
            if self.is_card_clicked(card, pos):
                if not card.revealed and not card.matched:
                    card.flip()
                    self.flip_sound.play()
                    if self.first_card is None:
                        self.first_card = card
                    elif self.second_card is None:
                        self.second_card = card
                        self.can_click = False
                break

    def is_card_clicked(self, card, pos):
        return (card.x <= pos[0] <= card.x + card.width and
                card.y <= pos[1] <= card.y + card.height)

    def update(self):
        for card in self.cards:
            card.update_flip()

        if self.first_card and self.second_card and not self.first_card.flipping and not self.second_card.flipping:
            self.moves += 1
            if self.first_card.color == self.second_card.color:
                self.first_card.matched = True
                self.second_card.matched = True
                self.score += 10
                self.match_sound.play()
            else:
                pygame.time.wait(500)
                self.first_card.flip()
                self.second_card.flip()
                self.score -= 1
                self.no_match_sound.play()
            
            self.first_card = None
            self.second_card = None
            self.can_click = True

        if all(card.matched for card in self.cards):
            self.game_over = True

    def reset(self):
        return Game(self.rows, self.mode)  # Ensure mode is passed correctly