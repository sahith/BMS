from django.conf.urls import url
from . import views

app_name = 'student'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^regsuccess/$', views.regs, name='success'),
    url(r'^login/$',views.slogin,name='slogin'),
    url(r'^studenthome/$',views.shome,name='shome'),
    url(r'^logout/$',views.stud_logout,name='stud_logout'),
    url(r'^forgotpassword/$',views.fpass,name='fpass'),
    url(r'^emailsent/$',views.email,name='email')
    ]
