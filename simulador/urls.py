from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<numPortas>\d+)/$', views.index, name='index'),
    url(r'^ajax/calcular/$', views.calcular, name='calcular'),
]
