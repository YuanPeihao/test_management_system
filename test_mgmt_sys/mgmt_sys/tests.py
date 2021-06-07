import os
import sys

from django.test import TestCase

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from test_buses.case_mgr import print_tmc


# print(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

print_tmc()
