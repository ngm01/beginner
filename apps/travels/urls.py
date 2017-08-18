"""
urls.py for TRAVELS app

"""

from django.conf.urls import url
from . import views
urlpatterns = [
url(r'^$', views.index),
url(r'^destination/(?P<id>\d+)$', views.destinations),
url(r'^add$', views.add),
url(r'newtrip$', views.newtrip),
url(r'logout$', views.logout),
url(r'join$', views.join)
]