from django.conf.urls import url
from . import views

app_name = 'adminstrator'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^adminhome/$', views.adminhome, name='adminhome'),
    url(r'^logoutadmin/$',views.logoutadmin,name='logoutadmin'),
    url(r'^fapprove/$',views.fapproval,name='fapproval'),
    url(r'sapprove/$',views.sapproval,name='sapproval')
    ]