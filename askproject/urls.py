from django.conf.urls import *
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'askproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^login/', 'django.contrib.auth.views.login', {'template_name':'login.html'}),
    #url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page':'/'}),
    url(r'^', include('ask.urls')),
]
