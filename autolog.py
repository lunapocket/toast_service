import logging

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(name)s: %(message)s',)

class AutoLog(object):
	def __init__(self, original_function = None, msg = None):
		self.original_function = original_function
		self.logger = self._getLoggerInfo(original_function)
		self.msg = msg

	def __call__(self, *args, **kwargs):
		if self.msg is not None:
			self.logger.debug("called > %s"%msg)
		else:
			self.logger.debug(self.msg)
		self.original_function(*args, **kwargs)

	def _getLoggerInfo(self, original_function):
		return logging.getLogger(original_function.__qualname__)