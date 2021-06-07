from django.urls import path

from . import views 


app_name = 'mgmt_sys'
urlpatterns = [
	path('', views.index, name='index'),
	path('test_mgmt_case/', views.TestMgmtCaseView.as_view(), name='test_mgmt_case'),
	path('test_mgmt_case_log/', views.TestMgmtCaseLogView.as_view(), 
		 name='test_mgmt_case_log'),
	path('test_mgmt_case_log_content/<str:filename>', views.test_mgmt_case_log_content, 
		 name='test_mgmt_case_log_content'),
	# RESTful API with CRUD operations 
	# post and get
	path('test_mgmt_rest_api/', views.TestMgmtRestApi.as_view()),
	# patch and delete
	path('test_mgmt_update/<int:case_id>', views.TestMgmtUpdateApi.as_view()),
]