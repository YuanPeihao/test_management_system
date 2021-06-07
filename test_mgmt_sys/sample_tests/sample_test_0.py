#!/usr/bin/env python
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from tms_bus.tms_case_manager import tms_case_manager


# OK case
@tms_case_manager.track_test_via_tms
def sample_test_00():
	mylogger = tms_case_manager.tms_case_logger.logger
	mylogger.info('test 00 step 1')
	mylogger.warning('test 00 step 2')
	mylogger.error('test 00 step 3')
	assert True, 'sample test 00 breaks'


# NOK case
@tms_case_manager.track_test_via_tms
def sample_test_01():
	mylogger = tms_case_manager.tms_case_logger.logger
	mylogger.debug('test 01 step 0')
	mylogger.info('test 01 step 1')
	mylogger.warning('test 01 step 2')
	mylogger.error('test 01 step 3')
	assert False, 'sample test 01 breaks'


if __name__ == '__main__':
	sample_test_00()
	sample_test_01()
	# print(tms_case_manager.tms_case_pool)
	tms_case_manager.send_cases_to_tms()