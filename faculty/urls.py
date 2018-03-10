from django.conf.urls import  url
from . import  views

app_name = 'faculty'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^regsuccess/$',views.regs,name='success'),
    url(r'^login/$',views.flogin,name='flogin'),
    url(r'^facultyhome/$',views.fachome,name='fachome'),
    url(r'^attendance/$',views.attendance,name='attendance'),
    url(r'^choosedate/$',views.sheet,name='sheet'),
    url(r'^editsheet/$',views.editsheet,name='editsheet'),
    url(r'^attendancesheet/$',views.viewsheet,name='viewsheet'),
    url(r'edit/$',views.view,name='view'),
    url(r'^logout/$',views.fac_logout,name='fac_logout'),
    url(r'^fullsheet/$', views.fullsheet, name='fullsheet')

]
