import os
import datetime
import requests
from collections import namedtuple
import sys
import random
import string
import traceback

PATH_TO_DIR = os.path.dirname(os.path.realpath(__file__))
PATH_TO_ROOT_DIR = os.path.dirname(PATH_TO_DIR)
PATH_TO_CASE_LOG_DIR = PATH_TO_ROOT_DIR + '/mgmt_sys/served_files/test_mgmt_logs'
sys.path.append(PATH_TO_DIR)

from tms_bus.tms_config import tms_config
from tms_bus.tms_case_logger import tms_case_logger

TMSCase = namedtuple('TMSCase', 
					 ['case_text', 'case_result', 'case_pub_date'])
TMSCaseLog = namedtuple('TMSCaseLog', 
						['case_log_pub_date', 'case_log_error_msg', 
						'case_log_file_name', 'case_log_file_url'])
TMSCaseSet = namedtuple('TMSCaseSet', 
						['TMSCase', 'TMSCaseLog'])


class TmsCaseManager(object):

	def __init__(self):
		self.tms_case_pool = []
		self.tms_info = tms_config.tms_config.get('test_management_sys')
		tms_ip, tms_port = self.tms_info.get('ip'), self.tms_info.get('port')
		self.tms_post_url = f'http://{tms_ip}:{tms_port}/mgmt_sys/test_mgmt_rest_api/'
		self.tms_case_log_dir = PATH_TO_CASE_LOG_DIR
		self.tms_case_logger = tms_case_logger

	def track_test_via_tms(self, test_func):
		def test_wrapper(*args, **kwargs):
			# TMS case and log attributes
			case_text = test_func.__name__ 
			case_result = 'OK'
			case_log_error_msg = ''
			# setup log file 
			tmp_log_filename = f'{case_text}_tmp_{self.random_lc_str()}.log'
			tmp_log_url = self.tms_case_log_dir + '/' + tmp_log_filename
			self.tms_case_logger.setup_logger(tmp_log_url)
			try:
				return test_func(*args, **kwargs)
			except Exception as err:
				case_result = 'NOK'
				case_log_error_msg = str(err)
				self.tms_case_logger.logger.error(case_log_error_msg)
				self.tms_case_logger.logger.debug(traceback.format_exc())
			finally:
				case_pub_date = case_log_pub_date = str(datetime.datetime.now())
				case_log_file_name = f'{case_text}_{case_result}_{case_log_pub_date}.log'
				case_log_file_url = self.tms_case_log_dir + '/' + case_log_file_name
				os.rename(tmp_log_url, case_log_file_url)
				tms_case = TMSCase(case_text, case_result, case_pub_date)
				tms_case_log = TMSCaseLog(case_log_pub_date, case_log_error_msg, 
										  case_log_file_name, case_log_file_url)
				tms_case_set = TMSCaseSet(tms_case, tms_case_log)
				self.tms_case_pool.append(tms_case_set)

		return test_wrapper

	def send_cases_to_tms(self):
		data_ = {}
		for tms_case_set in self.tms_case_pool:
			data_.update({'case_config': tms_case_set.TMSCase._asdict()})
			data_.update({'case_log_config': tms_case_set.TMSCaseLog._asdict()})
			requests.post(self.tms_post_url, json=data_)

	def __str__(self):
		return 'TmsCaseManager'

	@staticmethod
	def random_lc_str(num=8):
		letters = string.ascii_lowercase
		return ''.join(random.choice(letters) for _ in range(num))


tms_case_manager = TmsCaseManager()