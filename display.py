import pygame

class Display:
    def __init__(self, width, height, fullscreen=False):
        flags = pygame.FULLSCREEN if fullscreen else 0
        self.screen = pygame.display.set_mode((width, height), flags)
        self.width = width
        self.height = height

    def clear(self):
        self.screen.fill((0, 0, 0))  # Clear screen with black
