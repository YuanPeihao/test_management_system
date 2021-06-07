import datetime

from django.db import models
from django.utils import timezone


class TestMgmtCase(models.Model):
	case_text = models.CharField(max_length=200)
	case_result = models.CharField(max_length=20)
	case_pub_date = models.DateTimeField('date published')

	def __str__(self):
		text_field = self.case_text[:21] 
		if len(self.case_text) > 20:
			text_field += '...'
		result_field = ' is {}'.format(self.case_result)
		pub_date_field = ' at {}'.format(self.case_pub_date)
		return text_field + result_field + pub_date_field[:23]

	def was_pub_recently(self, recent_days=1):
		return self.case_pub_date >= timezone.now() - datetime.timedelta(days=recent_days)


class TestMgmtCaseLog(models.Model):
	case = models.ForeignKey(TestMgmtCase, on_delete=models.CASCADE)  
	case_log_pub_date = models.DateTimeField('date published')
	case_log_error_msg = models.CharField(max_length=500)
	case_log_file_name = models.CharField(max_length=100)
	case_log_file_url = models.CharField(max_length=100)

	def __str__(self):
		return self.case_log_file_name



