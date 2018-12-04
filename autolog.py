import logging
import functools

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(name)s: %(message)s',)

LOGARG = False

blogger = logging.getLogger("user")

def _getLoggerInfo(original_function, name):
	if original_function is not None:
		return logging.getLogger(original_function.__qualname__)
	else:
		return logging.getLogger(self.name)

def _args2str(*args, **kwargs):
	if LOGARG:
		if kwargs:
			return ', '.join(str(i) for i in args) + ' ' + str(kwargs)
		else:
			return ', '.join(str(i) for i in args)
	else:
		return ' '

def autolog(func = None, *, msg = None, name = 'default', solo = 0):
	if func is None:
		return functools.partial(autolog, msg = msg)


	logger = _getLoggerInfo(func, name)
	if solo:
		logger.debug("msg")
		return


	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		if msg is not None:
			logger.debug("%s \n  >> %s "%(_args2str(*args, **kwargs), msg))
		else:
			logger.debug("%s"%_args2str(*args, **kwargs))
		return func(*args, **kwargs)
	return wrapper


def call_log_class(Cls):
	for attr_name in dir(Cls):
		attr_value = getattr(Cls, attr_name)
		if type(attr_value) == type(Cls.__init__):
			setattr(Cls, attr_name, autolog(attr_value))
	return Cls


def call_log_class_soft(Cls):
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


if __name__ == '__main__':
	import os, csv

	f = open(os.getcwd() + "/files/filelist.csv", "w")
	writer = csv.writer(f)
	writer.writerow(['123', '123', '123', '123'])
	
	