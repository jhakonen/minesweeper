from minesweeper.definitions import Difficulty

class CreateNewGameUseCase(object):

	def __init__(self, sink):
		self.sink = sink
		# mapping of difficulty to game board's size
		self.dif_size_dict = {
			Difficulty.EASY: (9, 9),
			Difficulty.MEDIUM: (16, 16),
			Difficulty.HARD: (16, 30)
		}

	def create_new_game(self, difficulty=Difficulty.EASY):
		self.sink.game_created()
		size = self.dif_size_dict[difficulty]
		self.sink.board_size_changed(size[0], size[1])
