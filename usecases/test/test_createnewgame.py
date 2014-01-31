from minesweeper.usecases.createnewgame import CreateNewGameUseCase
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
		self.sink.board_size_changed.assert_called_once_with(9, 9)
