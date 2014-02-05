
import pygame
from pygame import Rect

class BoardView(object):

	geometry = Rect(0, 0, 1, 1)
	rows = 1
	cols = 1
	tile_renderer = None
	pressed_tile = None

	def __init__(self, tile_renderer):
		self.tile_renderer = tile_renderer
		self.calc_contents()

	def __setattr__(self, name, value):
		super(BoardView, self).__setattr__(name, value)
		if name is "geometry" or name is "cols" or name is "rows":
			self.calc_contents()

	def calc_contents(self):
		self.calc_tile_size()
		self.calc_top_left_pos()

	def calc_tile_size(self):
		self.tile_size = min(self.geometry.width / self.cols, self.geometry.height / self.rows)

	def calc_top_left_pos(self):
		self.left = self.geometry.left + (self.geometry.width - self.cols * self.tile_size) / 2
		self.top = self.geometry.top + (self.geometry.height - self.rows * self.tile_size) / 2

	def paint(self, screen):
		mouse_over_tile = self.get_tile_at_pos(pygame.mouse.get_pos())

		for col in range(0, self.cols):
			x = self.left + col * self.tile_size
			for row in range(0, self.rows):
				y = self.top + row * self.tile_size
				rect = Rect(x, y, self.tile_size, self.tile_size)
				self.tile_renderer.geometry = rect
				mouseover = mouse_over_tile and mouse_over_tile == (col, row)
				pressed = self.pressed_tile and self.pressed_tile == (col, row)
				self.tile_renderer.paint(screen=screen, mouseover=mouseover, pressed=pressed)

	def mouse_button_down_event(self):
		self.pressed_tile = self.get_tile_at_pos(pygame.mouse.get_pos())

	def mouse_button_up_event(self):
		if self.pressed_tile and self.pressed_tile == self.get_tile_at_pos(pygame.mouse.get_pos()):
			print "tile clicked at:", self.pressed_tile
		self.pressed_tile = None

	def get_tile_at_pos(self, pos):
		x = (pos[0] - self.left) / self.tile_size
		y = (pos[1] - self.top) / self.tile_size
		if x < 0 or x >= self.cols or y < 0 or y >= self.rows:
			return None
		return (x, y)
