class CallableWrapper(object):
	'''The CallableWrapper class wraps an object or a list of objects and
	proxies any call made to wrapper to the given objects.'''
	def __init__(self, arg=None):
		self.list = []
		if (hasattr(arg, "__iter__")):
			for func in arg:
				self.list.append(func)
		else:
			self.list.append(arg)

	def __getattr__(self, name):
		return CallableList(self.list, name)

	def append(self, func):
		self.list.append(func)

class CallableList(object):
	def __init__(self, list, methodname):
		self.list = list
		self.methodname = methodname

	def __call__(self, *args, **kwargs):
		for func in self.list:
			if (hasattr(func, self.methodname)):
				getattr(func, self.methodname)(*args, **kwargs)
