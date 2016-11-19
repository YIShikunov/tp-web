from django.conf.urls import *
import django.contrib.auth.views
from ask import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^page/(?P<page_num>\d+)$', views.page, name='page'),
	url(r'^question/(?P<question_id>\d+)$', views.show_question, name='show_question'),
	url(r'^login/', django.contrib.auth.views.login, {'template_name':'login.html'}, name='login'),
	url(r'^logout/', django.contrib.auth.views.logout, {'next_page':'/'}, name='logout'),
	url(r'^signup/', views.signup, name='signup'),
	url(r'^ask/', views.ask, name='ask'),
	url(r'^answer/(?P<question_id>\d+)$', views.give_answer, name='give_answer'),
	url(r'^tag/(?P<tagline>\w+)$', views.tag, name='tag'),
	url(r'^tag/(?P<tagline>\w+)/(?P<page_num>\d+)$', views.tag_page, name='tag'),

]
