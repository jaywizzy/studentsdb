from django.conf.urls import url
from . import views
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns
from students  import views
urlpatterns = [
    # url(r'^register/$', register),
    url(r'^$', signup, name = 'signup'),
    # url(r'^contact/$', contact, name = 'contact'),
    # url(r'^login/$', login),
    # url(r'^students_list/$', students_list),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),

]
urlpatterns = format_suffix_patterns(urlpatterns)
