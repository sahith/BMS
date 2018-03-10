from django.conf.urls import include, url
from django.contrib import admin
from . import  views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home,name='home'),
    url(r'^adminstrator/',include('adminstrator.urls')),
    url(r'^faculty/',include('faculty.urls')),
    url(r'^student/',include('student.urls')),
]
