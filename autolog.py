import logging

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(name)s: %(message)s',)

class Autolog(object):
	def __init__(self, original_function = None, msg = None, name='default'):
		self.original_function = original_function
		self.logger = self._getLoggerInfo(original_function)
		self.msg = msg
		self.name = name

	def __call__(self, *args, **kwargs):
		if self.msg is not None:
			self.logger.debug("called with arguments of %s > %s "%(self._args2str(*args, **kwargs) + msg ,))
		else:
			self.logger.debug("called with arguments of %s"%self._args2str(*args, **kwargs))
		self.original_function(*args, **kwargs)

	def _getLoggerInfo(self, original_function):
		try:
			return logging.getLogger(original_function.__qualname__)
		except:
			return logging.getLogger(self.name)

	def _args2str(self, *args, **kwargs):
		if kwargs:
			return ' '.join(str(i) for i in args) + ' ' + str(kwargs)
		else:
			return ' '.join(str(i) for i in args)