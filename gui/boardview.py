
from pygame import Rect

class BoardView(object):

	geometry = Rect(0, 0, 1, 1)
	rows = 1
	cols = 1
	tile_renderer = None

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
		for col in range(0, self.cols):
			x = self.left + col * self.tile_size
			for row in range(0, self.rows):
				y = self.top + row * self.tile_size
				self.tile_renderer.geometry = Rect(x, y, self.tile_size, self.tile_size)
				self.tile_renderer.paint(screen)
