import logging
import functools

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(name)s: %(message)s',)

def _getLoggerInfo(original_function, name):
	if original_function is not None:
		return logging.getLogger(original_function.__qualname__)
	else:
		return logging.getLogger(self.name)

def _args2str(*args, **kwargs):
	if kwargs:
		return ', '.join(str(i) for i in args) + ' ' + str(kwargs)
	else:
		return ', '.join(str(i) for i in args)

def autolog(func = None, *, msg = None, name = 'default', solo = 0):
	if func is None:
		return functools.partial(autolog, msg = msg)

	if solo:
		logger.debug("msg")
		return

	logger = _getLoggerInfo(func, name)
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		if msg is not None:
			logger.debug("| %s \n  >> %s "%(_args2str(*args, **kwargs), msg))
		else:
			logger.debug("| %s"%_args2str(*args, **kwargs))
		return func(*args, **kwargs)
	return wrapper

def call_log_class(Cls):
	class NewCls(object):
		def __init__(self, *args, **kwargs):
			self.oinstance = Cls(*args, **kwargs)

		def __getattribute__(self,s):
			try:
				x = super(NewCls, self).__getattribute__(s)
			except AttributeError:
				pass
			else:
				return x

			x = self.oinstance.__getattribute__(s)
			if type(x) == type(self.__init__):
				return autolog(x)
			else:
				return x
	return NewCls
