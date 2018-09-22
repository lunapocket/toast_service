import logging
import functools

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(name)s: %(message)s',)

class Autolog(object):
	def __init__(self, msg = None, name='default'):
		if callable(msg):
			#콜할 수 있는 일반 상황(데코메이커 호출 필요 x)
			self.func = msg
			self.logger = self._getLoggerInfo(self.func)
			self.decoagain = 0
			self.msg = None
			functools.update_wrapper(self, self.func)
		else:
			#메시지를 활용한 데코 메이커 후 다시 init 해야함
			self.decoagain = 1
			self.msg = msg
			self.name = name

	def __call__(self, *args, **kwargs):
		if self.decoagain:
		#데코 다시 필요하면
			self.decoagain = 0
			self.func = args[0]
			self.logger = self._getLoggerInfo(self.func)
			functools.update_wrapper(self, self.func)
			return self		
		
		if self.msg is not None:
			self.logger.debug("called with arguments of %s > %s "%(self._args2str(*args, **kwargs), self.msg))
		else:
			self.logger.debug("called with arguments of %s"%self._args2str(*args, **kwargs))
		self.func(*args, **kwargs)

		return self.func

	def _getLoggerInfo(self, original_function):
		if original_function is not None:
			return logging.getLogger(original_function.__qualname__)
		else:
			return logging.getLogger(self.name)

	def _args2str(self, *args, **kwargs):
		if kwargs:
			return ', '.join(str(i) for i in args) + ' ' + str(kwargs)
		else:
			return ', '.join(str(i) for i in args)