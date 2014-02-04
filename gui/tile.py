import pygame
from pygame import Rect

class TileRenderer(object):
	geometry = Rect(0, 0, 1, 1)
	
	def paint(self, screen):
		pygame.draw.rect(screen, (0, 0, 0), self.geometry)
		inner_rect = self.geometry.copy()
		inner_rect.inflate_ip(-2, -2)

		inner_color = (255, 255, 255)
		if self.geometry.collidepoint(pygame.mouse.get_pos()):
			inner_color = (200, 200, 200)
		pygame.draw.rect(screen, inner_color, inner_rect)
