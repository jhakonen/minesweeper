class CreateNewGameUseCase(object):

	def __init__(self, sink):
		self.sink = sink

	def create_new_game(self):
		self.sink.game_created()
		self.sink.board_size_changed(9, 9)
