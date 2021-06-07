import logging


class TmsCaseLogger(object):

	def __init__(self):
		self.logger = None

	def __str__(self):
		return 'TmsCaseLogger'

	def setup_logger(self, filename):
		if self.logger:
			self.update_logger(filename)
		else:
			self.init_logger(filename)

	def init_logger(self, filename):
		self.logger = self.get_logger(filename)

	def update_logger(self, filename):
		for handler in self.logger.handlers[:]:
			self.logger.removeHandler(handler)
		self.logger = self.get_logger(filename)

	def get_logger(self, filename):
		logger = logging.getLogger(__name__)
		logger.setLevel(logging.DEBUG)
		self.setup_console(logger)
		self.setup_file(logger, filename)
		return logger 

	@staticmethod
	def setup_console(logger):
		c_handler = logging.StreamHandler()
		c_handler.setLevel(logging.INFO)
		c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		c_handler.setFormatter(c_format)
		logger.addHandler(c_handler)

	@staticmethod
	def setup_file(logger, filename):
		f_handler = logging.FileHandler(filename)
		f_handler.setLevel(logging.DEBUG)
		f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		f_handler.setFormatter(f_format)
		logger.addHandler(f_handler)


tms_case_logger = TmsCaseLogger()







	