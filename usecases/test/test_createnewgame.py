from minesweeper.usecases.createnewgame import CreateNewGameUseCase
from minesweeper.definitions import Difficulty
from nose.tools import with_setup
import mock

class TestCreateNewGame(object):
	def setUp(self):
		self.sink = mock.Mock()
		self.uc = CreateNewGameUseCase(self.sink)

	def test_create_new_game_calls_game_created(self):
		self.uc.create_new_game()
		assert self.sink.game_created.called

	def test_create_new_game_calls_board_size_changed(self):
		self.uc.create_new_game()
		self.sink.board_size_changed.called

	def test_easy_difficulty_changes_board_size_to_9x9(self):
		self.uc.create_new_game(difficulty=Difficulty.EASY)
		self.sink.board_size_changed.assert_called_once_with(9, 9)

	def test_medium_difficulty_changes_board_size_to_16x16(self):
		self.uc.create_new_game(difficulty=Difficulty.MEDIUM)
		self.sink.board_size_changed.assert_called_once_with(16, 16)

	def test_hard_difficulty_changes_board_size_to_16x30(self):
		self.uc.create_new_game(difficulty=Difficulty.HARD)
		self.sink.board_size_changed.assert_called_once_with(16, 30)
