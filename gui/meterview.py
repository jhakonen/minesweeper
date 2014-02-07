import pygame
from pygame import Rect

class MeterView(object):
	
	geometry = Rect(0, 0, 1, 1)
	count = 0

	def __init__(self, text):
		self.text = text
		self.font = pygame.font.SysFont("monospace", 15, bold=True)

	def paint(self, screen):
		self.paint_background(screen)
		self.paint_count(screen)

	def paint_background(self, screen):
		pygame.draw.rect(screen, (0, 0, 0), self.geometry)
		inner_rect = self.geometry.copy()
		inner_rect.inflate_ip(-4, -4)
		pygame.draw.rect(screen, (255, 255, 255), inner_rect)

	def paint_count(self, screen):
		text = self.font.render(self.text + ": " + str(self.count), 1, (0, 0, 0))
		text_pos = text.get_rect()
		text_pos.center = self.geometry.center
		screen.blit(text, text_pos)		
