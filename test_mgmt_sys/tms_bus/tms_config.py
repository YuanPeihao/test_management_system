import os
import yaml

PATH_TO_DIR = os.path.dirname(os.path.realpath(__file__))


class TmsConfig(object):

	def __init__(self):
		self.path_to_tms_config = PATH_TO_DIR + '/config/tms_config.yaml'
		self.tms_config = self.load_config()

	def load_config(self):
		with open(self.path_to_tms_config, 'r') as stream:
		    try:
		        return yaml.safe_load(stream)
		    except yaml.YAMLError as exc:
		        print(exc)


tms_config = TmsConfig()