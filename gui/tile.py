import pygame
from pygame import Rect

class TileRenderer(object):
	def __init__(self):
		self.geometry = Rect(0, 0, 1, 1)
	
	def set_geometry(self, rect):
		self.geometry = rect

	def paint(self, screen):
		pygame.draw.rect(screen, (0, 0, 0), self.geometry)
		inner_rect = self.geometry.copy()
		inner_rect.inflate_ip(-2, -2)
		pygame.draw.rect(screen, (255, 255, 255), inner_rect)
