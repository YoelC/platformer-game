import pygame
from classes.tile import Tile


class NoteTile(Tile):
    def __init__(self, pos, tile):
        super().__init__(pos, tile, collision=False)
        self.width, self.height = 7, 30
        self.looking_right = False
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((255, 251, 191))
        self.reading = False

        self.text = f'Debug text ({tile})'
        if tile == 5.01:
            self.text = "I don't know. I've been here for a while. I don't want to keep moving, I don't want to go deeper. If I do so, I might end up like all of these corpses. They looked like they died recently, too. I can't risk anything. I'll wait for rescue."
        if tile == 5.02:
            self.text = "I've seen some other people, none of them knowing how they got here. However, we all woke up with the same thought: Keep. Going. Down."
        if tile == 5.03:
            self.text = "Sorry! Out of order (Thanks for playing the demo!)"

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 64, 64)

    def draw(self, surface):
        x_offset = 0
        if self.looking_right:
            x_offset += 64 - self.width

        surface.blit(self.surface, (self.x + x_offset, self.y))
