from django.urls import path
from . import views

#create urls for the app

urlpatterns = [
    path('', views.index, name='index'),
]
