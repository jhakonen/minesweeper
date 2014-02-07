from minesweeper.utils import CallableWrapper
import mock

class TestCallableWrapper(object):

	def test_can_append_callable(self):
		m = mock.Mock()
		l = CallableWrapper()
		l.append(m)
		l.some_function()
		assert m.some_function.called
