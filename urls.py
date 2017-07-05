"""shanxidaily URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,RegexURLPattern
from django.contrib import admin
from shanxidaily import View,settings
from django.conf import  settings
from django.conf.urls.static import  static
import  os

urlpatterns = [
    url(r'^$',view=View.login),
    url(r'^admin/', admin.site.urls),
    url(r'^index/$',View.index),
    url(r'^getdaily/$',view=View.GetDaily),
    url(r'^getdata/(?P<pageindex>\d{1,})/(?P<pagesize>\d{1,})$',View.datachoice) ,
    url(r'^ajax_list/$',View.ajax_list,name='ajax-list'),
    url(r'^ajax_dict/$',View.ajax_dict,name='ajax-dict'),
    url(r'^regin/(?P<suscode>\d{4,8})$',view=View.susdepvalue),
    url(r'^getdailinfo/$',view=View.GetDailyinfo),
    url(r'^getsuminfo/$',view=View.GetSum),
    url(r'^getsum$',view=View.GetSumView),
    url(r'^datatoexcel',view=View.ExportDatatoexcel)
]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

