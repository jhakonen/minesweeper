from minesweeper.usecases.createnewgame import CreateNewGameUseCase
from minesweeper.definitions import Difficulty
import mock

class TestCreateNewGame(object):
	def setUp(self):
		self.game = mock.Mock()
		self.game.timer = mock.Mock()
		self.sink = mock.Mock()
		self.uc = CreateNewGameUseCase(self.game, self.sink)

	def test_create_new_game_calls_game_created(self):
		self.uc.create_new_game()
		assert self.sink.game_created.called

	def test_create_new_game_calls_board_size_changed(self):
		self.uc.create_new_game()
		self.sink.board_size_changed.called

	def test_difficulty_change_changes_board_size(self):
		data = (
			(Difficulty.EASY, 9, 9),
			(Difficulty.MEDIUM, 16, 16),
			(Difficulty.HARD, 16, 30)
		)
		for level, width, height in data:
			yield self.check_difficulty, level, width, height

	def check_difficulty(self, level, width, height):
		self.uc.create_new_game(difficulty=level)
		self.sink.board_size_changed.assert_called_once_with(width, height)

	def test_creating_game_resets_timer(self):
		self.uc.create_new_game()
		assert self.game.timer.reset.called

	def test_creating_game_starts_timer(self):
		self.uc.create_new_game()
		assert self.game.timer.start.called

	def test_two_sinks_are_called_on_create_game(self):
		sink1 = mock.Mock()
		sink2 = mock.Mock()
		self.uc = CreateNewGameUseCase(self.game, [sink1, sink2])
		self.uc.create_new_game()
		assert sink1.game_created.called
		assert sink2.game_created.called
		assert sink1.board_size_changed.called
		assert sink2.board_size_changed.called
