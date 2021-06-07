import os
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View, generic
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import TestMgmtCase, TestMgmtCaseLog


PATH_TO_DIR = os.path.dirname(os.path.realpath(__file__))
RECENT_PUB_CASE_NUM = 5


# home page
def index(request):
	return render(request, 'mgmt_sys/index.html')


# case page
class TestMgmtCaseView(generic.ListView):
	template_name = 'mgmt_sys/test_case.html'
	context_object_name = 'latest_test_cases_list'

	def get_queryset(self):
		return TestMgmtCase.objects.filter(case_pub_date__lte=timezone.now()).order_by('-case_pub_date')[:RECENT_PUB_CASE_NUM]


# log page
class TestMgmtCaseLogView(generic.ListView):
	template_name = 'mgmt_sys/test_log.html'
	context_object_name = 'latest_test_logs_list'

	def get_queryset(self):
		return TestMgmtCaseLog.objects.filter(case_log_pub_date__lte=timezone.now()).order_by('-case_log_pub_date')[:RECENT_PUB_CASE_NUM]


# log content page
def test_mgmt_case_log_content(request, filename):
	try:
		content = open("{}/served_files/test_mgmt_logs/{}".format(PATH_TO_DIR, filename)).read()
	except FileNotFoundError:
		return HttpResponse('No log file found for this case')
	else:
		return HttpResponse(content, content_type='text/plain')


# RESTful APIs for create and read (CR)
@method_decorator(csrf_exempt, name='dispatch')
class TestMgmtRestApi(View):

	# create new case record with both case model and case log model
	def post(self, request):
		data = json.loads(request.body.decode('utf-8'))
		case = TestMgmtCase.objects.create(**data.get('case_config'))
		case.testmgmtcaselog_set.create(**data.get('case_log_config'))
		rsps = {
			'message': 'new case created successfully'
		}
		return JsonResponse(rsps, status=201)

	# get recent published cases info
	def get(self, request):
		cases = TestMgmtCase.objects.filter(case_pub_date__lte=timezone.now()).order_by('-case_pub_date')[:RECENT_PUB_CASE_NUM]
		case_list = []
		for case in cases:
			case_list.append({
				'case_text': case.case_text,
				'case_result': case.case_result,
				'case_pub_date': case.case_pub_date,
			}) 
		rsps = {
			'recent published cases': case_list,
			'count': RECENT_PUB_CASE_NUM,
		}
		return JsonResponse(rsps)


# RESTful APIs for update and delete (UD)
@method_decorator(csrf_exempt, name='dispatch')
class TestMgmtUpdateApi(View):

	# update a case record via case id (the case must exists)
	def patch(self, request, case_id):
		recv_data = json.loads(request.body.decode('utf-8'))
		case = TestMgmtCase.objects.get(id=case_id)
		new_case_text = recv_data.get('case_text', None)
		new_case_result = recv_data.get('case_result', None)
		new_case_pub_date = recv_data.get('case_pub_date', None)
		if new_case_text:
			case.case_text = new_case_text
		if new_case_result:
			case.case_result = new_case_result
		if new_case_pub_date:
			case.case_pub_date = new_case_pub_date
		case.save()

		rsps = {
			'message': f'case (id {case_id}) updated'
		}
		return JsonResponse(rsps)

	# delete a case record via case id 
	def delete(self, request, case_id):
		case = TestMgmtCase.objects.get(id=case_id)
		case.delete()

		rsps = {
			'message': f'case (id {case_id}) deleted'
		}
		return JsonResponse(rsps)

