from django.urls import path
from django.conf.urls.static import static
from Hood import settings
from . import views

#create urls for the app

urlpatterns = [
    path('', views.Index, name='Index'),
    path('profile/<str:username>/edit', views.EditProfile, name="EditProfile"),
    path('profile/<str:username>', views.Profile, name="Profile"),
    path('<str:username>/add/business/', views.AddBusiness, name='AddBusiness'),
    path('<str:username>/add/neighbourhood/', views.AddHood, name='AddHood'),
    path('<str:username>/neighbourhoods/', views.Myhoods, name='Myhoods'),
    path('<str:username>/posts/', views.MyPosts, name='MyPosts'),
    path('<str:username>/businesses/', views.MyBusinesses, name='MyBusinesses'),
    path('search', views.Search, name="Search"),
    path('<str:username>/add/post/', views.AddPost, name='AddPost'),
    path('join/neighbourhood/<str:title>', views.JoinHood, name="JoinHood"),
    path('leave/neighbourhood/<str:title>', views.LeaveHood, name="LeaveHood"),
    path('neighbourhood/<str:title>/', views.SingleHood, name='SingleHood'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
