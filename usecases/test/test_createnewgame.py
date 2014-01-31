from minesweeper.usecases.createnewgame import CreateNewGameUseCase
from nose.tools import with_setup
import mock

def setup():
	global sink
	sink = mock.Mock()
	global uc
	uc = CreateNewGameUseCase(sink)

@with_setup(setup)
def test_create_new_game_calls_game_created():
	uc.create_new_game()
	assert sink.game_created.called

@with_setup(setup)
def test_create_new_game_calls_board_size_changed():
	uc.create_new_game()
	sink.board_size_changed.assert_called_once_with(9, 9)
