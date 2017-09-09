from django.conf.urls import url
from sprint1 import views

url patterns = [
        url(r'^$', views.index, name='index'),
        url(r'^register/', views.register, name='register'),
]


